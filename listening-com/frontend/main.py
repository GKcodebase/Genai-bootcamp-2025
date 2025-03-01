import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.get_transcript import YouTubeTranscriptDownloader
import streamlit as st
from typing import Dict
import json
from collections import Counter
import re

from backend.chat import BedrockChat
from backend.structured_data import TranscriptStructurer  # Add this import at the top
from backend.rag import RAGSystem

# Page config
st.set_page_config(
    page_title="Japanese Learning Assistant",
    page_icon="🎌",
    layout="wide"
)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'structured_sections' not in st.session_state:
    st.session_state.structured_sections = None
if 'bedrock_chat' not in st.session_state:
    st.session_state.bedrock_chat = BedrockChat()
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = RAGSystem()
if 'video_id' not in st.session_state:
    st.session_state.video_id = None

def render_header():
    """Render the header section"""
    st.title("🎌 Japanese Learning Assistant")
    st.markdown("""
    Transform YouTube transcripts into interactive Japanese learning experiences.
    
    This tool demonstrates:
    - Base LLM Capabilities
    - RAG (Retrieval Augmented Generation)
    - Amazon Bedrock Integration
    - Agent-based Learning Systems
    """)

def render_sidebar():
    """Render the sidebar with component selection"""
    with st.sidebar:
        st.header("Development Stages")
        
        # Main component selection
        selected_stage = st.radio(
            "Select Stage:",
            [
                "1. Chat with Nova",
                "2. Raw Transcript",
                "3. Structured Data",
                "4. RAG Implementation",
                "5. Interactive Learning"
            ]
        )
        
        # Stage descriptions
        stage_info = {
            "1. Chat with Nova": """
            **Current Focus:**
            - Basic Japanese learning
            - Understanding LLM capabilities
            - Identifying limitations
            """,
            
            "2. Raw Transcript": """
            **Current Focus:**
            - YouTube transcript download
            - Raw text visualization
            - Initial data examination
            """,
            
            "3. Structured Data": """
            **Current Focus:**
            - Text cleaning
            - Dialogue extraction
            - Data structuring
            """,
            
            "4. RAG Implementation": """
            **Current Focus:**
            - Bedrock embeddings
            - Vector storage
            - Context retrieval
            """,
            
            "5. Interactive Learning": """
            **Current Focus:**
            - Scenario generation
            - Audio synthesis
            - Interactive practice
            """
        }
        
        st.markdown("---")
        st.markdown(stage_info[selected_stage])
        
        return selected_stage

def render_chat_stage():
    """Render an improved chat interface"""
    st.header("Chat with Nova")

    # Initialize BedrockChat instance if not in session state
    if 'bedrock_chat' not in st.session_state:
        st.session_state.bedrock_chat = BedrockChat()

    # Introduction text
    st.markdown("""
    Start by exploring Nova's base Japanese language capabilities. Try asking questions about Japanese grammar, 
    vocabulary, or cultural aspects.
    """)

    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

    # Chat input area
    if prompt := st.chat_input("Ask about Japanese language..."):
        # Process the user input
        process_message(prompt)

    # Example questions in sidebar
    with st.sidebar:
        st.markdown("### Try These Examples")
        example_questions = [
            "How do I say 'Where is the train station?' in Japanese?",
            "Explain the difference between は and が",
            "What's the polite form of 食べる?",
            "How do I count objects in Japanese?",
            "What's the difference between こんにちは and こんばんは?",
            "How do I ask for directions politely?"
        ]
        
        for q in example_questions:
            if st.button(q, use_container_width=True, type="secondary"):
                # Process the example question
                process_message(q)
                st.rerun()

    # Add a clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()

def process_message(message: str):
    """Process a message and generate a response"""
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(message)

    # Generate and display assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        response = st.session_state.bedrock_chat.generate_response(message)
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})



