"""
ChromaDB vector store implementation
"""

import os
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class ChromaDocStore:
    """ChromaDB document store with embedding capabilities"""
    
    def __init__(self, persist_dir="./data/chroma_db"):
        """Initialize the Chroma document store"""
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
        )
        self.store = self._create_store()
    
    def _create_store(self):
        """Create or load the Chroma store"""
        if os.path.exists(self.persist_dir):
            import shutil
            shutil.rmtree(self.persist_dir)
            
        return Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )
    
    def add_documents(self, documents):
        """Add documents to the store"""
        self.store.add_documents(documents)
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        **kwargs
    ) -> List[Document]:
        """Search for similar documents"""
        return self.store.similarity_search(
            query,
            k=k,
            **kwargs
        )
    
    def delete_collection(self) -> None:
        """Delete the current collection"""
        if hasattr(self.store, '_persist_directory'):
            import shutil
            shutil.rmtree(self.persist_dir) 