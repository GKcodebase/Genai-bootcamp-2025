import asyncio
import os
from datetime import datetime
from src.agents.mcp_agent import MCPAgent
from src.models.mcp_protocol import SecurityLevel

async def main():
    # Initialize the MCP agent
    agent = MCPAgent(
        model_name="llama-3.3-70b-versatile",
        security_level=SecurityLevel.PUBLIC
    )
    
    # Create a context ID for our conversation
    context_id = f"conversation-{datetime.utcnow().isoformat()}"
    
    # First interaction
    response1 = await agent.generate_response(
        prompt="What is the Model Context Protocol?",
        context_id=context_id
    )
    print("\nFirst Response:")
    print(response1["response"])
    print("\nMetadata:", response1["metadata"])
    
    # Second interaction with context
    response2 = await agent.generate_response(
        prompt="Can you explain more about its features?",
        context_id=context_id
    )
    print("\nSecond Response:")
    print(response2["response"])
    print("\nMetadata:", response2["metadata"])
    
    # Get conversation history
    history = await agent.get_conversation_history(context_id=context_id)
    print("\nConversation History:")
    for entry in history:
        print(f"\nTimestamp: {entry['created_at']}")
        print(f"Content: {entry['content']}")
        print(f"Metadata: {entry['metadata']}")

if __name__ == "__main__":
    asyncio.run(main()) 