import os

import pytest

from genlink.agent import StandardAgent
from genlink.connector import Connector, GPTConnector


@pytest.fixture
def mock_connectors():
    connector1 = Connector("connector1")
    connector2 = Connector("connector2")
    return {"connector1": connector1, "connector2": connector2}


def test_load_connector_from_yaml():
    # Get the absolute path to the YAML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "yml_files", "example_connector.yml")

    # Load the connector from the YAML file
    connector = GPTConnector.from_config(api_key="test", yaml_path=yaml_path)

    # Assert that the agent was loaded correctly
    assert connector.id == "connector1"
    assert connector.model == "gpt-3.5-turbo"


def test_load_agent_from_yaml(mock_connectors):
    # Get the absolute path to the YAML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "yml_files", "example_agent.yml")

    # Load the agent from the YAML file
    agent = StandardAgent.from_config(mock_connectors, yaml_path=yaml_path)

    # Assert that the agent was loaded correctly
    assert agent.id == "example_agent"
    assert agent.name == "Example Agent"
    assert agent.description == "This is an example agent."
    assert "helpful" in agent.prompt_parameters["system_prompt"]
    assert agent.generation_parameters == {"temperature": 0.5, "max_tokens": 100, "top_p": 1.0}
    assert len(agent.connector_list) == 2
    assert [connector.id for connector in agent.connector_list] == ["connector1", "connector2"]
