"""
Example usage of research and content generation workflows
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.workflows import ResearchWorkflow, ContentWorkflow

# Load environment variables
load_dotenv()

def run_research_workflow():
    """Example of research workflow"""
    # Initialize research workflow
    research = ResearchWorkflow(
        model_name="llama-3.1-8b-instant",
        temperature=0.7
    )
    
    # Execute research on a topic
    results = research.execute_research("AI Safety and Ethics")
    
    print("\nResearch Results:")
    print("----------------")
    print(f"Topic: {results['topic']}")
    print("\nWeb Research:")
    print(results['web_research'])
    print("\nAnalysis:")
    print(results['analysis'])
    print("\nSynthesis:")
    print(results['synthesis'])

def run_content_workflow():
    """Example of content generation workflow"""
    # Initialize content workflow
    content = ContentWorkflow(
        model_name="llama-3.1-8b-instant",
        temperature=0.7
    )
    
    # Generate content
    article = content.generate_content(
        topic="The Future of AI",
        style="technical blog post"
    )
    
    print("\nContent Generation Results:")
    print("-------------------------")
    print(f"Topic: {article['topic']}")
    print(f"Style: {article['style']}")
    print("\nResearch:")
    print(article['research'])
    print("\nDraft:")
    print(article['draft'])
    print("\nFinal Content:")
    print(article['final_content'])

if __name__ == "__main__":
    # Ensure GROQ API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("Please set GROQ_API_KEY environment variable")
        exit(1)
    
    print("Running Research Workflow...")
    run_research_workflow()
    
    print("\nRunning Content Generation Workflow...")
    run_content_workflow() 