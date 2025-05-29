"""
Core RAG System Implementation
Combines document retrieval with LLM generation using free APIs.
"""

import os
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path
import gc
import psutil

# Import our components
from vector_store import ChromaVectorStore
from document_processor import DocumentProcessor, DocumentChunk

# LLM imports
try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from dotenv import load_dotenv
load_dotenv()

@dataclass
class RAGResponse:
    answer: str
    sources: List[Dict[str, Any]]
    query: str
    model_used: str
    retrieval_time: float
    generation_time: float

class RAGSystem:
    def __init__(self,
                 vector_store_path: str = "./chroma_db",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        Initialize RAG system with free components.
        
        Args:
            vector_store_path: Path to ChromaDB storage
            chunk_size: Size of document chunks
            chunk_overlap: Overlap between chunks
        """
        self.vector_store_path = vector_store_path
        
        # Initialize components
        self.vector_store = ChromaVectorStore(persist_directory=vector_store_path)
        self.document_processor = DocumentProcessor(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Initialize LLM (prioritize free APIs)
        self.llm_client = None
        self.llm_provider = None
        self._initialize_llm()
        
        print(f"🤖 RAG System initialized with {self.llm_provider} LLM")
    
    def _initialize_llm(self):
        """Initialize LLM client with available free APIs."""
        # Try Groq first (fastest free API)
        if os.getenv("GROQ_API_KEY") and Groq:
            try:
                self.llm_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                self.llm_provider = "groq"
                self.llm_model = "allam-2-7b"
                return
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
        
        # Try Google AI Studio
        if os.getenv("GOOGLE_AI_API_KEY") and genai:
            try:
                genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
                self.llm_client = genai.GenerativeModel('gemini-pro')
                self.llm_provider = "google-ai"
                self.llm_model = "gemini-pro"
                return
            except Exception as e:
                print(f"⚠️ Google AI initialization failed: {e}")
        
        # Fallback error
        raise ValueError(
            "No LLM API configured! Please set up at least one of:\n"
            "- GROQ_API_KEY (recommended - fastest)\n"
            "- GOOGLE_AI_API_KEY (good alternative)\n"
            "\nGet free API keys from:\n"
            "- Groq: https://console.groq.com/keys\n"
            "- Google AI: https://makersuite.google.com/app/apikey"
        )
    
    def ingest_documents(self, documents_path: str) -> Dict[str, Any]:
        """Ingest documents with memory management."""
        try:
            start_time = time.time()
            print(f"📄 Starting document ingestion from: {documents_path}")
            
            # Process documents in smaller batches if needed
            chunks = []
            batch_size = 10  # Process 10 files at a time
            
            # Get all files
            all_files = list(Path(documents_path).rglob("*"))
            supported_files = [f for f in all_files if f.suffix.lower() in self.document_processor.supported_extensions]
            
            for i in range(0, len(supported_files), batch_size):
                batch_files = supported_files[i:i + batch_size]
                print(f"Processing batch {i//batch_size + 1}/{(len(supported_files)-1)//batch_size + 1}")
                
                # Process batch
                batch_chunks = []
                for file_path in batch_files:
                    try:
                        file_chunks = self.document_processor.process_file(str(file_path))
                        batch_chunks.extend(file_chunks)
                    except Exception as e:
                        print(f"Error processing {file_path.name}: {e}")
                        continue
                
                chunks.extend(batch_chunks)
                
                # Force garbage collection between batches
                gc.collect()
                
                # Check memory usage
                memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                if memory_usage > 1000:  # If using more than 1GB
                    print(f"High memory usage detected: {memory_usage:.2f}MB. Cleaning up...")
                    gc.collect()
            
            if not chunks:
                print("⚠️ No documents found or processed!")
                return {"status": "no_documents", "chunks_created": 0}
            
            # Prepare data for vector store
            texts = [chunk.content for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            ids = [chunk.chunk_id for chunk in chunks]
            
            # Add to vector store in batches
            batch_size = 100  # Smaller batch size for vector store
            for i in range(0, len(texts), batch_size):
                batch_end = min(i + batch_size, len(texts))
                self.vector_store.add_documents(
                    texts[i:batch_end],
                    metadatas[i:batch_end],
                    ids[i:batch_end]
                )
                print(f"Added batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1} to vector store")
            
            processing_time = time.time() - start_time
            
            stats = {
                "status": "success",
                "chunks_created": len(chunks),
                "processing_time": processing_time,
                "vector_store_stats": self.vector_store.get_stats()
            }
            
            print(f"✅ Ingestion complete! {len(chunks)} chunks in {processing_time:.2f}s")
            return stats
            
        except Exception as e:
            print(f"❌ Error during ingestion: {e}")
            raise
    
    def query(self, 
              question: str,
              k: int = 4,
              include_sources: bool = True) -> RAGResponse:
        """
        Answer a question using RAG.
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            include_sources: Whether to include source information
            
        Returns:
            RAG response with answer and sources
        """
        import time
        
        # Step 1: Retrieve relevant documents
        retrieval_start = time.time()
        relevant_docs = self.vector_store.similarity_search(question, k=k)
        retrieval_time = time.time() - retrieval_start
        
        if not relevant_docs:
            return RAGResponse(
                answer="I couldn't find any relevant information to answer your question.",
                sources=[],
                query=question,
                model_used=f"{self.llm_provider}:{self.llm_model}",
                retrieval_time=retrieval_time,
                generation_time=0.0
            )
        
        # Step 2: Generate answer using LLM
        generation_start = time.time()
        answer = self._generate_answer(question, relevant_docs)
        generation_time = time.time() - generation_start
        
        # Step 3: Prepare sources
        sources = []
        if include_sources:
            for doc in relevant_docs:
                sources.append({
                    'content': doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content'],
                    'source': doc['metadata'].get('filename', 'Unknown'),
                    'similarity': doc['similarity'],
                    'chunk_id': doc['id']
                })
        
        return RAGResponse(
            answer=answer,
            sources=sources,
            query=question,
            model_used=f"{self.llm_provider}:{self.llm_model}",
            retrieval_time=retrieval_time,
            generation_time=generation_time
        )
    
    def _generate_answer(self, question: str, relevant_docs: List[Dict]) -> str:
        """Generate answer using LLM with retrieved context."""
        
        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1}: {doc['content']}" 
            for i, doc in enumerate(relevant_docs)
        ])
        
        # Create prompt
        prompt = f"""Based on the following context documents, please answer the user's question. 
If the answer cannot be found in the context, say so clearly.

Context:
{context}

Question: {question}

Answer: Provide a clear, concise answer based solely on the information in the context documents above."""
        
        # Generate response based on provider
        if self.llm_provider == "groq":
            return self._groq_generate(prompt)
        elif self.llm_provider == "google-ai":
            return self._gemini_generate(prompt)
        else:
            return "Error: No LLM provider available"
    
    def _groq_generate(self, prompt: str) -> str:
        """Generate response using Groq API."""
        try:
            chat_completion = self.llm_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                model=self.llm_model,
                temperature=0.1,
                max_tokens=1000
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response with Groq: {str(e)}"
    
    def _gemini_generate(self, prompt: str) -> str:
        """Generate response using Google Gemini API."""
        try:
            response = self.llm_client.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response with Gemini: {str(e)}"
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        vector_stats = self.vector_store.get_stats()
        
        return {
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "vector_store": vector_stats,
            "document_processor": {
                "chunk_size": self.document_processor.chunk_size,
                "chunk_overlap": self.document_processor.chunk_overlap,
                "supported_formats": list(self.document_processor.supported_extensions.keys())
            }
        }

if __name__ == "__main__":
    # Test the RAG system
    rag = RAGSystem()
    
    # Test with sample documents
    print("🧪 Testing RAG system...")
    
    # Create sample documents
    os.makedirs("test_data", exist_ok=True)
    
    sample_docs = {
        "ai_basics.txt": """
        Artificial Intelligence (AI) is a branch of computer science that aims to create 
        intelligent machines that can perform tasks that typically require human intelligence.
        These tasks include learning, reasoning, problem-solving, perception, and language understanding.
        
        Machine Learning is a subset of AI that enables computers to learn and improve from 
        experience without being explicitly programmed.
        """,
        "python_info.txt": """
        Python is a high-level, interpreted programming language known for its simplicity 
        and readability. It was created by Guido van Rossum and first released in 1991.
        
        Python is widely used for web development, data science, artificial intelligence,
        automation, and many other applications.
        """
    }
    
    # Create test files
    for filename, content in sample_docs.items():
        with open(f"test_data/{filename}", "w") as f:
            f.write(content)
    
    # Ingest documents
    stats = rag.ingest_documents("test_data")
    print(f"📊 Ingestion stats: {stats}")
    
    # Test queries
    test_queries = [
        "What is artificial intelligence?",
        "Who created Python?",
        "What is machine learning?"
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        response = rag.query(query)
        print(f"🤖 Answer: {response.answer}")
        print(f"⏱️ Retrieval: {response.retrieval_time:.3f}s, Generation: {response.generation_time:.3f}s") 