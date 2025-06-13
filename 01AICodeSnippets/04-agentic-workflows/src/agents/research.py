"""
Research workflow specialized agents
"""

from typing import Dict, Any, List, Optional
from .base_workflow_agent import BaseWorkflowAgent
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

class WebResearchAgent(BaseWorkflowAgent):
    """Agent for web-based research"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = "web_researcher"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def run(self, task_spec: str) -> Dict[str, Any]:
        """Execute web research task"""
        try:
            # Extract search parameters
            search_params = self._parse_search_params(task_spec)
            
            # Perform web search
            search_results = self._search_web(search_params)
            
            # Extract relevant information
            extracted_info = self._extract_information(search_results)
            
            return {
                "status": "success",
                "results": extracted_info,
                "sources": search_results.get("sources", [])
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "results": "Web research failed"
            }
    
    def _parse_search_params(self, task_spec: str) -> Dict[str, Any]:
        """Extract search parameters from task"""
        try:
            prompt = f"Extract search parameters from this task. Return a JSON object with 'keywords' (list of strings) and 'filters' (dictionary):\n{task_spec}"
            response = self._llm_call(
                prompt=prompt,
                system_message="You are a search parameter extractor. Return a JSON object with 'keywords' and 'filters'.",
                json_output=True
            )
            if isinstance(response, dict) and "error" not in response:
                return {
                    "keywords": response.get("keywords", []),
                    "filters": response.get("filters", {})
                }
            else:
                return {"keywords": [task_spec], "filters": {}}
        except Exception as e:
            return {"keywords": [task_spec], "filters": {}}
    
    def _search_web(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform web search"""
        try:
            query = " ".join(params.get("keywords", []))
            if not query:
                return {"results": "No keywords provided for web search.", "sources": []}
            results = self._llm_call(
                prompt=f"Search the web for: {query}"
            )
            return {"results": results, "sources": ["web search results"]}
        except Exception as e:
            return {"results": "Web search failed", "sources": []}
    
    def _extract_information(self, search_results: Dict[str, Any]) -> str:
        """Extract relevant information from search results"""
        try:
            results = search_results.get("results", "")
            if not results:
                return "No search results to extract information from."
            prompt = f"Extract key information and insights from these search results:\n{results}"
            extracted = self._llm_call(
                prompt=prompt,
                system_message="You are an information extractor. Extract and summarize key information and insights."
            )
            return extracted
        except Exception as e:
            return "Information extraction failed"

class DocumentAnalysisAgent(BaseWorkflowAgent):
    """Agent for analyzing documents and extracting insights"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = "document_analyzer"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def run(self, task_spec: str) -> Dict[str, Any]:
        """Analyze documents and extract insights"""
        try:
            # Parse document content
            document = self._parse_document(task_spec)
            
            # Extract key concepts
            concepts = self._extract_concepts(document)
            
            # Analyze relationships
            relationships = self._analyze_relationships(concepts)
            
            # Generate insights
            insights = self._generate_insights(concepts, relationships)
            
            return {
                "status": "success",
                "concepts": concepts,
                "relationships": relationships,
                "insights": insights
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "insights": "Document analysis failed"
            }
    
    def _parse_document(self, task_spec: str) -> str:
        """Extract document content from task"""
        try:
            prompt = f"Extract the document content to analyze from this task:\n{task_spec}"
            return self._llm_call(prompt=prompt)
        except Exception as e:
            return f"Document parsing failed: {e}"
    
    def _extract_concepts(self, document: str) -> List[Dict[str, Any]]:
        """Extract key concepts from document"""
        try:
            if not document:
                return []
            prompt = f"Extract key concepts and their definitions from this document. Return a JSON list of objects, where each object has 'concept' and 'definition' keys:\n{document}"
            concepts = self._llm_call(
                prompt=prompt,
                system_message="You are a concept extractor. Return a JSON list of concept objects.",
                json_output=True
            )
            return concepts if isinstance(concepts, list) else []
        except Exception as e:
            return []
    
    def _analyze_relationships(self, concepts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze relationships between concepts"""
        try:
            if not concepts:
                return []
            prompt = f"Analyze relationships between these concepts. Return a JSON list of objects, where each object describes a relationship:\n{concepts}"
            relationships = self._llm_call(
                prompt=prompt,
                system_message="You are a relationship analyzer. Return a JSON list of relationship objects.",
                json_output=True
            )
            return relationships if isinstance(relationships, list) else []
        except Exception as e:
            return []
    
    def _generate_insights(self, concepts: List[Dict[str, Any]], 
                         relationships: List[Dict[str, Any]]) -> str:
        """Generate insights from concepts and relationships"""
        try:
            if not concepts and not relationships:
                return "No concepts or relationships to generate insights from."
            prompt = f"""Generate key insights based on:
            Concepts: {concepts}
            Relationships: {relationships}"""
            insights = self._llm_call(prompt=prompt)
            return insights
        except Exception as e:
            return f"Insight generation failed: {e}"

