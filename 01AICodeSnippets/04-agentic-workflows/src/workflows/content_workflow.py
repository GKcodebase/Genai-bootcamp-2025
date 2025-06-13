"""
Content Generation Workflow implementation
"""

from typing import Dict, Any
from ..agents import BaseWorkflowAgent
from ..agents.content import ResearchAgent, WritingAgent, EditingAgent

class ContentWorkflow(BaseWorkflowAgent):
    """Orchestrates content generation workflow"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.research_agent = ResearchAgent()
        self.writing_agent = WritingAgent()
        self.editing_agent = EditingAgent()
    
    def _delegate_task(self, task_spec: str) -> str:
        """Delegate content generation tasks to specialized agents"""
        if "research" in task_spec.lower():
            return self.research_agent.run(task_spec)
        elif "write" in task_spec.lower():
            return self.writing_agent.run(task_spec)
        elif "edit" in task_spec.lower():
            return self.editing_agent.run(task_spec)
        else:
            return "Task type not recognized"
    
    def generate_content(self, topic: str, style: str) -> Dict[str, Any]:
        """Execute content generation workflow"""
        # Run the workflow through the agent executor
        result = self.run(
            f"Generate {style} content about {topic}"
        )
        
        # Extract results from the agent's response
        return {
            "topic": topic,
            "style": style,
            "research": result.get("research", "No research results"),
            "draft": result.get("draft", "No draft generated"),
            "final_content": result.get("final_content", "No final content generated"),
            "output": result.get("output", "No output generated")
        } 