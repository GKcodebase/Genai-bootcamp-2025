import chromadb
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

class RAGSystem:
    def __init__(self, collection_name: str = "jlptn5-listening-comprehension"):
        """Initialize RAG system with ChromaDB"""
        # Create persistent client with specific path
        self.client = chromadb.PersistentClient(path="backend/data/chromadb")
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(collection_name)
        
    def load_processed_documents(self, base_path: str = "../backend/data/questions") -> bool:
        """Load processed documents from the questions directory"""
        try:
            documents = []
            metadatas = []
            ids = []
            
            # Clear existing documents
            try:
                self.collection.delete(where={})
            except Exception as e:
                print(f"Warning when clearing collection: {str(e)}")
            
            # Walk through the questions directory
            if not os.path.exists(base_path):
                print(f"Questions directory not found: {base_path}")
                return False
                
            for filename in os.listdir(base_path):
                if filename.endswith(".txt"):
                    file_path = os.path.join(base_path, filename)
                    
                    # Extract video_id and section from filename
                    video_id = filename.split('_section')[0]
                    section = filename.split('_section')[1].split('.')[0]
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Split content into individual questions
                        questions = content.split('<question>')
                        
                        for i, question in enumerate(questions):
                            if question.strip():  # Skip empty questions
                                documents.append(question.strip())
                                metadatas.append({
                                    "video_id": video_id,
                                    "section": section,
                                    "question_num": i
                                })
                                ids.append(f"{video_id}_s{section}_q{i}")
            
            # Add documents to collection if any were found
            if documents:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Added {len(documents)} documents to collection")
                return True
            else:
                print("No documents found to load")
                return False
                
        except Exception as e:
            print(f"Error loading documents: {str(e)}")
            return False
    
    def query_similar(self, query_text: str, n_results: int = 3) -> Optional[Dict]:
        """Query similar documents"""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error querying documents: {str(e)}")
            return None

if __name__ == "__main__":
    # Test the RAG system
    rag = RAGSystem()
    
    # Load processed documents
    if rag.load_processed_documents():
        print("Documents loaded successfully!")
        
        # Test query
        results = rag.query_similar("What time is the meeting?")
        if results:
            print("\nQuery Results:")
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                print(f"\nResult {i+1}:")
                print(f"Document: {doc[:200]}...")  # Print first 200 chars
                print(f"Metadata: {metadata}")