from .connector import Connector
from .typedicts import (
    Function,
    LLMParameters,
    Message,
    PromptParameters,
    StandardAgentConfig,
)
from .utils import get_role, read_yaml, validate_dictype


class Agent:
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str,
        name: str,
        description: str,
        generation_parameters: LLMParameters,
        prompt_parameters: PromptParameters,
        connector_list=list[Connector],
        functions: list[Function] = [],
    ):
        """
        Abstract class representing an agent that can interact with a user.

        Args:
            id (str): A unique identifier for the agent.
            name (str): The name of the agent.
            description (str): A description of the agent.
            generation_parameters (LLMParameters): The generation parameters for the language model. \
                                                    Refer to the LLMParameters class for more information.
            connector_list (list[Handler]): A list of handlers that the agent can use. \
            functions (Optional[list[Function]], optional): A list of functions that the agent can perform. \
                                                            Refer to the Function Class for more information. \
                                                            Defaults to None.
        """
        # Validate Inputs
        assert validate_dictype(generation_parameters, LLMParameters)
        assert validate_dictype(prompt_parameters, PromptParameters)
        for function in functions:
            assert validate_dictype(function, Function)

        # Initialize Attributes
        self.is_connected: bool = False
        self.generation_parameters: LLMParameters = generation_parameters
        self.prompt_parameters: PromptParameters = prompt_parameters
        self.id: str = id
        self.name: str = name
        self.description: str = description
        self.connector_list: list[Connector] = connector_list
        self.functions: list[Function] = functions

    @classmethod
    def from_config(
        cls,
        handler_dict: dict[str, Connector],
        yaml_path: str = "",
        config_dict: dict = {},
    ) -> "Agent":
        raise NotImplementedError

    def preprocess_messages(self, messages: list[Message], prompt_parameters: PromptParameters) -> list[Message]:
        raise NotImplementedError

    def workflow(
        self,
        messages: list[Message],
        additional_functions: list[Function] = [],
        n_results: int = 1,
    ) -> list[Message]:
        messages = self.preprocess_messages(messages, self.prompt_parameters)
        raise NotImplementedError

    async def async_workflow(
        self,
        messages: list[Message],
        additional_functions: list[Function] = [],
        n_results: int = 1,
    ) -> list[Message]:
        raise NotImplementedError

    def select_handler(self) -> Connector:
        assert len(self.connector_list) > 0, "No handler available"
        for handler in self.connector_list:
            if handler.check_connection():
                return handler
        raise ValueError("No handler is connected")


class StandardAgent(Agent):
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str,
        name: str,
        description: str,
        generation_parameters: LLMParameters,
        prompt_parameters: PromptParameters,
        connector_list=list[Connector],
        functions: list[Function] = [],
    ) -> None:
        """StandardAgent is a class inheriting from Agent that represents an agent that can interact with a user.


        Args:
            id (str): A unique identifier for the agent.
            name (str): The name of the agent.
            description (str): A description of the agent.
            generation_parameters (LLMParameters): The generation parameters for the language model. \
                                                    Refer to the LLMParameters class for more information.
            connector_list (list[Handler]): A list of handlers that the agent can use. \
            functions (Optional[list[Function]], optional): A list of functions that the agent can perform. \
                                                            Refer to the Function Class for more information. \
                                                            Defaults to None.
            
        """
        super().__init__(
            id=id,
            name=name,
            description=description,
            generation_parameters=generation_parameters,
            prompt_parameters=prompt_parameters,
            functions=functions,
            connector_list=connector_list,
        )

    @classmethod
    def from_config(
        cls,
        handler_dict: dict[str, Connector],
        yaml_path: str = "",
        config_dict: dict = {},
    ) -> "StandardAgent":
        """Create an instance of StandardAgent from a yaml file or a config_dict

        Args:
            handler_dict (dict[str, Handler]): Dictionnary mapping handler id to handler instance.
            yaml_path (Optional[str], optional): Path to the yaml file. Defaults to None.
            config_dict (Optional[dict], optional): Configuration dictionnary. Defaults to None.

        Returns:
            Instance of StandardAgent.
        """
        assert (yaml_path != "") or (len(config_dict) > 0), "yaml_path or config_dict must be provided"
        if len(config_dict) == 0:
            config_dict = read_yaml(yaml_path)

        assert validate_dictype(config_dict, StandardAgentConfig)

        return cls(
            id=config_dict["id"],
            name=config_dict["name"],
            description=config_dict["description"],
            generation_parameters=config_dict["generation_parameters"],
            prompt_parameters=config_dict["prompt_parameters"],
            functions=config_dict.get("functions", []),
            connector_list=[handler_dict[handler_id] for handler_id in config_dict.get("connector_ids", [])],
        )

    def preprocess_messages(self, messages: list[Message], prompt_parameters: PromptParameters) -> list[Message]:
        """
        Preprocess the messages before sending them to the handler.

        Args:
            messages (list[Message]): A list of messages to be sent to the handler.
            prompt_parameters (PromptParameters): The prompt parameters for the agent. \

        Returns:
            list[dict]: list of Openai formatted messages
        """

        transformed_messages = [Message(role="system", content=prompt_parameters["system_prompt"])] + [
            Message(
                role=get_role(message["role"]),
                content=prompt_parameters.get("pre_prompt", "")
                + "\n"
                + message["content"]
                + "\n"
                + prompt_parameters.get("post_prompt", ""),
            )
            for message in messages
        ]

        return transformed_messages

    def workflow(
        self,
        messages: list[Message],
        additional_functions: list[Function] = [],
        n_results: int = 1,
    ) -> list[Message]:
        """
        Perform the workflow (simple conversational flow) of the agent.

        Args:
            messages (list[Message]): A list of messages to be sent to the handler.
            additional_functions (Optional[list[Function]], optional): A list of additional functions \
                that the agent can perform. \
            n_results (int, optional): The number of results to return. Defaults to 1.

        Returns:
            Response: The response from the handler.
        """
        transformed_messages = self.preprocess_messages(messages, self.prompt_parameters)
        handler = self.select_handler()

        return handler.query(
            transformed_messages,
            parameters=self.generation_parameters,
            functions=self.functions + additional_functions,
            n_results=n_results,
        )

    async def async_workflow(
        self,
        messages: list[Message],
        additional_functions: list[Function] = [],
        n_results: int = 1,
    ) -> list[Message]:
        """
        (Async) Perform the workflow (simple conversational flow) of the agent.

        Args:
            messages (list[Message]): A list of messages to be sent to the handler.
            additional_functions (Optional[list[Function]], optional): A list of additional functions \
                that the agent can perform. \
            n_results (int, optional): The number of results to return. Defaults to 1.

        Returns:
            Response: The response from the handler.
        """
        transformed_messages = self.preprocess_messages(messages, self.prompt_parameters)
        handler = self.select_handler()
        return await handler.async_query(
            transformed_messages,
            parameters=self.generation_parameters,
            functions=self.functions + additional_functions,
            n_results=n_results,
        )
