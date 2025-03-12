import ollama
from tools.search_web import search_lyrics
from tools.get_page_content import get_page_content
from tools.extract_vocabulary import extract_vocabulary

class SongAgent:
    def __init__(self):
        self.model = "llama3.2:1b"
        # Set Ollama host through environment variable or directly in client instantiation
        self.ollama_client = ollama.Client(host='http://localhost:8008')
        
    async def process(self, song_request: str, primary_lang: str, target_lang: str):
        # Search for lyrics
        search_results = search_lyrics(song_request, primary_lang)
        
        # Try each result until we get valid lyrics
        lyrics = ""
        for result in search_results:
            lyrics_url = result["link"]
            lyrics = await get_page_content(lyrics_url)
            
            # Check if we got valid lyrics (at least 100 characters and contains newlines)
            if len(lyrics) > 100 and '\n' in lyrics:
                break
        
        if not lyrics:
            return {"lyrics": "", "vocabulary": [], "translation": {}}
            
        # Extract vocabulary
        vocab_list = extract_vocabulary(lyrics)
        
        # Translate vocabulary using Ollama
        translations = {}
        for word in vocab_list:
            response = self.ollama_client.chat(model=self.model, messages=[
                {
                    "role": "user",
                    "content": f"Translate this {primary_lang} word to {target_lang}: {word}"
                }
            ])
            translations[word] = response['message']['content'].strip()
        
        return {
            "lyrics": lyrics,
            "vocabulary": vocab_list,
            "translation": translations
        }