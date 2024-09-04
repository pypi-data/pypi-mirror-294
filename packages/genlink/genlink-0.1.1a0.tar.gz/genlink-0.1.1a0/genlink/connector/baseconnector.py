import asyncio
import time

from ..logger import Logger
from ..typedicts import Function, LLMParameters, Message
from ..utils import get_random_id, validate_dictype


class Connector:
    def __init__(
        self,
        id: str,
    ) -> None:
        """
        Abstract class representing a handler for a language model.

        Args:
            id (str): A unique identifier for the handler.
        """
        self.is_connected = False
        self.id = id

        # Performance metrics
        self.total_execution_time = 0.0
        self.total_tokens = 0.0

    @classmethod
    def from_config(
        cls,
        api_key: str,
        yaml_path: str = "",
        config_dict: dict = {},
    ) -> "Connector":
        assert (yaml_path != "") or {len(config_dict) > 0}, "No configuration provided"

        raise NotImplementedError

    def connect(self) -> None:
        raise NotImplementedError

    def validate_input(
        self,
        messages: list[Message],
        parameters: LLMParameters,
        functions: list[Function] | None = None,
    ) -> None:
        assert validate_dictype(parameters, LLMParameters), "Invalid parameters"
        for message in messages:
            assert validate_dictype(message, Message), "Invalid messages"
        if functions is not None:
            for function in functions:
                assert validate_dictype(function, Function), "Invalid functions"

    def query(
        self,
        messages: list[Message],
        parameters: LLMParameters,
        functions: list[Function] | None = None,
        n_results: int = 1,
    ) -> list[Message]:
        query_id = get_random_id()  # noqa F841
        self.validate_input(messages, parameters, functions)
        raise NotImplementedError

    async def async_query(
        self,
        messages: list[Message],
        parameters: LLMParameters,
        functions: list[Function] | None = None,
        n_results: int = 1,
    ) -> list[Message]:
        query_id = get_random_id()  # noqa F841
        self.validate_input(messages, parameters, functions)
        raise NotImplementedError

    def check_connection(self) -> bool:
        if self.is_connected:
            return True
        return False

    def update_metrics(
        self,
        query_id: str,
        start_timestamp: float,
        end_timestamp: float,
        total_tokens: int,
    ) -> None:
        """
        Update the performance metrics of the handler.

        Args:
            query_id (str): The unique identifier of the query.
            start_timestamp (int): The start timestamp of the query.
            end_timestamp (int): The end timestamp of the query.
            total_tokens (int): The total number of tokens used in the query.
        """
        execution_time = (end_timestamp - start_timestamp) / 1000
        token_rate = round(total_tokens / execution_time, 2)

        self.total_execution_time += execution_time
        self.total_tokens += total_tokens

        Logger.info(
            f"""query {query_id} for Handler {self.id} completed. \
                Execution time: {execution_time} seconds. {token_rate}/s average token per second"""
        )

    def format_output(self, completion_choice) -> Message:  # type: ignore
        raise NotImplementedError


# Mock Handler
class MockConnector(Connector):
    def __init__(self, id: str, mock_response: Message, sleep_time: int = 0) -> None:
        super().__init__(id)

        self.mock_response = mock_response
        self.sleep_time = sleep_time

    def connect(self) -> None:
        self.is_connected = True
        Logger.info("Handler Connected", handler_id=self.id)

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

        responses = [self.mock_response for _ in range(n_results)]

        time.sleep(self.sleep_time)

        end_time = time.time()

        # Update output metrics
        self.update_metrics(query_id, start_time, end_time, 100)

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

        responses = [self.mock_response for _ in range(n_results)]

        await asyncio.sleep(self.sleep_time)

        end_time = time.time()

        # Update output metrics
        self.update_metrics(query_id, start_time, end_time, 100)

        return responses

    def format_output(self, response: Message) -> Message:
        return response
