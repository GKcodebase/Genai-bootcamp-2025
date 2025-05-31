"""
Example usage of the Research RAG Agent
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from src.agents import ResearchRAGAgent
from src.retrieval import ChromaDocStore, DocumentProcessor

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize document processor and load documents
    processor = DocumentProcessor()
    documents = processor.load_directory("data/sample_documents")
    
    # Initialize vector store and add documents
    store = ChromaDocStore()
    store.add_documents(documents)
    
    # Create research agent
    agent = ResearchRAGAgent(
        vector_store=store,
        model_name="llama-3.1-8b-instant",
        temperature=0.7
    )
    
    # Example research queries
    queries = [
        "What are the main challenges in AI safety?",
        "How does deep learning compare to traditional machine learning?",
        "What are the ethical considerations in AI development?"
    ]
    
    # Run queries and display results
    for query in queries:
        print(f"\n=== Researching: {query} ===")
        result = agent.run(query)
        
        print("\nResponse:")
        print(result["output"])
        
        if result.get("sources"):
            print("\nSources:")
            for source in result["sources"]:
                print(f"- {source}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main() 