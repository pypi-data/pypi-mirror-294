import time

# Gemini Support
import google.generativeai as genai  # type: ignore

from ..logger import Logger
from ..typedicts import Function, LLMParameters, Message, StandardConnectorConfig
from ..utils import get_random_id, read_yaml, validate_dictype
from .baseconnector import Connector


# GPT Support
class GeminiConnector(Connector):
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
    ) -> "GeminiConnector":
        assert (yaml_path != "") or {len(config_dict) > 0}, "No configuration provided"
        if len(config_dict) == 0:
            pr_config_dict: dict = read_yaml(yaml_path)
        else:
            pr_config_dict = config_dict

        assert pr_config_dict.get("type") == "gemini", "Invalid configuration type"
        model = pr_config_dict["model"]
        connector_id = pr_config_dict["id"]

        assert validate_dictype(pr_config_dict, StandardConnectorConfig), "Invalid configuration"

        return cls(connector_id, api_key, model)

    def connect(self) -> None:
        if self.is_connected:
            return None
        try:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
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
        assert n_results == 1, "Gemini only supports n_results=1"

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

        # replace first system message with user message
        if messages[0]["role"] == "system":
            modified_messages = [
                {"role": "user", "content": messages[0]["content"]},
                *messages[1:],
            ]
        else:
            modified_messages = [m for m in messages]  # noqa C416

        try:
            chat = self.client.start_chat(
                history=modified_messages[:-1],
            )
            assert modified_messages[-1]["role"] == "user", "Last message must be user message"
            response = chat.send_message(
                modified_messages[-1]["content"],
                max_output_tokens=parameters["max_tokens"],
                temperature=parameters["temperature"],
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

        responses = [self.format_output(response)]

        # Get token count
        token_count = self.client.count_tokens(chat.history)

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
        assert n_results == 1, "Gemini only supports n_results=1"

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

        # replace first system message with user message
        if messages[0]["role"] == "system":
            modified_messages = [
                {"role": "user", "content": messages[0]["content"]},
                *messages[1:],
            ]
        else:
            modified_messages = [m for m in messages]  # noqa C416

        try:
            chat = self.client.start_chat(
                history=modified_messages[:-1],
            )
            assert modified_messages[-1]["role"] == "user", "Last message must be user message"
            response = await chat.send_message_async(
                modified_messages[-1]["content"],
                max_output_tokens=parameters["max_tokens"],
                temperature=parameters["temperature"],
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

        responses = [self.format_output(response)]

        # Get token count
        token_count = self.client.count_tokens(chat.history)

        # Update output metrics
        self.update_metrics(query_id, start_time, end_time, token_count)

        return responses

    def format_output(self, response) -> Message:  # type: ignore
        return {
            "role": "assistant",
            "content": response.text,
        }
