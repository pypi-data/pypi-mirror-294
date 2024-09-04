import json
import time
from typing import Iterable, cast

import anthropic
from anthropic.resources.messages import MessageParam, ToolParam

from ..logger import Logger
from ..typedicts import Function, LLMParameters, Message, StandardConnectorConfig
from ..utils import (
    convert_to_anthropic_function,
    get_random_id,
    read_yaml,
    validate_dictype,
)
from .baseconnector import Connector


# GPT Support
class AnthropicConnector(Connector):
    def __init__(self, id: str, api_key: str, model_name: str) -> None:
        super().__init__(id)

        self.api_key: str = api_key
        self.model: str = model_name

    @classmethod
    def from_config(
        cls,
        api_key: str,
        yaml_path: str = "",
        config_dict: dict = {},
    ) -> "AnthropicConnector":
        assert (yaml_path != "") or {len(config_dict) > 0}, "No configuration provided"
        if len(config_dict) == 0:
            pr_config_dict: dict = read_yaml(yaml_path)
        else:
            pr_config_dict = config_dict

        assert pr_config_dict.get("type") == "anthropic", "Invalid configuration type"
        model = pr_config_dict["model"]
        connector_id = pr_config_dict["id"]

        assert validate_dictype(pr_config_dict, StandardConnectorConfig), "Invalid configuration"

        return cls(connector_id, api_key, model)

    def connect(self) -> None:
        if self.is_connected:
            return None
        try:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.async_client = anthropic.AsyncAnthropic(api_key=self.api_key)
            self.is_connected = True
        except Exception as e:
            Logger.error("Failed to connect to API", handler_id=self.id, exception=e)
            raise e
        Logger.info("Handler Connected", handler_id=self.id)

        return None

    def query(
        self,
        messages: list[Message],
        parameters: LLMParameters,
        functions: list[Function] | None = None,
        n_results: int = 1,
    ) -> list[Message]:
        assert self.is_connected, "Handler not connected"
        assert n_results == 1, "Only one result is supported"
        self.validate_input(messages, parameters, functions)

        # query id
        query_id = get_random_id()

        start_time = time.time()
        Logger.info(
            "query started",
            handler_id=self.id,
            query_id=query_id,
            start_time=start_time,
        )

        # format ad cast messages and functions
        casted_messages = cast(Iterable[MessageParam], messages)
        try:
            if functions is not None:
                format_functions = cast(Iterable[ToolParam], [convert_to_anthropic_function(f) for f in functions])
                message = self.client.messages.create(
                    model=self.model,
                    messages=casted_messages,
                    tools=format_functions,
                    **parameters,
                )

            else:
                message = self.client.messages.create(
                    model=self.model,
                    messages=casted_messages,
                    **parameters,
                )

        except Exception as e:
            Logger.error(
                "query failed",
                handler_id=self.id,
                query_id=query_id,
                exception=e,
                end_time=time.time(),
            )
            raise

        end_time = time.time()

        responses = [self.format_output(message)]

        # Get token count
        token_count = message.usage.input_tokens + message.usage.output_tokens

        # Update output metrics
        self.update_metrics(query_id, start_time, end_time, token_count)

        return responses

    async def async_query(
        self,
        messages: list[Message],
        parameters: LLMParameters,
        functions: list[Function] | None = None,
        n_results: int = 1,
    ) -> list[Message]:
        assert self.is_connected, "Handler not connected"
        assert n_results == 1, "Only one result is supported"

        self.validate_input(messages, parameters, functions)

        # query id
        query_id = get_random_id()

        start_time = time.time()
        Logger.info(
            "query started",
            handler_id=self.id,
            query_id=query_id,
            start_time=start_time,
        )

        # format ad cast messages and functions
        casted_messages = cast(Iterable[MessageParam], messages)
        try:
            if functions is not None:
                format_functions = cast(Iterable[ToolParam], [convert_to_anthropic_function(f) for f in functions])
                message = await self.async_client.messages.create(
                    model=self.model,
                    messages=casted_messages,
                    tools=format_functions,
                    **parameters,
                )

            else:
                message = await self.async_client.messages.create(
                    model=self.model,
                    messages=casted_messages,
                    **parameters,
                )

        except Exception as e:
            Logger.error(
                "query failed",
                handler_id=self.id,
                query_id=query_id,
                exception=e,
                end_time=time.time(),
            )
            raise

        end_time = time.time()

        responses = [self.format_output(message)]

        # Get token count
        token_count = message.usage.input_tokens + message.usage.output_tokens

        # Update output metrics
        self.update_metrics(query_id, start_time, end_time, token_count)

        return responses

    def format_output(self, message) -> Message:  # type: ignore
        output = {
            "role": "assistant",
            "content": message.content,
        }

        if message.tool_calls is not None:
            output["tool_calls"] = [
                {
                    "name": e.function.name,
                    "arguments": json.loads(e.function.arguments),
                }
                for e in message.tool_calls
            ]

        return cast(Message, output)
