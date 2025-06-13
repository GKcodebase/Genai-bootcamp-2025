import pytest
import os
from unittest.mock import AsyncMock, patch
from src.agents.mcp_agent import MCPAgent
from src.models.context import ConversationContext

@pytest.fixture
def context():
    """Create a test conversation context."""
    return ConversationContext(
        conversation_id="test_1",
        metadata={"test": True}
    )

@pytest.fixture
def agent():
    """Create a test MCP agent."""
    return MCPAgent(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )

@pytest.mark.asyncio
async def test_agent_initialization(agent):
    """Test agent initialization."""
    with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
        await agent.initialize()
        assert agent.client is not None

@pytest.mark.asyncio
async def test_chat_response(agent, context):
    """Test chat response handling."""
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = "Test response"
    mock_response.usage.completion_tokens = 10
    mock_response.created = "2024-03-20T00:00:00"
    
    with patch.object(agent.client.chat.completions, "create") as mock_create:
        mock_create.return_value = mock_response
        
        response = await agent.chat(
            message="Test message",
            context=context
        )
        
        assert response["content"] == "Test response"
        assert "metadata" in response
        assert response["metadata"]["tokens"] == 10

@pytest.mark.asyncio
async def test_context_validation(agent):
    """Test context validation."""
    with pytest.raises(ValueError):
        await agent.chat(
            message="Test message",
            context=None
        )

@pytest.mark.asyncio
async def test_error_handling(agent, context):
    """Test error handling."""
    with patch.object(agent.client.chat.completions, "create") as mock_create:
        mock_create.side_effect = Exception("API Error")
        
        with pytest.raises(Exception):
            await agent.chat(
                message="Test message",
                context=context
            )
        
        # Verify error was added to context
        last_message = context.get_last_message()
        assert last_message is not None
        assert "Error in chat" in last_message.content

@pytest.mark.asyncio
async def test_state_management(agent, context):
    """Test state management."""
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = "Test response"
    mock_response.usage.completion_tokens = 10
    mock_response.created = "2024-03-20T00:00:00"
    
    with patch.object(agent.client.chat.completions, "create") as mock_create:
        mock_create.return_value = mock_response
        
        await agent.chat(
            message="Test message",
            context=context
        )
        
        # Verify state was updated
        assert "last_model" in context.state
        assert "last_tokens" in context.state
        assert "last_timestamp" in context.state 