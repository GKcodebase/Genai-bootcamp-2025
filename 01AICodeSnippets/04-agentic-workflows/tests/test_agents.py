"""
Tests for agent implementations
"""

import unittest
from unittest.mock import patch, MagicMock
from src.agents.content import ResearchAgent, WritingAgent, EditingAgent
from src.agents.research import WebResearchAgent, DocumentAnalysisAgent, SynthesisAgent

class TestContentAgents(unittest.TestCase):
    """Test cases for content generation agents"""
    
    def setUp(self):
        """Set up test cases"""
        self.research_agent = ResearchAgent()
        self.writing_agent = WritingAgent()
        self.editing_agent = EditingAgent()
    
    @patch('src.agents.content.ResearchAgent._llm_call')
    def test_research_agent(self, mock_llm):
        """Test research agent functionality"""
        mock_llm.return_value = '{"key": "value"}'
        result = self.research_agent.run("Research AI topics")
        self.assertEqual(result['status'], 'success')
        self.assertIn('research', result)
    
    @patch('src.agents.content.WritingAgent._llm_call')
    def test_writing_agent(self, mock_llm):
        """Test writing agent functionality"""
        mock_llm.return_value = '{"outline": "test outline"}'
        result = self.writing_agent.run("Write about AI")
        self.assertEqual(result['status'], 'success')
        self.assertIn('draft', result)
    
    @patch('src.agents.content.EditingAgent._llm_call')
    def test_editing_agent(self, mock_llm):
        """Test editing agent functionality"""
        mock_llm.return_value = 'Edited content'
        result = self.editing_agent.run("Edit this content")
        self.assertEqual(result['status'], 'success')
        self.assertIn('final_content', result)

class TestResearchAgents(unittest.TestCase):
    """Test cases for research agents"""
    
    def setUp(self):
        """Set up test cases"""
        self.web_agent = WebResearchAgent()
        self.doc_agent = DocumentAnalysisAgent()
        self.synthesis_agent = SynthesisAgent()
    
    @patch('src.agents.research.WebResearchAgent._llm_call')
    def test_web_research_agent(self, mock_llm):
        """Test web research agent functionality"""
        mock_llm.return_value = '{"results": ["result1", "result2"]}'
        result = self.web_agent.run("Search AI topics")
        self.assertEqual(result['status'], 'success')
        self.assertIn('results', result)
    
    @patch('src.agents.research.DocumentAnalysisAgent._llm_call')
    def test_document_analysis_agent(self, mock_llm):
        """Test document analysis agent functionality"""
        mock_llm.return_value = '["concept1", "concept2"]'
        result = self.doc_agent.run("Analyze this document")
        self.assertEqual(result['status'], 'success')
        self.assertIn('concepts', result)
    
    @patch('src.agents.research.SynthesisAgent._llm_call')
    def test_synthesis_agent(self, mock_llm):
        """Test synthesis agent functionality"""
        mock_llm.return_value = '{"summary": "test summary"}'
        result = self.synthesis_agent.run("Synthesize findings")
        self.assertEqual(result['status'], 'success')
        self.assertIn('synthesis', result)

class TestErrorHandling(unittest.TestCase):
    """Test error handling in agents"""
    
    def setUp(self):
        """Set up test cases"""
        self.agent = ResearchAgent()
    
    @patch('src.agents.content.ResearchAgent._llm_call')
    def test_api_error_handling(self, mock_llm):
        """Test API error handling"""
        mock_llm.side_effect = Exception("API Error")
        result = self.agent.run("Research topic")
        self.assertEqual(result['status'], 'error')
        self.assertIn('error', result)
    
    @patch('src.agents.content.ResearchAgent._llm_call')
    def test_retry_mechanism(self, mock_llm):
        """Test retry mechanism"""
        mock_llm.side_effect = [Exception("Error"), Exception("Error"), "success"]
        result = self.agent.run("Research topic")
        self.assertEqual(result['status'], 'success')
        self.assertEqual(mock_llm.call_count, 3)

if __name__ == '__main__':
    unittest.main() 