def count_characters(text):
    """Count Japanese and total characters in text"""
    if not text:
        return 0, 0
        
    def is_japanese(char):
        return any([
            '\u4e00' <= char <= '\u9fff',  # Kanji
            '\u3040' <= char <= '\u309f',  # Hiragana
            '\u30a0' <= char <= '\u30ff',  # Katakana
        ])
    
    jp_chars = sum(1 for char in text if is_japanese(char))
    return jp_chars, len(text)

def render_transcript_stage():
    """Render the raw transcript stage"""
    st.header("Raw Transcript Processing")
    
    # URL input
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a Japanese lesson YouTube URL"
    )
    
    # Download button and processing
    if url:
        if st.button("Download Transcript"):
            try:
                downloader = YouTubeTranscriptDownloader()
                # Extract video ID from URL
                video_id = downloader.extract_video_id(url)
                if not video_id:
                    st.error("Could not extract video ID from URL")
                    return

                transcript = downloader.get_transcript(url)
                if transcript:
                    # Store the raw transcript text and video_id in session state
                    transcript_text = "\n".join([entry['text'] for entry in transcript])
                    st.session_state.transcript = transcript_text
                    st.session_state.video_id = video_id  # Store video_id in session state
                    
                    # Save the transcript to file
                    if downloader.save_transcript(transcript, video_id):
                        st.success(f"Transcript downloaded and saved successfully! Video ID: {video_id}")
                    else:
                        st.error("Failed to save transcript to file")
                else:
                    st.error("No transcript found for this video.")
            except Exception as e:
                st.error(f"Error downloading transcript: {str(e)}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Raw Transcript")
        if st.session_state.transcript:
            st.text_area(
                label="Raw text",
                value=st.session_state.transcript,
                height=400,
                disabled=True
            )
    
        else:
            st.info("No transcript loaded yet")
    
    with col2:
        st.subheader("Transcript Stats")
        if st.session_state.transcript:
            # Calculate stats
            jp_chars, total_chars = count_characters(st.session_state.transcript)
            total_lines = len(st.session_state.transcript.split('\n'))
            
            # Display stats
            st.metric("Total Characters", total_chars)
            st.metric("Japanese Characters", jp_chars)
            st.metric("Total Lines", total_lines)
        else:
            st.info("Load a transcript to see statistics")

def render_structured_stage():
    """Render the structured data stage"""
    st.header("Structured Data Processing")
    
    # Initialize TranscriptStructurer
    if 'structurer' not in st.session_state:
        st.session_state.structurer = TranscriptStructurer()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Raw Transcript")
        if st.session_state.transcript:
            st.text_area(
                label="Source text",
                value=st.session_state.transcript,
                height=300,
                disabled=True
            )
            
            if st.button("Process Transcript"):
                with st.spinner("Processing transcript..."):
                    try:
                        structured_sections = st.session_state.structurer.structure_transcript(
                            st.session_state.transcript
                        )
                        st.session_state.structured_sections = structured_sections
                        st.success("Transcript processed successfully!")
                    except Exception as e:
                        st.error(f"Error processing transcript: {str(e)}")
        else:
            st.info("Please load a transcript in the Raw Transcript stage first")
        
    with col2:
        st.subheader("Structured Output")
        if st.session_state.structured_sections:
            tabs = st.tabs(["Section 2", "Section 3"])
            
            for i, tab in enumerate(tabs):
                section_num = i + 2  # Since we're skipping section 1
                with tab:
                    if section_num in st.session_state.structured_sections:
                        st.text_area(
                            label=f"Section {section_num}",
                            value=st.session_state.structured_sections[section_num],
                            height=300,
                            disabled=True
                        )
                    else:
                        st.info(f"No content for Section {section_num}")
            
            # Save button
            if st.button("Save Structured Data"):
                try:
                    # Use the video_id from session state
                    video_id = st.session_state.video_id if st.session_state.video_id else "processed_transcript"
                    save_path = f"../backend/data/questions/{video_id}.txt"
                    if st.session_state.structurer.save_questions(
                        st.session_state.structured_sections, 
                        save_path
                    ):
                        st.success(f"Structured data saved successfully for video ID: {video_id}")
                    else:
                        st.error("Failed to save structured data")
                except Exception as e:
                    st.error(f"Error saving structured data: {str(e)}")
        else:
            st.info("Process a transcript to see structured output")

