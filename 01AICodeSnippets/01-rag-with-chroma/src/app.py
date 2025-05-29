"""
RAG Chat Application with Gradio Interface
A user-friendly interface for the RAG system using completely free tools.
"""

import gradio as gr
import os
from pathlib import Path
import json
import time
from typing import List, Tuple
import shutil
import signal
import sys

from rag_system import RAGSystem, RAGResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGChatApp:
    def __init__(self):
        """Initialize the RAG chat application."""
        self.rag_system = None
        self.chat_history = []
        
        # Check if vector store exists
        self.vector_store_path = "./chroma_db"
        self.has_documents = self._check_existing_documents()
        
        # Create upload directory
        self.upload_dir = Path("./uploaded_docs")
        self.upload_dir.mkdir(exist_ok=True)
        
        print(f"🚀 RAG Chat App initialized")
        print(f"📊 Documents in vector store: {self.has_documents}")
    
    def _check_existing_documents(self) -> bool:
        """Check if there are existing documents in the vector store."""
        try:
            from vector_store import ChromaVectorStore
            temp_store = ChromaVectorStore(persist_directory=self.vector_store_path)
            count = temp_store.collection.count()
            return count > 0
        except Exception:
            return False
    
    def initialize_rag_system(self):
        """Initialize RAG system with error handling."""
        try:
            if self.rag_system is None:
                self.rag_system = RAGSystem(vector_store_path=self.vector_store_path)
            return True, "✅ RAG system initialized successfully!"
        except Exception as e:
            return False, f"❌ Error initializing RAG system: {str(e)}"
    
    def upload_documents(self, files) -> Tuple[str, str]:
        """Handle document upload and processing with improved error handling."""
        if not files:
            return "⚠️ No files uploaded.", ""
        
        try:
            # Initialize RAG system if needed
            success, message = self.initialize_rag_system()
            if not success:
                return message, ""
            
            # Save uploaded files
            uploaded_files = []
            skipped_files = []
            
            for file in files:
                if file is not None:
                    try:
                        # Check file size (limit to 50MB)
                        if os.path.getsize(file.name) > 50 * 1024 * 1024:
                            skipped_files.append(f"{file.name} (too large)")
                            continue
                        
                        file_path = self.upload_dir / Path(file.name).name
                        # Use shutil to copy file safely
                        shutil.copy2(file.name, file_path)
                        uploaded_files.append(str(file_path))
                    except Exception as e:
                        skipped_files.append(f"{file.name} (error: {str(e)})")
            
            if not uploaded_files:
                return "⚠️ No valid files found to process.", ""
            
            # Process documents with proper cleanup and progress updates
            try:
                print(f"Processing {len(uploaded_files)} files...")
                stats = self.rag_system.ingest_documents(str(self.upload_dir))
                self.has_documents = True
                
                # Format result message
                result_message = f"""✅ Document Processing Complete!
                
📊 Statistics:
• Files processed successfully: {len(uploaded_files)}
• Files skipped: {len(skipped_files)}
• Chunks created: {stats.get('chunks_created', 0)}
• Processing time: {stats.get('processing_time', 0):.2f}s
• Total documents in store: {stats.get('vector_store_stats', {}).get('total_documents', 0)}

"""
                # Add skipped files information if any
                if skipped_files:
                    result_message += "\n⚠️ Skipped files:\n" + "\n".join(f"- {f}" for f in skipped_files)
                
                result_message += "\n🎉 You can now start asking questions!"
                
                return result_message, "Documents processed successfully! Ask your first question below."
                
            except Exception as e:
                return f"❌ Error processing documents: {str(e)}", ""
                
            finally:
                # Clean up uploaded files after processing
                for file_path in uploaded_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Warning: Could not remove temporary file {file_path}: {e}")
                    
        except Exception as e:
            return f"❌ Error during upload: {str(e)}", ""
    
    def chat(self, message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
        """Handle chat interactions."""
        if not message.strip():
            return "", history
        
        try:
            # Initialize RAG system if needed
            if self.rag_system is None:
                success, init_message = self.initialize_rag_system()
                if not success:
                    history.append([message, init_message])
                    return "", history
            
            # Check if documents are available
            if not self.has_documents:
                response = "⚠️ No documents have been uploaded yet. Please upload some documents first to enable Q&A."
                history.append([message, response])
                return "", history
            
            # Get response from RAG system
            rag_response = self.rag_system.query(message, k=4)
            
            # Format response with sources
            formatted_response = self._format_response(rag_response)
            
            # Add to history
            history.append([message, formatted_response])
            
            return "", history
            
        except Exception as e:
            error_response = f"❌ Error processing your question: {str(e)}"
            history.append([message, error_response])
            return "", history
    
    def _format_response(self, rag_response: RAGResponse) -> str:
        """Format the RAG response for display."""
        response_parts = [
            f"🤖 **Answer:**\n{rag_response.answer}"
        ]
        
        if rag_response.sources:
            response_parts.append("\n📚 **Sources:**")
            for i, source in enumerate(rag_response.sources, 1):
                similarity_bar = "🟢" if source['similarity'] > 0.8 else "🟡" if source['similarity'] > 0.6 else "🟠"
                response_parts.append(
                    f"{i}. {similarity_bar} **{source['source']}** (similarity: {source['similarity']:.3f})\n"
                    f"   _{source['content']}_"
                )
        
        response_parts.append(
            f"\n⏱️ *Retrieval: {rag_response.retrieval_time:.3f}s | "
            f"Generation: {rag_response.generation_time:.3f}s | "
            f"Model: {rag_response.model_used}*"
        )
        
        return "\n".join(response_parts)
    
    def get_system_info(self) -> str:
        """Get system information for display."""
        try:
            if self.rag_system is None:
                success, message = self.initialize_rag_system()
                if not success:
                    return f"System not initialized: {message}"
            
            stats = self.rag_system.get_system_stats()
            
            info = f"""🔧 **System Information**

**LLM Provider:** {stats['llm_provider']} ({stats['llm_model']})
**Vector Store:** ChromaDB with {stats['vector_store']['total_documents']} documents
**Embedding Model:** {stats['vector_store']['embedding_model']} dimensions
**Chunk Size:** {stats['document_processor']['chunk_size']} characters
**Supported Formats:** {', '.join(stats['document_processor']['supported_formats'])}

**Status:** {'✅ Ready' if self.has_documents else '⚠️ No documents uploaded'}"""
            
            return info
            
        except Exception as e:
            return f"❌ Error getting system info: {str(e)}"
    
    def clear_chat(self):
        """Clear chat history."""
        return []
    
    def create_interface(self):
        """Create the Gradio interface."""
        
        # Custom CSS for better styling
        css = """
        .gradio-container {
            max-width: 1200px !important;
        }
        .upload-container {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        """
        
        with gr.Blocks(title="🤖 RAG Chat - Free AI Assistant", css=css, theme=gr.themes.Soft()) as interface:
            
            gr.Markdown("""
            # 🤖 RAG Chat Assistant (Completely Free!)
            
            Upload your documents and chat with them using **free AI APIs**:
            - 🚀 **Groq API** for lightning-fast responses  
            - 🧠 **ChromaDB** for intelligent document search
            - 🔍 **Free embeddings** for semantic understanding
            
            ---
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        height=500,
                        label="💬 Chat with Your Documents",
                        placeholder="Upload documents first, then start asking questions!"
                    )
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            placeholder="Ask a question about your documents...",
                            label="Your Question",
                            scale=4
                        )
                        send_btn = gr.Button("Send 📤", scale=1, variant="primary")
                    
                    with gr.Row():
                        clear_btn = gr.Button("Clear Chat 🗑️", scale=1)
                
                with gr.Column(scale=1):
                    # Document upload section
                    gr.Markdown("### 📁 Upload Documents")
                    
                    file_upload = gr.Files(
                        label="Select Documents",
                        file_count="multiple",
                        file_types=[".txt", ".pdf", ".docx", ".md", ".html"]
                    )
                    
                    upload_btn = gr.Button("Process Documents 🔄", variant="secondary")
                    upload_status = gr.Textbox(label="Processing Status", lines=8, interactive=False)
                    
                    # System info section
                    gr.Markdown("### ⚙️ System Status")
                    system_info = gr.Textbox(
                        label="System Information",
                        lines=10,
                        interactive=False,
                        value=self.get_system_info()
                    )
                    
                    refresh_btn = gr.Button("Refresh Info 🔄")
            
            # Example questions
            gr.Markdown("""
            ### 💡 Example Questions
            - "What are the main topics covered in these documents?"
            - "Can you summarize the key points?"
            - "What does the document say about [specific topic]?"
            """)
            
            # Event handlers
            send_btn.click(
                self.chat,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            msg.submit(
                self.chat,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            upload_btn.click(
                self.upload_documents,
                inputs=[file_upload],
                outputs=[upload_status, msg]
            )
            
            clear_btn.click(
                self.clear_chat,
                outputs=[chatbot]
            )
            
            refresh_btn.click(
                self.get_system_info,
                outputs=[system_info]
            )
            
            # Load existing documents message
            if self.has_documents:
                gr.Markdown("✅ **Existing documents found!** You can start asking questions immediately.")
            else:
                gr.Markdown("📤 **Upload documents above to get started.**")
        
        return interface

    def __del__(self):
        """Cleanup resources when the app is closed."""
        try:
            # Clean up temporary upload directory
            shutil.rmtree(self.upload_dir, ignore_errors=True)
            
            # Close ChromaDB client if exists
            if self.rag_system and self.rag_system.vector_store:
                self.rag_system.vector_store.client._client.close()
        except Exception as e:
            print(f"Warning: Cleanup error: {e}")

def main():
    """Main function to run the application."""
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check environment setup
    required_env_vars = ["GROQ_API_KEY", "GOOGLE_AI_API_KEY"]
    available_apis = [var for var in required_env_vars if os.getenv(var)]
    
    if not available_apis:
        print("❌ No API keys found!")
        print("Please set up at least one free API key:")
        print("- GROQ_API_KEY: Get from https://console.groq.com/keys")
        print("- GOOGLE_AI_API_KEY: Get from https://makersuite.google.com/app/apikey")
        return
    
    print(f"✅ Found API keys: {available_apis}")
    
    try:
        # Create and launch app
        app = RAGChatApp()
        interface = app.create_interface()
        
        print("🚀 Starting RAG Chat Application...")
        print("💡 Open http://localhost:7860 in your browser")
        
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,  # Set to True if you want a public link
            show_error=True
        )
    finally:
        # Cleanup on exit
        if 'app' in locals():
            del app

if __name__ == "__main__":
    main() 