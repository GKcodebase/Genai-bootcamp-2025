import asyncio
import os
from datetime import datetime
from src.agents.mcp_agent import MCPAgent
from src.models.mcp_protocol import (
    ModelCapability,
    SecurityLevel,
    ContextType,
    TextContext,
    ImageContext
)

async def main():
    # Initialize the MCP agent with security
    agent = MCPAgent(
        model_name="llama-3.3-70b-versatile",
        security_level=SecurityLevel.PRIVATE
    )
    
    # Generate a security token for text generation
    token = await agent.generate_security_token([
        ModelCapability.TEXT_GENERATION,
        ModelCapability.SUMMARIZATION
    ])
    print(f"Generated security token: {token}")
    
    # Create a context ID for our conversation
    context_id = f"conversation-{datetime.utcnow().isoformat()}"
    
    # First interaction
    response1 = await agent.generate_response(
        prompt="What is the Model Context Protocol?",
        context_id=context_id,
        security_token=token
    )
    print("\nFirst Response:")
    print(response1["response"])
    print("\nMetadata:", response1["metadata"])
    
    # Second interaction with context
    response2 = await agent.generate_response(
        prompt="Can you explain more about its security features?",
        context_id=context_id,
        security_token=token
    )
    print("\nSecond Response:")
    print(response2["response"])
    print("\nMetadata:", response2["metadata"])
    
    # Get conversation history
    history = await agent.get_conversation_history(
        context_id=context_id,
        security_token=token
    )
    print("\nConversation History:")
    for entry in history:
        print(f"\nTimestamp: {entry['created_at']}")
        print(f"Content: {entry['content']}")
        print(f"Metadata: {entry['metadata']}")
    
    # Validate the security token
    is_valid = await agent.validate_security_token(
        token=token,
        required_capabilities=[ModelCapability.TEXT_GENERATION]
    )
    print(f"\nSecurity token valid: {is_valid}")
    
    # Try to use an invalid capability
    is_valid = await agent.validate_security_token(
        token=token,
        required_capabilities=[ModelCapability.IMAGE_GENERATION]
    )
    print(f"Security token valid for image generation: {is_valid}")
    
    # Save agent state
    state = agent.to_dict()
    print("\nAgent State:")
    print(f"Model: {state['model_name']}")
    print(f"Protocol Version: {state['protocol']['version']}")
    print(f"Registered Models: {list(state['protocol']['model_registry'].keys())}")

if __name__ == "__main__":
    asyncio.run(main()) 