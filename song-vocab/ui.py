import streamlit as st
import requests
import json

st.title("Song Vocabulary Generator")

song_name = st.text_input("Enter song name:")
primary_lang = st.text_input("Enter primary language:")
target_lang = st.text_input("Enter target language:")

if st.button("Generate Vocabulary"):
    if song_name and primary_lang and target_lang:
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
            
            st.subheader("Lyrics")
            st.text(data["lyrics"])
            
            st.subheader("Vocabulary")
            for word, translation in data["translation"].items():
                st.write(f"{word} - {translation}")
        else:
            st.error("Failed to generate vocabulary")
    else:
        st.warning("Please fill in all fields")