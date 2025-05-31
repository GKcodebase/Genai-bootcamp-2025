"""
Tools Agent Implementation using LangChain
Demonstrates how to use custom tools with LangChain agents.
"""

from typing import List, Dict, Any, Callable
from langchain.tools import Tool
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from .base_langchain_agent import BaseLangChainAgent

load_dotenv()

class ToolsLangChainAgent(BaseLangChainAgent):
    """LangChain-powered agent with custom tools."""
    
    def __init__(self, **kwargs):
        """Initialize tools agent with custom tools."""
        super().__init__(**kwargs)
    
    def _get_tools(self) -> List[Tool]:
        """Get custom tools for the agent."""
        tools = []
        
        # Weather tool
        if os.getenv("OPENWEATHER_API_KEY"):
            tools.append(Tool(
                name="weather",
                description="Get current weather for a location. Format: 'city,country_code'. Example: 'London,UK', 'New York,US'",
                func=self._get_weather
            ))
        
        # Time tool
        tools.append(Tool(
            name="time",
            description="Get current time in different timezones. Format: 'timezone'. Example: 'UTC', 'America/New_York'",
            func=self._get_time
        ))
        
        # Date calculator tool
        tools.append(Tool(
            name="date_calculator",
            description="Calculate dates. Format: 'operation days'. Example: 'add 7', 'subtract 30'",
            func=self._calculate_date
        ))
        
        # URL shortener tool
        tools.append(Tool(
            name="url_shortener",
            description="Shorten a URL. Format: 'url'. Example: 'https://example.com'",
            func=self._shorten_url
        ))
        
        # Text analyzer tool
        tools.append(Tool(
            name="text_analyzer",
            description="Analyze text for word count, character count, etc. Format: 'text'. Example: 'Hello world!'",
            func=self._analyze_text
        ))
        
        return tools
    
    def _get_weather(self, location: str) -> str:
        """Get weather information for a location."""
        try:
            api_key = os.getenv("OPENWEATHER_API_KEY")
            if not api_key:
                return "OpenWeather API key not configured"
            
            # Split location into city and country
            parts = location.split(',')
            city = parts[0].strip()
            country = parts[1].strip() if len(parts) > 1 else ""
            
            # Build URL
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
            
            # Make request
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200:
                return f"Error: {data.get('message', 'Unknown error')}"
            
            # Extract weather info
            weather = {
                "location": f"{city}, {country}",
                "temperature": f"{data['main']['temp']}°C",
                "feels_like": f"{data['main']['feels_like']}°C",
                "humidity": f"{data['main']['humidity']}%",
                "description": data['weather'][0]['description'],
                "wind": f"{data['wind']['speed']} m/s"
            }
            
            return json.dumps(weather, indent=2)
            
        except Exception as e:
            return f"Error getting weather: {str(e)}"
    
    def _get_time(self, timezone: str) -> str:
        """Get current time in a timezone."""
        try:
            from datetime import datetime
            import pytz
            
            # Get timezone
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            
            return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            
        except Exception as e:
            return f"Error getting time: {str(e)}"
    
    def _calculate_date(self, operation: str) -> str:
        """Calculate dates based on operation."""
        try:
            # Parse operation
            parts = operation.split()
            if len(parts) != 2:
                return "Format: 'operation days'. Example: 'add 7', 'subtract 30'"
            
            op, days = parts
            days = int(days)
            
            # Calculate date
            today = datetime.now()
            if op.lower() == 'add':
                result = today + timedelta(days=days)
            elif op.lower() == 'subtract':
                result = today - timedelta(days=days)
            else:
                return f"Unknown operation: {op}. Use 'add' or 'subtract'"
            
            return f"Date: {result.strftime('%Y-%m-%d')}"
            
        except Exception as e:
            return f"Error calculating date: {str(e)}"
    
    def _shorten_url(self, url: str) -> str:
        """Shorten a URL using a free URL shortener service."""
        try:
            # Use TinyURL API
            response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
            
            if response.status_code == 200:
                return f"Shortened URL: {response.text}"
            else:
                return f"Error shortening URL: {response.text}"
            
        except Exception as e:
            return f"Error shortening URL: {str(e)}"
    
    def _analyze_text(self, text: str) -> str:
        """Analyze text for various metrics."""
        try:
            # Basic text analysis
            analysis = {
                "character_count": len(text),
                "word_count": len(text.split()),
                "sentence_count": len([s for s in text.split('.') if s.strip()]),
                "average_word_length": sum(len(word) for word in text.split()) / len(text.split()) if text.split() else 0,
                "uppercase_count": sum(1 for c in text if c.isupper()),
                "lowercase_count": sum(1 for c in text if c.islower()),
                "digit_count": sum(1 for c in text if c.isdigit()),
                "space_count": sum(1 for c in text if c.isspace())
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            return f"Error analyzing text: {str(e)}"
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for tools agent."""
        return """You are a helpful assistant with access to various tools and utilities.

Your capabilities include:
- Weather information lookup
- Time and date calculations
- URL shortening
- Text analysis
- And more!

Process:
1. Understand the user's request
2. Choose the most appropriate tool(s)
3. Use the tools effectively
4. Provide clear, helpful responses

Always:
- Use tools when they can help
- Provide context and explanations
- Handle errors gracefully
- Be efficient and precise

Be helpful and resourceful. Use your tools to provide the best possible assistance."""

    def use_tool(self, tool_name: str, input_text: str) -> Dict[str, Any]:
        """
        Use a specific tool with the given input.
        
        Args:
            tool_name: Name of the tool to use
            input_text: Input for the tool
            
        Returns:
            Tool results with metadata
        """
        # Find the tool
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            return {
                "error": True,
                "output": f"Tool '{tool_name}' not found. Available tools: {[t.name for t in self.tools]}"
            }
        
        # Use the tool
        try:
            result = tool.func(input_text)
            return {
                "output": result,
                "tool": tool_name,
                "input": input_text
            }
        except Exception as e:
            return {
                "error": True,
                "output": f"Error using tool '{tool_name}': {str(e)}",
                "tool": tool_name,
                "input": input_text
            } 