import json
import time
from typing import Iterable, cast

import openai
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam

from ..logger import Logger
from ..typedicts import Function, LLMParameters, Message, StandardConnectorConfig
from ..utils import get_random_id, read_yaml, validate_dictype
from .baseconnector import Connector


# GPT Support
class GPTConnector(Connector):
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
    ) -> "GPTConnector":
        assert (yaml_path != "") or {len(config_dict) > 0}, "No configuration provided"
        if len(config_dict) == 0:
            pr_config_dict: dict = read_yaml(yaml_path)
        else:
            pr_config_dict = config_dict

        assert pr_config_dict.get("type") == "openai", "Invalid configuration type"
        model = pr_config_dict["model"]
        connector_id = pr_config_dict["id"]

        assert validate_dictype(pr_config_dict, StandardConnectorConfig), "Invalid configuration"

        return cls(connector_id, api_key, model)

    def connect(self) -> None:
        if self.is_connected:
            return None
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.async_client = openai.AsyncOpenAI(api_key=self.api_key)
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
        casted_messages = cast(Iterable[ChatCompletionMessageParam], messages)
        try:
            if functions is not None:
                format_functions = [
                    cast(ChatCompletionToolParam, {"function": f, "type": "function"}) for f in functions
                ]
                completion = self.client.chat.completions.create(
                    model=self.model,
                    n=n_results,
                    messages=casted_messages,
                    tools=format_functions,
                    **parameters,
                )
            else:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    n=n_results,
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

        responses = [self.format_output(choice) for choice in completion.choices]

        # Get token count
        if completion.usage is not None:
            token_count = completion.usage.total_tokens
        else:
            token_count = 0

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
        casted_messages = cast(Iterable[ChatCompletionMessageParam], messages)
        try:
            if functions is not None:
                completion = await self.async_client.chat.completions.create(
                    model=self.model,
                    n=n_results,
                    messages=casted_messages,
                    tools=[cast(ChatCompletionToolParam, {"function": f, "type": "function"}) for f in functions],
                    **parameters,
                )

            else:
                completion = await self.async_client.chat.completions.create(
                    model=self.model,
                    n=n_results,
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

        responses = [self.format_output(choice) for choice in completion.choices]

        # Get token count
        if completion.usage is not None:
            token_count = completion.usage.total_tokens
        else:
            token_count = 0

        # Update output metrics
        self.update_metrics(query_id, start_time, end_time, token_count)

        return responses

    def format_output(self, completion_choice) -> Message:  # type: ignore
        output = {
            "role": "assistant",
            "content": completion_choice.message.content,
        }

        if completion_choice.message.tool_calls is not None:
            output["tool_calls"] = [
                {
                    "name": e.function.name,
                    "arguments": json.loads(e.function.arguments),
                }
                for e in completion_choice.message.tool_calls
            ]

        return cast(Message, output)