class SynthesisAgent(BaseWorkflowAgent):
    """Agent for synthesizing research findings"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = "synthesizer"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def run(self, task_spec: str) -> Dict[str, Any]:
        """Synthesize research findings"""
        try:
            # Extract research findings
            findings = self._extract_findings(task_spec)
            
            # Identify patterns
            patterns = self._identify_patterns(findings)
            
            # Generate synthesis
            synthesis = self._generate_synthesis(findings, patterns)
            
            # Create summary
            summary = self._create_summary(synthesis)
            
            return {
                "status": "success",
                "patterns": patterns,
                "synthesis": synthesis,
                "summary": summary
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "synthesis": "Synthesis failed"
            }
    
    def _extract_findings(self, task_spec: str) -> List[Dict[str, Any]]:
        """Extract research findings from task"""
        try:
            if not task_spec:
                return []
            prompt = f"Extract research findings to synthesize from this task. Return a JSON list of objects, each representing a finding:\n{task_spec}"
            findings = self._llm_call(
                prompt=prompt,
                system_message="You are a findings extractor. Return a JSON list of finding objects.",
                json_output=True
            )
            return findings if isinstance(findings, list) else []
        except Exception as e:
            return []
    
    def _identify_patterns(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify patterns in research findings"""
        try:
            if not findings:
                return []
            prompt = f"Identify patterns and themes in these findings. Return a JSON list of objects, each representing a pattern:\n{findings}"
            patterns = self._llm_call(
                prompt=prompt,
                system_message="You are a pattern identifier. Return a JSON list of pattern objects.",
                json_output=True
            )
            return patterns if isinstance(patterns, list) else []
        except Exception as e:
            return []
    
    def _generate_synthesis(self, findings: List[Dict[str, Any]], 
                          patterns: List[Dict[str, Any]]) -> str:
        """Generate synthesis from findings and patterns"""
        try:
            if not findings and not patterns:
                return "No findings or patterns to synthesize."
            prompt = f"""Generate a comprehensive synthesis based on:
            Findings: {findings}
            Patterns: {patterns}"""
            return self._llm_call(prompt=prompt)
        except Exception as e:
            return f"Synthesis generation failed: {e}"
    
    def _create_summary(self, synthesis: str) -> Dict[str, Any]:
        """Create executive summary of synthesis"""
        try:
            if not synthesis:
                return {"status": "success", "summary": "No synthesis to summarize."}
            prompt = f"Create an executive summary of this synthesis. Return a JSON object with a 'summary' key:\n{synthesis}"
            summary_obj = self._llm_call(
                prompt=prompt,
                system_message="You are a summary creator. Return a JSON object with a 'summary' key.",
                json_output=True
            )
            
            summary = summary_obj.get("summary", "Summary creation failed.") if isinstance(summary_obj, dict) else "Summary creation failed."

            return {
                "status": "success",
                "summary": summary
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "summary": "Summary creation failed"
            } 