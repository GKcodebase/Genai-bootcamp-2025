import streamlit as st
import requests
import json

st.title("Song Vocabulary Generator")

# Initialize session state for loading state if not exists
if 'processing' not in st.session_state:
    st.session_state.processing = False

song_name = st.text_input("Enter song name:")
primary_lang = st.text_input("Enter primary language:")
target_lang = st.text_input("Enter target language:")

# Disable button only during processing
if st.button("Generate Vocabulary", disabled=st.session_state.processing):
    if song_name and primary_lang and target_lang:
        try:
            # Set processing state
            st.session_state.processing = True
            
            # Show loading spinner with custom message
            with st.spinner("🎵 Finding your song lyrics and creating vocabulary... 🎸"):
                # Call the FastAPI endpoint
                response = requests.post(
                    "http://localhost:8000/api/agent",
                    json={
                        "message_request": song_name,
                        "primary_lang": primary_lang,
                        "target_lang": target_lang
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Show success message with balloons
                    st.balloons()
                    
                    st.subheader("📝 Lyrics")
                    st.text(data["lyrics"])
                    
                    st.subheader("📚 Vocabulary")
                    # Create a nice looking table for vocabulary
                    vocab_data = {"Word": [], "Translation": []}
                    for word, translation in data["translation"].items():
                        vocab_data["Word"].append(word)
                        vocab_data["Translation"].append(translation)
                    
                    st.table(vocab_data)
                else:
                    st.error("Failed to generate vocabulary")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Reset processing state
            st.session_state.processing = False
    else:
        st.warning("🎯 Please fill in all fields")