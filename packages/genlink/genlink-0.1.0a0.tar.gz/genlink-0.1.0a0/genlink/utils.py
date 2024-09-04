import uuid
from typing import Any, Literal

import yaml
from pydantic import TypeAdapter, ValidationError

from .typedicts import Function


def validate_dictype(object: Any, schema: type) -> bool:
    DictValidator = TypeAdapter(schema)  # type: ignore
    try:
        DictValidator.validate_python(object)
        return True
    except ValidationError as exc:
        raise ValueError(f"ERROR: Invalid schema: {exc}") from exc


def get_random_id() -> str:
    """
    Generate a random unique id.

    Returns:
        str: A random unique id.
    """
    unique_id = str(uuid.uuid4())
    return unique_id


def read_yaml(file_path: str) -> dict:
    """
    Read a yaml file and return its content.

    Args:
        file_path (str): Path to the yaml file.

    Returns:
        list | dict: The content of the yaml file.
    """
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def get_role(role_str: str) -> Literal["user", "assistant", "system"]:
    if role_str == "user":
        return "user"
    elif role_str == "assistant":
        return "assistant"
    elif role_str == "system":
        return "system"
    else:
        raise ValueError(f"Invalid role: {role_str}")


# anthropic support
def convert_to_anthropic_function(function: Function) -> dict:
    new_function: dict = dict(function)
    new_function["input_schema"] = new_function.pop("parameters")
    return new_function
