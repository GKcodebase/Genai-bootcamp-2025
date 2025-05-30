from typing import List, Dict
from duckduckgo_search import DDGS
import wikipedia
from .base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    def _get_default_tools(self) -> List[Dict]:
        return [
            {
                "name": "web_search",
                "description": "Useful for searching the internet for current information",
                "func": self._web_search
            },
            {
                "name": "wikipedia",
                "description": "Useful for getting detailed information from Wikipedia",
                "func": self._wikipedia_search
            }
        ]
    
    def _web_search(self, query: str) -> str:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        return "\n".join([f"- {result['title']}: {result['body']}" for result in results])
    
    def _wikipedia_search(self, query: str) -> str:
        try:
            return wikipedia.summary(query, sentences=3)
        except wikipedia.exceptions.DisambiguationError as e:
            return wikipedia.summary(e.options[0], sentences=3)
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{query}'" 