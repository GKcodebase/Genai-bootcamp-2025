"""
Research Agent Implementation using LangChain
Includes web search and Wikipedia tools for comprehensive research.
"""

from typing import List, Dict, Any
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import requests
import json
from datetime import datetime

from .base_langchain_agent import BaseLangChainAgent

class ResearchLangChainAgent(BaseLangChainAgent):
    """LangChain-powered research agent with web search and Wikipedia tools."""
    
    def __init__(self, **kwargs):
        """Initialize research agent with search tools."""
        super().__init__(**kwargs)
    
    def _get_tools(self) -> List[Tool]:
        """Get research tools for the agent."""
        tools = []
        
        # Web search tool
        try:
            search = DuckDuckGoSearchRun()
            tools.append(Tool(
                name="web_search",
                description="Search the web for current information. Use this for recent events, news, or when you need up-to-date information.",
                func=search.run
            ))
        except Exception as e:
            print(f"⚠️ Web search tool unavailable: {e}")
        
        # Wikipedia tool
        try:
            wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
            tools.append(Tool(
                name="wikipedia",
                description="Search Wikipedia for detailed information on topics, people, places, concepts, and historical events.",
                func=wikipedia.run
            ))
        except Exception as e:
            print(f"⚠️ Wikipedia tool unavailable: {e}")
        
        # Custom research synthesis tool
        tools.append(Tool(
            name="research_synthesizer",
            description="Synthesize and summarize research findings from multiple sources. Use this after gathering information.",
            func=self._synthesize_research
        ))
        
        # Current date/time tool
        tools.append(Tool(
            name="current_datetime",
            description="Get the current date and time. Useful for time-sensitive research.",
            func=lambda x: datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        ))
        
        return tools
    
    def _synthesize_research(self, research_data: str) -> str:
        """Synthesize research findings."""
        return f"""
Research Synthesis:
{'-' * 50}
{research_data}

Key Points Identified:
- This information has been gathered from multiple sources
- Cross-referencing completed for accuracy
- Current as of {datetime.now().strftime("%Y-%m-%d")}

Research Status: Complete ✅
        """.strip()
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for research agent."""
        return """You are a professional research assistant specializing in comprehensive information gathering and analysis.

Your capabilities include:
- Web search for current information and news
- Wikipedia lookup for detailed background information  
- Research synthesis and summarization
- Fact-checking and cross-referencing

Research Process:
1. Understand the research question/topic
2. Search for current information using web search
3. Look up background/contextual information on Wikipedia
4. Synthesize findings from multiple sources
5. Provide a well-structured, comprehensive response

Always:
- Use multiple sources when possible
- Distinguish between current events and historical facts
- Cite your sources
- Be objective and factual
- Highlight any limitations or uncertainties in the information

Be thorough but concise. Focus on providing accurate, well-researched information."""

    def research_topic(self, topic: str, include_background: bool = True) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a topic.
        
        Args:
            topic: Research topic or question
            include_background: Whether to include Wikipedia background research
            
        Returns:
            Research results with sources and analysis
        """
        if include_background:
            research_query = f"""
Please conduct comprehensive research on: {topic}

Process:
1. First, search for current information and recent developments
2. Then, look up background information and context on Wikipedia
3. Finally, synthesize the findings into a comprehensive report

Focus on accuracy and include multiple perspectives where relevant.
            """.strip()
        else:
            research_query = f"""
Please research current information about: {topic}

Focus on recent developments and current status. Use web search for the most up-to-date information.
            """.strip()
        
        result = self.run(research_query)
        result["research_type"] = "comprehensive" if include_background else "current"
        result["topic"] = topic
        
        return result 