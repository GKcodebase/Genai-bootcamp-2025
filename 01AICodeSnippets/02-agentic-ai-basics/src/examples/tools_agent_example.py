"""
Example usage of the ToolsLangChainAgent.
"""

import os
from dotenv import load_dotenv
from langchain_agents.tools_langchain_agent import ToolsLangChainAgent
from langchain_agents.base_langchain_agent import BaseLangChainAgent

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the agent
    agent = ToolsLangChainAgent(
        model_name="llama3-8b-8192",  # Using Groq's Mixtral model
        temperature=0.7
    )
    
    # Example 1: Weather lookup
    print("\n=== Weather Lookup ===")
    weather_result = agent.use_tool("weather", "London,UK")
    print(weather_result["output"])
    
    # Example 2: Time in different timezones
    print("\n=== Time Lookup ===")
    time_result = agent.use_tool("time", "America/New_York")
    print(time_result["output"])
    
    # Example 3: Date calculation
    print("\n=== Date Calculation ===")
    date_result = agent.use_tool("date_calculator", "add 7")
    print(date_result["output"])
    
    # Example 4: URL shortening
    print("\n=== URL Shortening ===")
    url_result = agent.use_tool("url_shortener", "https://www.example.com")
    print(url_result["output"])
    
    # Example 5: Text analysis
    print("\n=== Text Analysis ===")
    text = "Hello, World! This is a test message with 123 numbers."
    text_result = agent.use_tool("text_analyzer", text)
    print(text_result["output"])
    
    # Example 6: Using the agent for a complex task
    print("\n=== Complex Task ===")
    prompt = """I need to know the weather in Tokyo, Japan, and then calculate what date it will be 14 days from now.
    Also, please analyze this text: 'The quick brown fox jumps over the lazy dog.'"""
    
    response = agent.run(prompt)
    print("\nAgent Response:")
    print(response)

if __name__ == "__main__":
    main() 