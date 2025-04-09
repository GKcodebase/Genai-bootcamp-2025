import ollama
from tools.search_web import search_lyrics
from tools.get_page_content import get_page_content
from tools.extract_vocabulary import extract_vocabulary
import logging
from utils.logger import setup_logger

logger = setup_logger()

class SongAgent:
    def __init__(self):
        logger.info("Initializing SongAgent")
        self.model = "llama3.2:1b"
        self.ollama_client = ollama.Client(host='http://localhost:11434')
        logger.debug(f"Initialized with model: {self.model}")
        
    async def process(self, song_request: str, primary_lang: str, target_lang: str):
        logger.info(f"Processing song request: {song_request}")
        
        # Search for lyrics
        logger.debug("Searching for lyrics...")
        search_results = search_lyrics(song_request, primary_lang)
        logger.info(f"Found {len(search_results)} search results")
        
        # Try each result until we get valid lyrics
        lyrics = ""
        for idx, result in enumerate(search_results, 1):
            lyrics_url = result["link"]
            logger.debug(f"Attempting to fetch lyrics from URL ({idx}/{len(search_results)}): {lyrics_url}")
            
            lyrics = await get_page_content(lyrics_url)
            if len(lyrics) > 100 and '\n' in lyrics:
                logger.info("Successfully extracted lyrics")
                break
            
            logger.debug("Invalid lyrics content, trying next result")
        
        if not lyrics:
            logger.warning("No valid lyrics found in any search result")
            return {"lyrics": "", "vocabulary": [], "translation": {}}
        
        # Extract vocabulary
        logger.debug("Extracting vocabulary from lyrics")
        vocab_list = extract_vocabulary(lyrics)
        logger.info(f"Extracted {len(vocab_list)} vocabulary words")
        
        # Translate vocabulary
        logger.info("Starting vocabulary translation")
        translations = {}
        for idx, word in enumerate(vocab_list, 1):
            logger.debug(f"Translating word {idx}/{len(vocab_list)}: {word}")
            try:
                response = self.ollama_client.chat(model=self.model, messages=[
                    {
                        "role": "user",
                        "content": f"Translate this {primary_lang} word to {target_lang}: {word}"
                    }
                ])
                translations[word] = response['message']['content'].strip()
            except Exception as e:
                logger.error(f"Error translating word '{word}': {str(e)}")
                translations[word] = f"Translation error: {str(e)}"
        
        logger.info("Processing completed successfully")
        return {
            "lyrics": lyrics,
            "vocabulary": vocab_list,
            "translation": translations
        }