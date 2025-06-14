import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.agent import GoogleAgent

async def main():
    # Initialize the agent
    agent = GoogleAgent()
    
    # Example 1: Basic agent task
    print("\nExample 1: Basic agent task")
    print("-" * 50)
    
    task = "Explain the concept of quantum computing in simple terms."
    result = await agent.run_agent(task=task)
    
    print("\nTask:", task)
    print("\nResponse:", result["response"])
    print("\nMetadata:", result["metadata"])
    
    # Example 2: Agent with tools
    print("\nExample 2: Agent with tools")
    print("-" * 50)
    
    tools = [
        {
            "name": "calculator",
            "description": "Perform mathematical calculations"
        },
        {
            "name": "web_search",
            "description": "Search the web for information"
        }
    ]
    
    task = "Calculate the square root of 144 and explain the result."
    result = await agent.run_agent(
        task=task,
        tools=tools
    )
    
    print("\nTask:", task)
    print("\nResponse:", result["response"])
    print("\nMetadata:", result["metadata"])
    
    # Example 3: Agent with memory
    print("\nExample 3: Agent with memory")
    print("-" * 50)
    
    conversation_history = [
        {"role": "user", "content": "What is machine learning?"},
        {"role": "assistant", "content": "Machine learning is a branch of artificial intelligence that enables computers to learn from data and improve their performance without being explicitly programmed."},
        {"role": "user", "content": "How does it differ from deep learning?"}
    ]
    
    result = await agent.run_agent_with_memory(
        task="Explain the relationship between machine learning and deep learning.",
        conversation_history=conversation_history
    )
    
    print("\nConversation History:")
    for msg in conversation_history:
        print(f"{msg['role']}: {msg['content']}")
    
    print("\nResponse:", result["response"])
    print("\nMetadata:", result["metadata"])

if __name__ == "__main__":
    asyncio.run(main()) 