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
from backend.interactive import InteractiveLearning  # Add this import

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
if 'interactive_learning' not in st.session_state:
    st.session_state.interactive_learning = InteractiveLearning()

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
    
    # Initialize states
    if 'interactive_learning' not in st.session_state:
        st.session_state.interactive_learning = InteractiveLearning()
    if 'generated_question' not in st.session_state:
        st.session_state.generated_question = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    
    st.subheader("Generate Questions")
    
    # Topic input and section selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input(
            "Enter Topic",
            placeholder="e.g., shopping, restaurant, school, weather",
            key="generate_topic"
        )
    
    with col2:
        gen_section = st.selectbox(
            "Section",
            options=[2, 3],
            format_func=lambda x: f"Section {x}",
            key="generate_section"
        )
    
    # Generate button
    if st.button("Generate Question", type="primary"):
        if not topic:
            st.warning("Please enter a topic first")
        else:
            with st.spinner("Generating question..."):
                new_question = st.session_state.interactive_learning.generate_similar_question(
                    gen_section, topic
                )
                if new_question:
                    st.write("Generated question:", new_question)  # Debug print
                    st.session_state.generated_question = new_question
                    st.session_state.feedback = None
                    st.session_state.answer_submitted = False
                    st.success("Question generated successfully!")
                else:
                    st.error("Failed to generate question. Please try again.")
    
    # Display generated question and answer options
    if st.session_state.generated_question:
        with st.container():
            st.markdown("### Question")
            
            # Generate audio for the question if not already generated
            if 'audio_data' not in st.session_state:
                with st.spinner("Generating audio..."):
                    st.session_state.audio_data = st.session_state.interactive_learning.generate_audio_for_question(
                        st.session_state.generated_question
                    )
            
            # Display question content with audio controls
            if 'Introduction' in st.session_state.generated_question:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**Introduction:**")
                    st.write(st.session_state.generated_question['Introduction'])
                with col2:
                    if 'Introduction' in st.session_state.audio_data:
                        st.audio(st.session_state.audio_data['Introduction']['audio'])
                
                st.write("**Conversation:**")
                conversation_parts = st.session_state.generated_question['Conversation'].split('\n')
                for i, (part, audio) in enumerate(zip(conversation_parts, st.session_state.audio_data.get('Conversation', []))):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(part)
                    with col2:
                        st.audio(audio['audio'])
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**Situation:**")
                    st.write(st.session_state.generated_question['Situation'])
                with col2:
                    if 'Situation' in st.session_state.audio_data:
                        st.audio(st.session_state.audio_data['Situation']['audio'])
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Question:**")
                st.write(st.session_state.generated_question['Question'])
            with col2:
                if 'Question' in st.session_state.audio_data:
                    st.audio(st.session_state.audio_data['Question']['audio'])
            
            # Display options with audio
            st.write("**選択肢 (Options):**")
            options = st.session_state.generated_question['Options']
            options_audio = st.session_state.audio_data.get('Options', [])
            
            for i, (opt, audio) in enumerate(zip(options, options_audio), 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{i}. {opt}")
                with col2:
                    st.audio(audio['audio'])
            
            # Replace the radio button and feedback section with this updated code
            if 'Options' in st.session_state.generated_question:
                options = st.session_state.generated_question['Options']
                if len(options) == 4:  # Ensure we have exactly 4 options
                    st.write("**選択肢 (Options):**")
                    selected_answer = st.radio(
                        "",
                        options=range(1, 5),
                        format_func=lambda x: f"{x}. {options[x-1]}",
                        key="answer_selection",
                        disabled=st.session_state.answer_submitted,
                        horizontal=False,
                        label_visibility="collapsed"
                    )
                    
                    # Add Submit Answer button
                    if not st.session_state.answer_submitted:
                        if st.button("Submit Answer", type="primary"):
                            with st.spinner("Checking answer..."):
                                # Get correct answer directly from the generated question
                                correct_answer = st.session_state.generated_question.get('correct_answer')
                                
                                if correct_answer is not None:
                                    is_correct = int(selected_answer) == int(correct_answer)
                                    feedback = {
                                        'correct': is_correct,
                                        'correct_answer': correct_answer,
                                        'explanation': f"{'正解です！' if is_correct else '不正解です。'} The correct answer is option {correct_answer}: {options[correct_answer-1]}"
                                    }
                                    st.session_state.feedback = feedback
                                    st.session_state.answer_submitted = True
                                    st.rerun()
                                else:
                                    st.error("Could not find correct answer in the question")
                    
                    # Display feedback section
                    if st.session_state.answer_submitted and st.session_state.feedback:
                        feedback_container = st.container()
                        with feedback_container:
                            if st.session_state.feedback['correct']:
                                st.success(f"✅ Correct! You selected option {selected_answer}")
                            else:
                                correct_answer = st.session_state.feedback['correct_answer']
                                st.error(
                                    f"❌ Incorrect! You selected option {selected_answer}.\n\n"
                                    f"The correct answer is option {correct_answer}: {options[correct_answer-1]}"
                                )
                            
                            st.markdown("### Explanation")
                            st.write(st.session_state.feedback['explanation'])
                        
                        # Show next question button
                        if st.button("Generate New Question", type="primary"):
                            st.session_state.generated_question = None
                            st.session_state.feedback = None
                            st.session_state.answer_submitted = False
                            if 'audio_data' in st.session_state:
                                del st.session_state.audio_data
                            st.rerun()

    # Example topics
    with st.expander("Example Topics"):
        st.markdown("""
        Try these topics:
        - Shopping (買い物)
        - Restaurant (レストラン)
        - School (学校)
        - Weather (天気)
        - Travel (旅行)
        - Work (仕事)
        - Hobbies (趣味)
        """)

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