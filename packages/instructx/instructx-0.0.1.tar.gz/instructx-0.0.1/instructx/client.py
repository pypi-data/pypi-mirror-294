from __future__ import annotations

import enum
import inspect
from copy import deepcopy
from enum import Enum
from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Optional,
    ParamSpec,
    Self,
    Type,
    TypeVar,
    Union,
    get_type_hints,
    overload,
)

import anthropic
import openai
from openai import ChatCompletion
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

T_Model = TypeVar("T_Model", bound=BaseModel)
T_Retval = TypeVar("T_Retval")
T_ParamSpec = ParamSpec("T_ParamSpec")
T = TypeVar("T", bound=Union[BaseModel, "Iterable[Any]", "Partial[Any]"])


class TypedResponseMode(Enum):
    OPENAI = "openai",
    ANTHROPIC = "anthropic",


# TODO: support parsing list[int] and list[str]


def is_primitive(type_: type) -> bool:
    if type_ in [int, str, float, bool, complex, bytes, bytearray]:
        return True
    return False


def get_annotated_str(cls: Type[Any]) -> str:
    output: str = ""
    parsed_classes = set()  # To keep track of parsed classes and avoid duplication
    subclasses_to_parse = [cls]

    def parse_class(cls: Type[Any]) -> str:
        class_name = cls.__name__
        if class_name in parsed_classes:
            return ""  # Skip already parsed classes

        parsed_classes.add(class_name)
        if issubclass(cls, enum.Enum):
            return f"enum {class_name}:\n" + "\n".join([f"    {member.value}" for member in cls]) + "\n"

        if issubclass(cls, BaseModel):
            class_output = f"class {class_name}:\n"
            type_hints = get_type_hints(cls)

            for field, field_type in type_hints.items():
                if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
                    inner_type = field_type.__args__[0]
                    class_output += f"    {field}: list[{inner_type.__name__}]"
                else:
                    class_output += f"    {field}: {field_type.__name__}"

                # Check if the field has a default value and description from the Field
                field_info = getattr(cls, field, None)
                if field_info is not None and isinstance(field_info, FieldInfo):
                    description = field_info.description
                    if description:
                        class_output += f"  # {description}"

                class_output += "\n"

            subclasses_to_parse.append(cls)
            return class_output + "\n"

        raise ValueError(f"Unsupported class type: {cls}")

    # Start with the main class
    output += parse_class(cls)

    # Check for nested classes to include their structure as well
    while subclasses_to_parse:
        next_cls = subclasses_to_parse.pop()
        for field, field_type in get_type_hints(next_cls).items():
            if (  # Check if this is a list of BaseModels
                hasattr(field_type, "__origin__")
                and field_type.__origin__ is list
                and issubclass(inner_type := field_type.__args__[0], BaseModel)
            ):
                output += parse_class(inner_type)
            elif inspect.isclass(field_type) and issubclass(field_type, (Enum, BaseModel)):
                output += parse_class(field_type)

    return output


def from_xml(xml: str, cls: BaseModel) -> BaseModel:
    def find_tag_content(tag: str, xml: str) -> str:
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start = xml.find(start_tag)
        end = xml.find(end_tag)

        if start == -1 or end == -1:
            # Try to find tag with lowercased tag name
            start_tag = f"<{tag.lower()}>"
            end_tag = f"</{tag.lower()}>"
            start = xml.find(start_tag)
            end = xml.find(end_tag)
            if start == -1 or end == -1:
                return ""

        return xml[start + len(start_tag):end]

    def find_all_tag_content(tag: str, xml: str) -> list[str]:
        """Returns a list of all content between tags

        Like
        <Mod>
        <name>Reinforced Plating</name>
        <desc>Increases armor durability by 25%</desc>
        </Mod>
        <Mod>
        <name>Energy Dispersal</name>
        <desc>Reduces energy weapon damage by 15%</desc>
        </Mod>

        would return ["<name>Reinforced Plating</name><desc>Increases armor durability by 25%</desc>", "<name>Energy Dispersal</name><desc>Reduces energy weapon damage by 15%</desc>"]
        """
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        results = []
        start_idx = 0

        while True:
            start_idx = xml.find(start_tag, start_idx)
            if start_idx == -1:
                break
            end_idx = xml.find(end_tag, start_idx)
            if end_idx == -1:
                break
            end_idx += len(end_tag)
            content = xml[start_idx + len(start_tag):end_idx - len(end_tag)]
            results.append(content.strip())
            start_idx = end_idx

        return results

    def get_value(type_, content: str):
        """Parses the content based on the annotation type"""
        # Enum
        if inspect.isclass(type_) and issubclass(type_, enum.Enum):
            return type_(content)

        # List
        if hasattr(type_, "__origin__") and type_.__origin__ is list:
            is_class = inspect.isclass(type_.__args__[0]) and issubclass(type_.__args__[0], BaseModel)
            inner_type = type_.__args__[0]
            if is_class:
                return [get_value(inner_type, inner_content) for inner_content in find_all_tag_content(inner_type.__name__, content)]
            else:  # List of primitives
                return [get_value(inner_type, inner_content) for inner_content in find_all_tag_content("value", content)]

        # Primitives
        if is_primitive(type_):
            return type_(content)

        return parse_props(type_, content)

    def parse_props(cls: BaseModel, content: str):
        props = cls.__fields__.keys()
        prob_values = {prop: None for prop in props}

        for prop in props:
            tag_content = find_tag_content(prop, content)
            prob_values[prop] = get_value(cls.__annotations__[prop], tag_content)

        return prob_values

    # Start with the most outer class
    outer_content = find_tag_content(cls.__name__, xml)
    props = parse_props(cls, outer_content)
    return cls(**props)


