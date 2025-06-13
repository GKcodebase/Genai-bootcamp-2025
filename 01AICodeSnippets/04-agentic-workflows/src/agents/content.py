"""
Content generation specialized agents
"""

from typing import Dict, Any, Optional
from .base_workflow_agent import BaseWorkflowAgent
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

class ResearchAgent(BaseWorkflowAgent):
    """Agent for researching content topics"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = "research"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def run(self, task_spec: str) -> Dict[str, Any]:
        """Execute research for content generation"""
        try:
            # Extract key points from task
            topic = self._extract_topic(task_spec)
            
            # Perform web research
            research_results = self._web_research(topic)
            
            # Analyze and organize findings
            organized_research = self._organize_research(research_results)
            
            return {
                "status": "success",
                "research": organized_research,
                "sources": research_results.get("sources", [])
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "research": "Research could not be completed"
            }
    
    def _extract_topic(self, task_spec: str) -> str:
        """Extract main topic from task specification"""
        # Use LLM to extract key topic
        response = self._llm_call(
            prompt=f"Extract the main research topic from: {task_spec}"
        )
        return response.strip()
    
    def _web_research(self, topic: str) -> Dict[str, Any]:
        """Perform web research on topic"""
        # Implement web search and content extraction
        results = self._llm_call(
            prompt=f"Research the following topic and provide key findings: {topic}"
        )
        return {"findings": results, "sources": ["web search results"]}
    
    def _organize_research(self, research_results: Dict[str, Any]) -> str:
        """Organize research findings into coherent format"""
        findings = research_results.get("findings", "")
        prompt = f"Organize these research findings into a clear, structured format:\n{findings}"
        return self._llm_call(prompt=prompt)

class WritingAgent(BaseWorkflowAgent):
    """Agent for writing content drafts"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = "writer"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def run(self, task_spec: str) -> Dict[str, Any]:
        """Generate content draft based on research"""
        try:
            # Parse task requirements
            requirements = self._parse_requirements(task_spec)
            
            # Generate outline
            outline = self._create_outline(requirements)
            
            # Write draft
            draft = self._write_draft(outline, requirements)
            
            return {
                "status": "success",
                "draft": draft,
                "outline": outline
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "draft": "Draft generation failed"
            }
    
    def _parse_requirements(self, task_spec: str) -> Dict[str, Any]:
        """Extract writing requirements from task"""
        prompt = f"Extract writing requirements (style, tone, length) from: {task_spec}"
        response = self._llm_call(prompt=prompt)
        return eval(response)  # Convert string response to dict
    
    def _create_outline(self, requirements: Dict[str, Any]) -> str:
        """Create content outline"""
        prompt = f"Create a detailed outline for content with these requirements: {requirements}"
        return self._llm_call(prompt=prompt)
    
    def _write_draft(self, outline: str, requirements: Dict[str, Any]) -> str:
        """Write content draft based on outline"""
        prompt = f"""Write a draft following this outline: {outline}
        Requirements: {requirements}"""
        return self._llm_call(prompt=prompt)

class EditingAgent(BaseWorkflowAgent):
    """Agent for editing and refining content"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = "editor"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def run(self, task_spec: str) -> Dict[str, Any]:
        """Edit and refine content"""
        try:
            # Extract content and requirements
            content = self._extract_content(task_spec)
            
            # Perform editing
            edited_content = self._edit_content(content)
            
            # Final polish
            final_content = self._polish_content(edited_content)
            
            return {
                "status": "success",
                "final_content": final_content,
                "edits_made": self._summarize_edits(content, final_content)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "final_content": "Editing failed"
            }
    
    def _extract_content(self, task_spec: str) -> str:
        """Extract content to be edited from task"""
        prompt = f"Extract the content to be edited from: {task_spec}"
        return self._llm_call(prompt=prompt)
    
    def _edit_content(self, content: str) -> str:
        """Perform initial editing pass"""
        prompt = f"""Edit this content for clarity, coherence, and correctness:
        {content}"""
        return self._llm_call(prompt=prompt)
    
    def _polish_content(self, content: str) -> str:
        """Final polish and refinement"""
        prompt = f"""Polish and refine this content for professional quality:
        {content}"""
        return self._llm_call(prompt=prompt)
    
    def _summarize_edits(self, original: str, edited: str) -> Dict[str, Any]:
        """Summarize edits made to content"""
        prompt = f"""Summarize the key changes made between these versions:
        Original: {original}
        Edited: {edited}"""
        changes = self._llm_call(prompt=prompt)
        return {"summary": changes} 