"""
Base LangChain Agent Implementation
Supports free APIs: Groq, Google AI, Anthropic (free tiers)
"""

import os
import pytz
from datetime import datetime, timedelta
import requests
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# LangChain imports
from langchain.agents import AgentType, initialize_agent, create_tool_calling_agent
from langchain.agents.agent import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.schema import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# LLM imports
try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

load_dotenv()

class BaseLangChainAgent:
    """Base class for LangChain-powered agents using free APIs."""
    
    def __init__(self, model_name="llama-3.1-8b-instant", temperature=0.7, agent_type="tool-calling", **kwargs):
        """
        Initialize the base agent.
        
        Args:
            model_name: Name of the LLM model
            temperature: LLM temperature (0.0 to 1.0)
            agent_type: Type of agent ("tool-calling" or "zero-shot")
            max_tokens: Maximum tokens for response
            verbose: Whether to show agent reasoning
        """
        self.model_name = model_name
        self.temperature = temperature
        self.agent_type = agent_type
        self.max_tokens = kwargs.get('max_tokens', 16000)
        self.verbose = kwargs.get('verbose', True)
        
        # Initialize LLM
        self.llm = self._initialize_llm()
        self.llm_provider = self._get_provider_name()
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Tools will be set by subclasses
        self.tools = self._get_tools()
        
        # Initialize agent
        self.agent_executor = self._create_agent()
        
        print(f"🤖 LangChain Agent initialized with {self.llm_provider}")
    
    def _initialize_llm(self):
        """Initialize LLM with available free APIs."""
        # Try Google AI Studio first with the basic model
        if os.getenv("GOOGLE_AI_API_KEY") and ChatGoogleGenerativeAI:
            try:
                return ChatGoogleGenerativeAI(
                    google_api_key=os.getenv("GOOGLE_AI_API_KEY"),
                    model="gemini-2.0-flash",  # Using the standard model instead of 1.5-pro
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                    request_timeout=30,
                    retry_max_attempts=2
                )
            except Exception as e:
                print(f"⚠️ Google AI initialization failed: {e}, trying next provider...")
        
        # Try Anthropic as fallback
        if os.getenv("ANTHROPIC_API_KEY") and ChatAnthropic:
            try:
                return ChatAnthropic(
                    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                    model="claude-3-haiku-20240307",
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
            except Exception as e:
                print(f"⚠️ Anthropic initialization failed: {e}, trying next provider...")
        
        # Try Groq as last resort
        if os.getenv("GROQ_API_KEY") and ChatGroq:
            try:
                return ChatGroq(
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                    model_name="llama-3.1-8b-instant",
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
        
        # Fallback error
        raise ValueError(
            "No LLM API configured! Please set up at least one of:\n"
            "- GROQ_API_KEY (recommended - fastest)\n"
            "- GOOGLE_AI_API_KEY (good alternative)\n"
            "- ANTHROPIC_API_KEY (Claude - good reasoning)\n"
            "\nGet free API keys from:\n"
            "- Groq: https://console.groq.com/keys\n"
            "- Google AI: https://makersuite.google.com/app/apikey\n"
            "- Anthropic: https://console.anthropic.com/"
        )
    
    def _get_provider_name(self) -> str:
        """Get the provider name for display."""
        class_name = self.llm.__class__.__name__
        if "Groq" in class_name:
            return "Groq"
        elif "Google" in class_name:
            return "Google AI"
        elif "Anthropic" in class_name:
            return "Anthropic"
        else:
            return "Unknown"
    
    def _get_tools(self) -> List[Tool]:
        """Get tools for the agent. Override in subclasses."""
        return []
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor."""
        if self.agent_type == "tool-calling" and self.tools:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self._get_system_prompt()),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
                MessagesPlaceholder(variable_name="chat_history", optional=True)
            ])
            
            return AgentExecutor(
                agent=create_tool_calling_agent(
                    llm=self.llm,
                    tools=self.tools,
                    prompt=prompt
                ),
                tools=self.tools,
                memory=self.memory,
                verbose=self.verbose,
                max_iterations=3,  # Reduced to prevent loops
                handle_parsing_errors=True,
                early_stopping_method="force",  # Force stop if iterations exceeded
            )
        else:
            # Fallback to zero-shot react agent
            return initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=self.verbose,
                max_iterations=5,
                handle_parsing_errors=True
            )
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the agent."""
        return """You are a helpful AI assistant that uses tools to complete tasks. When using tools:

        1. Use EXACTLY ONE tool at a time
        2. Wait for each tool's response before proceeding
        3. Use the EXACT tool names and formats specified below

        Available Tools and Formats:
        - weather: Input format 'City,Country' (e.g., 'Tokyo,Japan')
        - time: Input format 'Region/City' (e.g., 'Asia/Tokyo')
        - date_calculator: Input format 'add N' or 'subtract N' (e.g., 'add 14')
        - url_shortener: Input format: full URL
        - text_analyzer: Input format: text string to analyze

        For multi-step tasks:
        1. Break down the task into individual tool calls
        2. Make one tool call at a time
        3. Combine the results in your final response

        Example:
        Human: "What's the weather in London and what date is it in 7 days?"
        Assistant: Let me help you with that.
        1. First, I'll check the weather:
        {{weather: "London,UK"}}
        2. Then, I'll calculate the future date:
        {{date_calculator: "add 7"}}

        Always format tool calls exactly as shown in the example."""
    
    def run(self, input_text: str) -> Dict[str, Any]:
        """
        Run the agent with the given input.
        
        Args:
            input_text: User input/question
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Execute the agent
            result = self.agent_executor.invoke({"input": input_text})
            
            return {
                "output": result["output"],
                "input": input_text,
                "provider": self.llm_provider,
                "agent_type": self.agent_type,
                "tools_used": [tool.name for tool in self.tools] if self.tools else []
            }
            
        except Exception as e:
            return {
                "output": f"Error: {str(e)}",
                "input": input_text,
                "provider": self.llm_provider,
                "agent_type": self.agent_type,
                "error": True
            }
    
    def reset_memory(self):
        """Reset the agent's conversation memory."""
        self.memory.clear()
        print("🧠 Agent memory cleared")

    # def _get_weather(self, location: str) -> str:
    #     # Implementation for weather lookup
    #     pass

    # def _get_time(self, timezone: str) -> str:
    #     # Implementation for time lookup
    #     pass

    # def _calculate_date(self, operation: str) -> str:
    #     # Implementation for date calculation
    #     pass

class ToolsLangChainAgent(BaseLangChainAgent):
    def _get_tools(self) -> List[Tool]:
        """Get the list of tools for this agent."""
        return [
            Tool(
                name="weather",
                func=self._get_weather,
                description="Get current weather for a location. Input should be city name (e.g., 'London,UK')"
            ),
            Tool(
                name="time",
                func=self._get_time,
                description="Get current time in a timezone. Input should be timezone name (e.g., 'America/New_York')"
            ),
            Tool(
                name="date_calculator",
                func=self._calculate_date,
                description="Calculate future or past dates. Input should be 'add N' or 'subtract N' where N is days"
            ),
            Tool(
                name="url_shortener",
                func=self._shorten_url,
                description="Shorten a long URL using TinyURL. Input should be the full URL"
            ),
            Tool(
                name="text_analyzer",
                func=self._analyze_text,
                description="Analyze text for various metrics. Input should be the text to analyze"
            )
        ]

    def _get_weather(self, location: str) -> str:
        """Get weather information for a location using OpenWeather API."""
        try:
            api_key = os.getenv("OPENWEATHER_API_KEY")
            if not api_key:
                return "Error: OpenWeather API key not found in environment variables"

            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = {
                    "temperature": round(data["main"]["temp"]),
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"]
                }
                return (f"Weather in {location}:\n"
                       f"Temperature: {weather['temperature']}°C\n"
                       f"Humidity: {weather['humidity']}%\n"
                       f"Conditions: {weather['description']}\n"
                       f"Wind Speed: {weather['wind_speed']} m/s")
            else:
                return f"Error getting weather: {data.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_time(self, timezone: str) -> str:
        """Get current time in specified timezone."""
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        except Exception as e:
            return f"Error: Invalid timezone. {str(e)}"

    def _calculate_date(self, operation: str) -> str:
        """Calculate future or past dates."""
        try:
            parts = operation.lower().split()
            if len(parts) != 2:
                return "Error: Invalid format. Use 'add N' or 'subtract N' where N is number of days"

            action, days = parts
            days = int(days)
            
            current_date = datetime.now()
            if action == 'add':
                result_date = current_date + timedelta(days=days)
            else:  # subtract
                result_date = current_date - timedelta(days=days)

            return f"Result date: {result_date.strftime('%Y-%m-%d')} (calculated from current date: {current_date.strftime('%Y-%m-%d')})"
        except ValueError:
            return "Error: Days must be a valid number"
        except Exception as e:
            return f"Error: {str(e)}"

    def _shorten_url(self, url: str) -> str:
        """Shorten a URL using TinyURL API."""
        try:
            api_url = f"http://tinyurl.com/api-create.php?url={url}"
            response = requests.get(api_url)
            if response.status_code == 200:
                return f"Shortened URL: {response.text}"
            else:
                return "Error: Could not shorten URL"
        except Exception as e:
            return f"Error: {str(e)}"

    def _analyze_text(self, text: str) -> str:
        """Analyze text and return various metrics."""
        try:
            metrics = {
                "character_count": len(text),
                "word_count": len(text.split()),
                "sentence_count": len([s for s in text.split('.') if s.strip()]),
                "average_word_length": sum(len(word) for word in text.split()) / len(text.split()) if text.split() else 0,
                "uppercase_count": sum(1 for c in text if c.isupper()),
                "lowercase_count": sum(1 for c in text if c.islower()),
                "digit_count": sum(1 for c in text if c.isdigit()),
                "space_count": sum(1 for c in text if c.isspace())
            }
            return json.dumps(metrics, indent=2)
        except Exception as e:
            return f"Error analyzing text: {str(e)}"

    def _get_system_prompt(self) -> str:
        """Get system prompt for the agent."""
        return """You are a helpful AI assistant that uses tools to complete tasks. When using tools:

        1. Use EXACTLY ONE tool at a time
        2. Wait for each tool's response before proceeding
        3. Use the EXACT tool names and formats specified below

        Available Tools and Formats:
        - weather: Input format 'City,Country' (e.g., 'Tokyo,Japan')
        - time: Input format 'Region/City' (e.g., 'Asia/Tokyo')
        - date_calculator: Input format 'add N' or 'subtract N' (e.g., 'add 14')
        - url_shortener: Input format: full URL
        - text_analyzer: Input format: text string to analyze

        For multi-step tasks:
        1. Break down the task into individual tool calls
        2. Make one tool call at a time
        3. Combine the results in your final response

        Example:
        Human: "What's the weather in London and what date is it in 7 days?"
        Assistant: Let me help you with that.
        1. First, I'll check the weather:
        {{weather: "London,UK"}}
        2. Then, I'll calculate the future date:
        {{date_calculator: "add 7"}}

        Always format tool calls exactly as shown in the example.""" 

if __name__ == "__main__":
    # Initialize the agent for testing
    agent = ToolsLangChainAgent(
        model_name="claude-3-haiku-20240307",
        temperature=0.7
    )
    
    # Test individual tools first
    print("\n=== Testing Individual Tools ===")
    print(agent.run("What date will it be in 14 days?")["output"])
    print(agent.run("Analyze this text: 'Hello, World!'")["output"])

    # Then try the complex task
    print("\n=== Testing Complex Task ===")
    complex_task = """I need to know the weather in Tokyo, Japan, and then calculate what date it will be 14 days from now.
    Also, please analyze this text: 'The quick brown fox jumps over the lazy dog.'"""
    print(agent.run(complex_task)["output"]) 