def render_rag_stage():
    """Render the RAG implementation stage"""
    st.header("Japanese Learning Assistant with RAG")
    
    # Load documents button
    if st.button("Load Processed Documents"):
        with st.spinner("Loading documents into RAG system..."):
            if st.session_state.rag_system.load_processed_documents():
                st.success("Documents loaded successfully!")
            else:
                st.error("Failed to load documents")
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Select Analysis Type",
        options=[
            "translate_to_english",
            "translate_to_japanese",
            "kanji_info",
            "language_analysis"
        ],
        format_func=lambda x: x.replace('_', ' ').title()
    )

    # Query input and button in columns
    col_query, col_button = st.columns([3, 1])
    
    with col_query:
        query = st.text_input(
            "Enter Text",
            placeholder="Enter Japanese or English text..."
        )
    
    with col_button:
        search_button = st.button("Analyze", type="primary", use_container_width=True)
    
    # Process query when button is clicked
    if search_button and query:
        with st.spinner("Analyzing and retrieving relevant content..."):
            # Get context from RAG system
            rag_results = st.session_state.rag_system.query_similar(query)
            
            # Initialize BedrockChat if not in session state
            if 'bedrock_chat' not in st.session_state:
                st.session_state.bedrock_chat = BedrockChat()
            
            # Generate response using Bedrock
            bedrock_response = st.session_state.bedrock_chat.generate_response(
                query, 
                response_type=analysis_type
            )
            
            # Display results in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Similar Content")
                if rag_results and rag_results['documents']:
                    for i, (doc, metadata) in enumerate(zip(
                        rag_results['documents'][0], 
                        rag_results['metadatas'][0]
                    )):
                        with st.expander(f"Reference {i+1}"):
                            st.markdown(doc)
                            st.markdown("**Metadata:**")
                            st.json(metadata)
                else:
                    st.info("No similar content found in the database")
                
            with col2:
                st.subheader("Analysis Results")
                if bedrock_response:
                    # Create tabs for different views
                    response_tab, context_tab = st.tabs(["Analysis", "Context"])
                    
                    with response_tab:
                        st.markdown(bedrock_response)
                    
                    with context_tab:
                        st.markdown("""
                        **Analysis Type:** {}
                        
                        **Query:** {}
                        """.format(
                            analysis_type.replace('_', ' ').title(),
                            query
                        ))
                else:
                    st.error("Failed to generate analysis")
    else:
        st.info("Enter text and click Analyze to start")

def render_interactive_stage():
    """Render the interactive learning stage"""
    st.header("Interactive Learning")
    
    # Practice type selection
    practice_type = st.selectbox(
        "Select Practice Type",
        ["Dialogue Practice", "Vocabulary Quiz", "Listening Exercise"]
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Practice Scenario")
        # Placeholder for scenario
        st.info("Practice scenario will appear here")
        
        # Placeholder for multiple choice
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        selected = st.radio("Choose your answer:", options)
        
    with col2:
        st.subheader("Audio")
        # Placeholder for audio player
        st.info("Audio will appear here")
        
        st.subheader("Feedback")
        # Placeholder for feedback
        st.info("Feedback will appear here")

def main():
    render_header()
    selected_stage = render_sidebar()
    
    # Render appropriate stage
    if selected_stage == "1. Chat with Nova":
        render_chat_stage()
    elif selected_stage == "2. Raw Transcript":
        render_transcript_stage()
    elif selected_stage == "3. Structured Data":
        render_structured_stage()
    elif selected_stage == "4. RAG Implementation":
        render_rag_stage()
    elif selected_stage == "5. Interactive Learning":
        render_interactive_stage()
    
    # Debug section at the bottom
    with st.expander("Debug Information"):
        st.json({
            "selected_stage": selected_stage,
            "transcript_loaded": st.session_state.transcript is not None,
            "chat_messages": len(st.session_state.messages)
        })

if __name__ == "__main__":
    main()