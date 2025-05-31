"""
Document processing utilities for RAG system
"""

import os
from typing import List, Optional
from langchain_community.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentProcessor:
    """Process and chunk documents for RAG system"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def load_documents(self, file_path: str) -> List[Document]:
        """Load documents based on file type"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PDFMinerLoader(file_path)
        elif file_extension == '.txt':
            loader = TextLoader(file_path)
        elif file_extension in ['.md', '.markdown']:
            loader = UnstructuredMarkdownLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        documents = loader.load()
        return self.split_documents(documents)
    
    def load_directory(
        self,
        directory_path: str,
        glob_pattern: Optional[str] = None
    ) -> List[Document]:
        """Load all documents from a directory"""
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")
        
        all_documents = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.pdf', '.txt', '.md', '.markdown')):
                    file_path = os.path.join(root, file)
                    try:
                        docs = self.load_documents(file_path)
                        all_documents.extend(docs)
                    except Exception as e:
                        print(f"Error loading {file_path}: {str(e)}")
        
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)
    
    def process_text(self, text: str) -> List[Document]:
        """Process raw text into documents"""
        return self.text_splitter.create_documents([text]) 