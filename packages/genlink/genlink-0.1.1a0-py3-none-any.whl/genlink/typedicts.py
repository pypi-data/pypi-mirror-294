from typing import Literal, Optional

from typing_extensions import TypedDict


# LLM Parameters
class LLMParameters(TypedDict, total=False):
    temperature: float
    max_tokens: int
    top_p: float


class PromptParameters(TypedDict, total=True):
    system_prompt: str
    pre_prompt: str
    post_prompt: str


# Inputs & Outputs
class FunctionCall(TypedDict, total=True):
    name: str
    arguments: dict[str, str]


class Message(TypedDict, total=False):
    role: Literal["user", "assistant", "system"]
    content: str
    tool_calls: Optional[list[FunctionCall]]


# Functions
class FunctionParameters(TypedDict, total=True):
    properties: dict[str, object]
    required: list[str]
    type: Literal["object"]


class Function(TypedDict, total=True):
    name: str
    description: str
    parameters: FunctionParameters


# Configuration formats
class StandardAgentConfig(TypedDict, total=False):
    id: str
    name: str
    description: str
    generation_parameters: LLMParameters
    prompt_parameters: PromptParameters
    connector_list: list[str]
    functions: Optional[list[Function]]


class StandardConnectorConfig(TypedDict, total=False):
    id: str
    model: str
    type: str