class InstructX:
    client: openai.OpenAI
    mode: TypedResponseMode
    create_fn: Callable[..., Any]

    def __init__(self, client: openai.OpenAI, mode: TypedResponseMode, create: Callable[..., Any], **kwargs: Any):
        self.client = client
        self.mode = mode
        self.create_fn = create
        self.kwargs = kwargs

    @property
    def chat(self) -> Self:
        return self

    @property
    def completions(self) -> Self:
        return self

    @property
    def messages(self) -> Self:
        return self

    @overload
    def create(
        self: AsyncInstructX,
        response_model: type[T],
        **kwargs: Any
    ) -> Awaitable[Any]:
        ...

    @overload
    def create(
        self: Self,
        response_model: type[T],
        **kwargs: Any
    ):
        ...

    def create(
        self,
        response_model: type[T],
        **kwargs: Any
    ) -> T | Any | Awaitable[T] | Awaitable[Any]:
        kwargs = self.patch_system_prompt(response_model, kwargs)
        return self.create_fn(response_model=response_model, **kwargs)

    def patch_system_prompt(self, response_model: T, kwargs: Any) -> Any:
        """
        Injects the typed instructions into the system prompt.

        If {instructx.response_model} is in the prompt, it will be replaced with the actual response model.
        """
        annotated_str = self._chat(response_model)

        """
        Account for {"role": ..., "content": ...} and {"role": ..., "content": [{'type': 'text', 'text': "..." }]}
        """

        def contains_format_key(prompt: str | list[dict]) -> bool:
            if prompt is None:
                return False
            if isinstance(prompt, list):
                return prompt[0]["type"] == "text" and "{instructx.response_model}" in prompt[0]["text"]
            return "{instructx.response_model}" in prompt

        def replace_format_key(prompt: str | list[dict], response_model: str) -> str:
            if prompt is None:
                return None
            if isinstance(prompt, list):
                if prompt[0]["type"] == "text":
                    prompt[0]["text"] = prompt[0]["text"].replace("{instructx.response_model}", response_model)
                return prompt

            return prompt.replace("{instructx.response_model}", response_model)

        def replace_all_format_keys(messages: list[dict[str, str]], response_model: str) -> list[dict[str, str]]:
            return [
                {
                    "role": message["role"],
                    "content": replace_format_key(message["content"], response_model),
                }
                for message in messages
            ]

        if self.mode == TypedResponseMode.OPENAI:
            messages: list[dict[str, str]] = deepcopy(kwargs.get("messages", []))

            use_format = any(contains_format_key(message["content"]) for message in messages)
            if use_format:
                messages = replace_all_format_keys(messages, annotated_str)
            elif len(messages) > 0 and messages[0]["role"] == "system":
                messages[0]["content"] += f"\n\n---\n\n{annotated_str}"
            else:
                raise ValueError("System message not found in messages")

            kwargs["messages"] = messages
            return kwargs
        if self.mode == TypedResponseMode.ANTHROPIC:
            system = kwargs.get("system", "")
            use_format = contains_format_key(system)
            if use_format:
                kwargs["system"] = replace_format_key(system, annotated_str)

            messages = deepcopy(kwargs.get("messages", []))
            use_format = use_format or any(contains_format_key(message["content"]) for message in messages)
            if use_format:
                messages = replace_all_format_keys(messages, annotated_str)
            else:
                system += f"\n\n---\n\n{annotated_str}"

            kwargs["system"] = system
            kwargs["messages"] = messages
            return kwargs

    def get_field_repr(self, field: str, field_cls: type) -> str:
        if hasattr(field_cls, "__origin__") and field_cls.__origin__ is list:
            inner_type = field_cls.__args__[0]
            if inspect.isclass(inner_type) and issubclass(inner_type, BaseModel):
                return f"<{field}>\n...\n</{field}>"
            else:  # List of primitives, use <value>...</value>
                return f"<{field}>\n<value>...</value>\n...\n</{field}>"
        return f'<{field}>...</{field}>'

    def _chat(self, response_model: type):
        annotated_str = get_annotated_str(response_model)
        # add a <var_name>...</var_name> for each field in the response_model
        response_format_str = f"""<{response_model.__name__}>
{"\n".join([self.get_field_repr(field, field_cls) for field, field_cls in get_type_hints(response_model).items()])}
</{response_model.__name__}>"""

        system_prompt = f"""<data_types>
{annotated_str.strip()}
<data_types>

<response_format desc="ONLY generate the {response_model.__name__} class in your response">
{response_format_str}
</response_format>"""
        return system_prompt


