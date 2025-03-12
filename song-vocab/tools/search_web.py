from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

def search_lyrics(song_name: str, language: str) -> list:
    """Search for song lyrics using Google Search."""
    # Create a search query with lyrics-specific terms but without site restrictions
    search = GoogleSearch({
        "q": f"{song_name} lyrics {language}",
        "api_key": os.getenv("SERP_API_KEY"),
        "num": 20,  # Increased number of results
        "gl": "us",  # Set region to US for more reliable results
        # Filter out problematic sites known to block automated access
        "exclude_sites": "genius.com,musixmatch.com",
        "safe": "active"  # Enable safe search to avoid inappropriate content
    })
    
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    # Filter results to prioritize those that likely contain lyrics
    filtered_results = []
    for result in organic_results:
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()
        
        # Check if the result appears to be lyrics-related
        if any(keyword in title or keyword in snippet 
               for keyword in ["lyrics", "song", "words", "text", language.lower()]):
            filtered_results.append(result)
    
    return filtered_results[:10]  # Return top 10 filtered results