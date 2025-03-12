# Tech Specs

## Business Goal
We want to create a program that will find lyrics off the internet for a target song in a specific langauge and produce vocabulary to be imported into our database.

## Front End requirements
 1.User will type the song name , primarylanguage name and traget name click the button to search and generate
 Generate a list of vocabulary in primary language and translation in target language

## Technical Requirements

- FastAPI
- Ollama via api hosted in http://localhost:8008
    - llama3.2:1b
- Instructor (for structured json output)
- SQLite3 (for database)
- Serp API (to search for lyrics)
- Streamlit for UI

## API Endpoints

### GetLyrics POST /api/agent 

### Behaviour

This endpoint goes to our agent which is uses the reAct framework
so that it can go to the internet, find multiple possible version of lyrics
and then extract out the correct lyrics and format the lyrics into vocaulary.
Once vacabulary is generated, it is translated to target language

Tools avaliable:
- tools/extract_vocabulary.py
- tools/get_page_content.py
- tools/search_web.py

### JSON Request Parameters
- `message_request` (str): A string that describes the song and/or artist to get lyrics for a song from the ineternet
- `primary_lang` (str): A string in which the song is written.
- `traget_lang` (str): A string in which we need translation.

### JSON Response
- `lyrics` (str): The lyrics of the song
- `vocabulary` (list): A list of vocabulary words found in the lyrics
- `translation` (key-value): A map of vocabulary in primary land and translation in target lang.