"""
Research Workflow implementation
"""

from typing import Dict, Any
from ..agents import BaseWorkflowAgent
from ..agents.research import WebResearchAgent, DocumentAnalysisAgent, SynthesisAgent

class ResearchWorkflow(BaseWorkflowAgent):
    """Orchestrates research workflow using multiple agents"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.web_agent = WebResearchAgent()
        self.analysis_agent = DocumentAnalysisAgent()
        self.synthesis_agent = SynthesisAgent()
    
    def _delegate_task(self, task_type: str, task_spec: str) -> Dict[str, Any]:
        """Delegate research tasks to specialized agents based on an explicit type."""
        try:
            if task_type == "web_research":
                result = self.web_agent.run(task_spec)
                return {"type": "web_research", "result": result}
            
            elif task_type == "analysis":
                result = self.analysis_agent.run(task_spec)
                return {"type": "analysis", "result": result}
            
            elif task_type == "synthesis":
                result = self.synthesis_agent.run(task_spec)
                return {"type": "synthesis", "result": result}
            
            else:
                return {"type": "unknown", "result": f"Task type '{task_type}' not recognized"}
            
        except Exception as e:
            return {"type": "error", "result": str(e)}
    
    def execute_research(self, topic: str) -> Dict[str, Any]:
        """Execute full research workflow"""
        try:
            # Step 1: Web Research
            print(f"--- Running Web Research for topic: {topic} ---")
            web_research_task_spec = f"Perform web research on {topic}"
            web_research_result = self._delegate_task("web_research", web_research_task_spec)
            
            if web_research_result.get("result", {}).get("status") != "success":
                 print("Web research failed. Aborting workflow.")
                 return {
                     "topic": topic,
                     "error": web_research_result.get("result", {}).get("error", "Web research failed"),
                     "web_research": web_research_result.get("result"),
                     "analysis": "Skipped due to web research failure",
                     "synthesis": "Skipped due to web research failure"
                 }
            web_research_content = web_research_result.get("result", {}).get("results", "")

            # Step 2: Analysis
            print(f"--- Running Document Analysis ---")
            analysis_task_spec = f"Analyze these research findings on {topic}: {web_research_content}"
            analysis_result = self._delegate_task("analysis", analysis_task_spec)
            
            if analysis_result.get("result", {}).get("status") != "success":
                 print("Analysis failed. Aborting workflow.")
                 return {
                     "topic": topic,
                     "error": analysis_result.get("result", {}).get("error", "Analysis failed"),
                     "web_research": web_research_result.get("result"),
                     "analysis": analysis_result.get("result"),
                     "synthesis": "Skipped due to analysis failure"
                 }
            analysis_content = analysis_result.get("result", {}).get("insights", "")
            
            # Step 3: Synthesis
            print(f"--- Running Synthesis ---")
            synthesis_task_spec = f"Synthesize the research and analysis on {topic}. Research: {web_research_content}. Analysis: {analysis_content}"
            synthesis_result = self._delegate_task("synthesis", synthesis_task_spec)
            
            # Return the results
            return {
                "topic": topic,
                "web_research": web_research_result.get("result", "No web research results"),
                "analysis": analysis_result.get("result", "No analysis results"),
                "synthesis": synthesis_result.get("result", "No synthesis results")
            }
            
        except Exception as e:
            return {
                "topic": topic,
                "error": str(e),
                "web_research": "Research failed",
                "analysis": "Analysis failed",
                "synthesis": "Synthesis failed"
            }
        
        # The original `run` method from BaseWorkflowAgent is not used here for the research workflow,
        # as this workflow is deterministic and not based on the ReAct agent loop.
        # If we wanted to use the ReAct loop, we would call super().run(topic) 