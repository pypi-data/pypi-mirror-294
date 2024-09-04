import time
from unittest.mock import AsyncMock, Mock, patch

import pytest

from genlink.connector import (
    AnthropicConnector,
    GeminiConnector,
    GPTConnector,
    MockConnector,
)

# Test data
TEST_API_KEY = "test_api_key"
TEST_MODEL = "gpt-3.5-turbo"
TEST_CONFIG = {
    "model": TEST_MODEL,
    "id": "test_gpt_connector",
    "name": "Test GPT Connector",
    "description": "A test GPT connector",
}
TEST_PARAMETERS = {"temperature": 0.7, "max_tokens": 50, "top_p": 0.9}


@pytest.fixture
def gpt_connector():
    ncfg = TEST_CONFIG.copy()
    ncfg["type"] = "openai"
    return GPTConnector.from_config(TEST_API_KEY, config_dict=ncfg)


@pytest.fixture
def anthropic_connector():
    ncfg = TEST_CONFIG.copy()
    ncfg["type"] = "anthropic"
    return AnthropicConnector.from_config(TEST_API_KEY, config_dict=ncfg)


@pytest.fixture
def gemini_connector():
    ncfg = TEST_CONFIG.copy()
    ncfg["type"] = "gemini"
    return GeminiConnector.from_config(TEST_API_KEY, config_dict=ncfg)


@pytest.fixture
def mock_connector():
    mock_response = {"role": "assistant", "content": "Mock response"}
    return MockConnector("test_mock_connector", mock_response, sleep_time=0.1)


# GPTConnector tests
def test_gpt_connector_connect(gpt_connector):
    with patch("openai.OpenAI"), patch("openai.AsyncOpenAI"):
        gpt_connector.connect()
        assert gpt_connector.is_connected


