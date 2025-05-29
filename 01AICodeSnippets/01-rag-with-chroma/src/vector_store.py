"""
ChromaDB Vector Store Implementation
Handles embedding storage and similarity search using free tools.
"""

import chromadb
import os
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path

class ChromaVectorStore:
    def __init__(self, 
                 persist_directory: str = "./chroma_db",
                 collection_name: str = "rag_documents",
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize ChromaDB vector store with free embedding model.
        
        Args:
            persist_directory: Where to store the database
            collection_name: Name of the collection
            embedding_model: Free sentence transformer model
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize free embedding model
        print(f"🔄 Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        print(f"✅ ChromaDB initialized with {self.collection.count()} documents")
    
    def add_documents(self, 
                     texts: List[str], 
                     metadatas: List[Dict[str, Any]],
                     ids: Optional[List[str]] = None) -> None:
        """
        Add documents to the vector store.
        
        Args:
            texts: List of document texts to embed
            metadatas: List of metadata dictionaries
            ids: Optional list of document IDs
        """
        if not texts:
            return
        
        # Generate embeddings using free model
        print(f"🔄 Generating embeddings for {len(texts)} documents...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Generate IDs if not provided
        if ids is None:
            existing_count = self.collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(texts))]
        
        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Added {len(texts)} documents to vector store")
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 4,
                         filter_metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of similar documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=k,
            where=filter_metadata
        )
        
        # Format results
        documents = []
        for i in range(len(results['documents'][0])):
            documents.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                'id': results['ids'][0][i]
            })
        
        return documents
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.collection_name,
            'embedding_model': self.embedding_model.get_sentence_embedding_dimension(),
            'persist_directory': self.persist_directory
        }
    
    def delete_collection(self):
        """Delete the entire collection."""
        self.client.delete_collection(self.collection_name)
        print(f"🗑️ Deleted collection: {self.collection_name}")

if __name__ == "__main__":
    # Test the vector store
    vector_store = ChromaVectorStore()
    
    # Add sample documents
    sample_texts = [
        "The capital of France is Paris.",
        "Python is a programming language.",
        "Machine learning is a subset of artificial intelligence."
    ]
    
    sample_metadata = [
        {"source": "geography.txt", "topic": "geography"},
        {"source": "programming.txt", "topic": "programming"}, 
        {"source": "ai.txt", "topic": "artificial_intelligence"}
    ]
    
    vector_store.add_documents(sample_texts, sample_metadata)
    
    # Test search
    results = vector_store.similarity_search("What is the capital of France?", k=2)
    
    print("\n🔍 Search Results:")
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc['content'][:100]}... (similarity: {doc['similarity']:.3f})") 