class AsyncInstructX(InstructX):
    async def create(
        self,
        response_model: type[T],
        **kwargs: Any
    ):
        kwargs = self.patch_system_prompt(response_model, kwargs)
        return await self.create_fn(response_model=response_model, **kwargs)


"""
PATCHING
"""


def is_async_method(func: Callable[..., Any]) -> bool:
    """Checks if function is async, even if it's wrapped"""
    is_async = inspect.iscoroutinefunction(func)
    # Find the innermost function
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__  # type: ignore
        is_async = is_async or inspect.iscoroutinefunction(func)
    return is_async


def process_response(
    response: ChatCompletion,
    response_model: Optional[type[T_Model]],
    mode: TypedResponseMode,
) -> T_Model | ChatCompletion:
    if response_model is None:
        return response

    content: str = None
    if mode == TypedResponseMode.OPENAI:
        content = response.choices[0].message.content
    elif mode == TypedResponseMode.ANTHROPIC:
        content = response.content[0].text

    ret: T_Model = from_xml(content, response_model)
    ret._raw_response = response
    return ret


def patch(
    client: openai.OpenAI | openai.AsyncOpenAI,
    mode: TypedResponseMode,
    create: Callable
) -> openai.OpenAI | openai.AsyncOpenAI:
    """
    Patch the `client.chat.completions.create` method:
    - `response_model` parameter to parse the response from OpenAI's API
    - `max_retries` parameter to retry request if the response is not valid
    """
    is_async = is_async_method(create)

    @wraps(create)
    async def wrapped_create_async(
        response_model: type[T_Model] = None,
        *args: T_ParamSpec.args,
        **kwargs: T_ParamSpec.kwargs,
    ) -> T_Model:
        response: ChatCompletion = await create(*args, **kwargs)
        return process_response(response, response_model, mode)

    @wraps(create)
    def wrapped_create_sync(
        response_model: type[T_Model] = None,
        *args: T_ParamSpec.args,
        **kwargs: T_ParamSpec.kwargs,
    ) -> T_Model:
        response: ChatCompletion = create(*args, **kwargs)
        return process_response(response, response_model, mode)

    wrapped_func = wrapped_create_async if is_async else wrapped_create_sync
    # client.chat.completions.create = wrapped_func
    return wrapped_func


"""
OPENAI
"""


@overload
def from_openai(
    client: openai.OpenAI,
    **kwargs: Any,
):
    ...


@overload
def from_openai(
    client: openai.AsyncOpenAI,
    **kwargs: Any,
):
    ...


def from_openai(
    client: openai.OpenAI | openai.AsyncOpenAI,
    **kwargs: Any,
):
    if not isinstance(client, (openai.OpenAI, openai.AsyncOpenAI)):
        import warnings
        warnings.warn("client must be an instance of openai.OpenAI or openai.AsyncOpenAI", stacklevel=2)

    cls = InstructX if isinstance(client, openai.OpenAI) else AsyncInstructX
    return cls(
        client=client,
        mode=TypedResponseMode.OPENAI,
        create=patch(client=client, create=client.chat.completions.create, mode=TypedResponseMode.OPENAI),
        **kwargs,
    )


"""
ANTHROPIC
"""


@overload
def from_anthropic(
    client: anthropic.Anthropic,
    **kwargs: Any,
):
    ...


@overload
def from_anthropic(
    client: anthropic.AsyncAnthropic,
    **kwargs: Any,
):
    ...


def from_anthropic(
    client: anthropic.Anthropic | anthropic.AsyncAnthropic,
    **kwargs: Any,
) -> InstructX | AsyncInstructX:
    if not isinstance(client, (anthropic.Anthropic, anthropic.AsyncAnthropic)):
        import warnings
        warnings.warn("client must be an instance of anthropic.Anthropic or anthropic.AsyncAnthropic", stacklevel=2)

    cls = InstructX if isinstance(client, anthropic.Anthropic) else AsyncInstructX
    return cls(
        client=client,
        mode=TypedResponseMode.ANTHROPIC,
        create=patch(client=client, create=client.messages.create, mode=TypedResponseMode.ANTHROPIC),
        **kwargs,
    )