def test_gpt_connector_query(gpt_connector):
    messages = [{"role": "user", "content": "Hello"}]
    functions = [
        {
            "name": "test_function",
            "description": "A test function",
            "parameters": {"properties": {}, "required": [], "type": "object"},
        }
    ]

    mock_completion = Mock()
    mock_function_call = Mock()
    mock_function_call.function.name = "test_function"
    mock_function_call.function.arguments = '{"test_argument": "test_value"}'
    mock_completion.choices = [
        Mock(
            message=Mock(content="Hello, how can I help you?", role="assistant", tool_calls=[mock_function_call]),
        )
    ]
    mock_completion.usage = Mock(total_tokens=15)

    with patch("openai.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = mock_completion
        gpt_connector.connect()

        # Without functions
        responses = gpt_connector.query(messages, TEST_PARAMETERS)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"

        # With functions
        responses = gpt_connector.query(messages, TEST_PARAMETERS, functions=functions)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"


@pytest.mark.asyncio
async def test_gpt_connector_async_query(gpt_connector):
    messages = [{"role": "user", "content": "Hello"}]
    functions = [
        {
            "name": "test_function",
            "description": "A test function",
            "parameters": {"properties": {}, "required": [], "type": "object"},
        }
    ]

    mock_completion = Mock()
    mock_function_call = Mock()
    mock_function_call.function.name = "test_function"
    mock_function_call.function.arguments = '{"test_argument": "test_value"}'
    mock_completion.choices = [
        Mock(
            message=Mock(content="Hello, how can I help you?", role="assistant", tool_calls=[mock_function_call]),
        )
    ]
    mock_completion.usage = Mock(total_tokens=15)

    async_mock = AsyncMock()
    async_mock.return_value = mock_completion

    with patch("openai.AsyncOpenAI") as mock_async_openai:
        mock_async_openai.return_value.chat.completions.create = async_mock
        gpt_connector.connect()

        # Without functions
        responses = await gpt_connector.async_query(messages, TEST_PARAMETERS)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"

        # With functions
        responses = await gpt_connector.async_query(messages, TEST_PARAMETERS, functions=functions)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"


# MockConnector tests
def test_mock_connector_connect(mock_connector):
    mock_connector.connect()
    assert mock_connector.is_connected


def test_mock_connector_query(mock_connector):
    messages = [{"role": "user", "content": "Hello"}]

    mock_connector.connect()
    responses = mock_connector.query(messages, TEST_PARAMETERS)

    assert len(responses) == 1
    assert responses[0]["content"] == "Mock response"


@pytest.mark.asyncio
async def test_mock_connector_async_query(mock_connector):
    messages = [{"role": "user", "content": "Hello"}]
    mock_connector.connect()
    start_time = time.time()
    responses = await mock_connector.async_query(messages, TEST_PARAMETERS)
    end_time = time.time()

    assert len(responses) == 1
    assert responses[0]["content"] == "Mock response"
    assert end_time - start_time >= 0.1  # Check if sleep time was respected


def test_mock_connector_multiple_responses(mock_connector):
    messages = [{"role": "user", "content": "Hello"}]

    mock_connector.connect()
    responses = mock_connector.query(messages, TEST_PARAMETERS, n_results=3)

    assert len(responses) == 3
    for response in responses:
        assert response["content"] == "Mock response"


# AnthropicConnector tests
def test_anthropic_connector_connect(anthropic_connector):
    with patch("anthropic.Anthropic"), patch("anthropic.AsyncAnthropic"):
        anthropic_connector.connect()
        assert anthropic_connector.is_connected


def test_anthropic_connector_query(anthropic_connector):
    messages = [{"role": "user", "content": "Hello"}]
    functions = [
        {
            "name": "test_function",
            "description": "A test function",
            "parameters": {"properties": {}, "required": [], "type": "object"},
        }
    ]

    mock_completion = Mock()
    mock_function_call = Mock()
    mock_function_call.function.name = "test_function"
    mock_function_call.function.arguments = '{"test_argument": "test_value"}'
    mock_completion = Mock(content="Hello, how can I help you?", tool_calls=[mock_function_call])
    mock_completion.usage.input_tokens = 15
    mock_completion.usage.output_tokens = 15

    with patch("anthropic.Anthropic") as mock_anthropic:
        mock_anthropic.return_value.messages.create.return_value = mock_completion
        anthropic_connector.connect()

        # Without functions
        responses = anthropic_connector.query(messages, TEST_PARAMETERS)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"

        # With functions
        responses = anthropic_connector.query(messages, TEST_PARAMETERS, functions=functions)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"


@pytest.mark.asyncio
async def test_anthropic_connector_async_query(anthropic_connector):
    messages = [{"role": "user", "content": "Hello"}]
    functions = [
        {
            "name": "test_function",
            "description": "A test function",
            "parameters": {"properties": {}, "required": [], "type": "object"},
        }
    ]

    mock_completion = Mock()
    mock_function_call = Mock()
    mock_function_call.function.name = "test_function"
    mock_function_call.function.arguments = '{"test_argument": "test_value"}'
    mock_completion = Mock(content="Hello, how can I help you?", tool_calls=[mock_function_call])
    mock_completion.usage.input_tokens = 15
    mock_completion.usage.output_tokens = 15

    async_mock = AsyncMock()
    async_mock.return_value = mock_completion

    with patch("anthropic.AsyncAnthropic") as mock_async_anthropic:
        mock_async_anthropic.return_value.messages.create = async_mock
        anthropic_connector.connect()

        # Without functions
        responses = await anthropic_connector.async_query(messages, TEST_PARAMETERS)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"

        # With functions
        responses = await anthropic_connector.async_query(messages, TEST_PARAMETERS, functions=functions)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"


# AnthropicConnector tests
def test_gemini_connector_connect(gemini_connector):
    with patch("anthropic.Anthropic"), patch("anthropic.AsyncAnthropic"):
        gemini_connector.connect()
        assert gemini_connector.is_connected


def test_gemini_connector_query(gemini_connector):
    messages = [{"role": "user", "content": "Hello"}]

    with patch("google.generativeai.GenerativeModel") as mock_gemini:
        mock_gemini.return_value.start_chat.return_value.send_message.return_value.text = "Hello, how can I help you?"
        gemini_connector.connect()

        # Without functions
        responses = gemini_connector.query(messages, TEST_PARAMETERS)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"


@pytest.mark.asyncio
async def test_gemini_connector_async_query(gemini_connector):
    messages = [{"role": "user", "content": "Hello"}]

    async_mock = AsyncMock()
    async_mock.return_value.text = "Hello, how can I help you?"

    with patch("google.generativeai.GenerativeModel") as mock_gemini:
        mock_gemini.return_value.start_chat.return_value.send_message_async = async_mock
        gemini_connector.connect()

        # async call
        responses = await gemini_connector.async_query(messages, TEST_PARAMETERS)
        assert len(responses) == 1
        assert responses[0]["content"] == "Hello, how can I help you?"
