import pytest

from genlink.agent import StandardAgent
from genlink.connector import MockConnector

# Test data
TEST_CONFIG = {
    "id": "test_agent",
    "name": "Test Agent",
    "description": "A test agent",
    "generation_parameters": {"temperature": 0.7, "max_tokens": 50, "top_p": 0.9},
    "prompt_parameters": {"system_prompt": "You are a test agent.", "pre_prompt": "Pre: ", "post_prompt": " :Post"},
    "functions": [],
    "connector_ids": ["test_connector"],
}
ADDITIONAL_FUNCTION = {
    "name": "test_function",
    "description": "A test function",
    "parameters": {"properties": {}, "required": [], "type": "object"},
}


@pytest.fixture
def mock_connector():
    connector = MockConnector(
        "test_connector",
        {"role": "assistant", "content": "Test response"},
        sleep_time=0.1,
    )
    connector.connect()
    return connector


@pytest.fixture
def standard_agent(mock_connector):
    handler_dict = {"test_connector": mock_connector}
    return StandardAgent.from_config(handler_dict, config_dict=TEST_CONFIG)


def test_preprocess_messages(standard_agent):
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]
    processed = standard_agent.preprocess_messages(messages, standard_agent.prompt_parameters)
    assert len(processed) == 3
    assert processed[0]["role"] == "system"
    assert processed[0]["content"] == "You are a test agent."
    assert processed[1]["content"] == "Pre: \nHello\n :Post"
    assert processed[2]["content"] == "Pre: \nHi there\n :Post"


def test_workflow(standard_agent):
    messages = [{"role": "user", "content": "Hello"}]
    response = standard_agent.workflow(messages)

    assert len(response) == 1
    assert response[0]["content"] == "Test response"


@pytest.mark.asyncio
async def test_async_workflow(standard_agent):
    messages = [{"role": "user", "content": "Hello"}]
    response = await standard_agent.async_workflow(messages)

    assert len(response) == 1
    assert response[0]["content"] == "Test response"


def test_workflow_with_additional_functions(standard_agent):
    messages = [{"role": "user", "content": "Hello"}]
    standard_agent.workflow(messages, additional_functions=[ADDITIONAL_FUNCTION])


@pytest.mark.asyncio
async def test_async_workflow_with_additional_functions(standard_agent):
    messages = [{"role": "user", "content": "Hello"}]
    await standard_agent.async_workflow(messages, additional_functions=[ADDITIONAL_FUNCTION])


def test_workflow_multiple_results(standard_agent):
    messages = [{"role": "user", "content": "Hello"}]
    responses = standard_agent.workflow(messages, n_results=2)

    assert len(responses) == 2
