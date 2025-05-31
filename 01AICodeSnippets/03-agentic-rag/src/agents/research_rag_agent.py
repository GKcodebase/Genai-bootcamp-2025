"""
Research-focused RAG Agent implementation
"""

from typing import List, Dict, Any
from langchain.tools import Tool
from .base_rag_agent import BaseRAGAgent
from ..tools.search_tools import create_search_tools

class ResearchRAGAgent(BaseRAGAgent):
    """Agent specialized for research tasks with RAG capabilities"""
    
    def _get_tools(self) -> List[Tool]:
        """Get research-specific tools"""
        base_tools = super()._get_tools()
        search_tools = create_search_tools(self.vector_store)
        
        additional_tools = [
            Tool(
                name="summarize_findings",
                func=self._summarize_findings,
                description="Summarize the key findings from the research"
            ),
            Tool(
                name="extract_key_points",
                func=self._extract_key_points,
                description="Extract key points from the retrieved documents"
            )
        ]
        
        return base_tools + search_tools + additional_tools
    
    def _get_system_prompt(self) -> str:
        """Get research-specific system prompt"""
        return """You are an advanced research assistant that combines document analysis with autonomous research capabilities.
        
        Your primary goals are to:
        1. Search and analyze documents thoroughly
        2. Provide well-structured, evidence-based responses
        3. Cite sources and maintain academic rigor
        4. Synthesize information from multiple sources
        5. Identify gaps in knowledge and suggest further research
        
        When conducting research:
        1. Start with broad document searches
        2. Narrow down to specific relevant information
        3. Compare and contrast different sources
        4. Provide balanced perspectives
        5. Summarize key findings clearly
        """
    
    def _summarize_findings(self, context: str) -> str:
        """Summarize research findings"""
        try:
            summary_prompt = f"Please summarize the key findings from the following research:\n\n{context}"
            result = self.llm.invoke(summary_prompt)
            return result.content
        except Exception as e:
            return f"Error summarizing findings: {str(e)}"
    
    def _extract_key_points(self, text: str) -> str:
        """Extract key points from text"""
        try:
            extraction_prompt = f"Please extract the main points from the following text:\n\n{text}"
            result = self.llm.invoke(extraction_prompt)
            return result.content
        except Exception as e:
            return f"Error extracting key points: {str(e)}"
    
    def _get_sources(self, result: Dict[str, Any]) -> List[str]:
        """Extract sources from the research results"""
        sources = []
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                if isinstance(step, tuple) and len(step) == 2:
                    action, response = step
                    if action.tool == "search_documents":
                        sources.append(f"Search: {action.tool_input}")
                    elif action.tool == "retrieve_context":
                        sources.append(f"Context: {action.tool_input}")
        return sources 