"""
Tests for workflow implementations
"""

import unittest
from unittest.mock import patch, MagicMock
from src.workflows import ResearchWorkflow, ContentWorkflow

class TestResearchWorkflow(unittest.TestCase):
    """Test cases for research workflow"""
    
    def setUp(self):
        """Set up test cases"""
        self.workflow = ResearchWorkflow(
            model_name="test-model",
            temperature=0.7
        )
    
    @patch('src.agents.research.WebResearchAgent.run')
    @patch('src.agents.research.DocumentAnalysisAgent.run')
    @patch('src.agents.research.SynthesisAgent.run')
    def test_execute_research(self, mock_synthesis, mock_analysis, mock_web):
        """Test research workflow execution"""
        # Mock agent responses
        mock_web.return_value = {
            'status': 'success',
            'results': ['result1', 'result2'],
            'sources': ['source1']
        }
        mock_analysis.return_value = {
            'status': 'success',
            'concepts': ['concept1'],
            'insights': ['insight1']
        }
        mock_synthesis.return_value = {
            'status': 'success',
            'synthesis': 'Final synthesis',
            'summary': {'key': 'value'}
        }
        
        # Execute workflow
        result = self.workflow.execute_research("Test Topic")
        
        # Verify results
        self.assertIn('web_research', result)
        self.assertIn('analysis', result)
        self.assertIn('synthesis', result)
        
        # Verify agent calls
        mock_web.assert_called_once()
        mock_analysis.assert_called_once()
        mock_synthesis.assert_called_once()
    
    def test_error_handling(self):
        """Test workflow error handling"""
        with patch('src.agents.research.WebResearchAgent.run') as mock_web:
            mock_web.return_value = {
                'status': 'error',
                'error': 'Test error'
            }
            result = self.workflow.execute_research("Test Topic")
            self.assertIn('error', result)

class TestContentWorkflow(unittest.TestCase):
    """Test cases for content generation workflow"""
    
    def setUp(self):
        """Set up test cases"""
        self.workflow = ContentWorkflow(
            model_name="test-model",
            temperature=0.7
        )
    
    @patch('src.agents.content.ResearchAgent.run')
    @patch('src.agents.content.WritingAgent.run')
    @patch('src.agents.content.EditingAgent.run')
    def test_generate_content(self, mock_edit, mock_write, mock_research):
        """Test content generation workflow"""
        # Mock agent responses
        mock_research.return_value = {
            'status': 'success',
            'research': 'Research results',
            'sources': ['source1']
        }
        mock_write.return_value = {
            'status': 'success',
            'draft': 'Content draft',
            'outline': 'Content outline'
        }
        mock_edit.return_value = {
            'status': 'success',
            'final_content': 'Final content',
            'edits_made': {'summary': 'changes made'}
        }
        
        # Execute workflow
        result = self.workflow.generate_content(
            topic="Test Topic",
            style="test style"
        )
        
        # Verify results
        self.assertIn('research', result)
        self.assertIn('draft', result)
        self.assertIn('final_content', result)
        
        # Verify agent calls
        mock_research.assert_called_once()
        mock_write.assert_called_once()
        mock_edit.assert_called_once()
    
    def test_style_validation(self):
        """Test content style validation"""
        with self.assertRaises(ValueError):
            self.workflow.generate_content(
                topic="Test Topic",
                style=""  # Empty style should raise error
            )
    
    def test_error_propagation(self):
        """Test error propagation in workflow"""
        with patch('src.agents.content.ResearchAgent.run') as mock_research:
            mock_research.return_value = {
                'status': 'error',
                'error': 'Research failed'
            }
            result = self.workflow.generate_content(
                topic="Test Topic",
                style="test style"
            )
            self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main() 