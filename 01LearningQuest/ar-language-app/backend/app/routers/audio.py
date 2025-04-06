from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
import whisper
import numpy as np
import soundfile as sf
import io
import tempfile
from difflib import SequenceMatcher
from functools import lru_cache
from typing import Dict, Set, List, Tuple
import re
from ..utils.transliteration import transliterate_malayalam
import hashlib
from gtts import gTTS

# Load environment variables
load_dotenv()

router = APIRouter()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro')

# Create audio directory if it doesn't exist
AUDIO_DIR = Path("static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Whisper model with specific settings
model = whisper.load_model("base", device="cpu")  # Explicitly use CPU

# Create cache directory
CACHE_DIR = Path("static/audio/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/audio/{object_id}")
async def get_audio(object_id: int):
    return {
        "object_id": object_id,
        "audio_url": f"https://example.com/audio/{object_id}.mp3",
        "timestamp": datetime.now()
    }

@router.post("/audio/generate")
async def generate_audio(text: str):
    return {
        "text": text,
        "audio_url": "https://example.com/audio/generated.mp3",
        "timestamp": datetime.now()
    }

@router.get("/generate_audio")
async def generate_audio(text: str):
    """Generate audio for Malayalam text with caching"""
    try:
        # Create a unique filename based on the text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        cache_file = CACHE_DIR / f"{text_hash}.mp3"

        # Return cached file if it exists
        if cache_file.exists():
            return {
                "audio_url": f"http://127.0.0.1:8000/static/audio/cache/{cache_file.name}"
            }

        # Generate new audio file using gTTS with better quality
        tts = gTTS(
            text=text,
            lang='ml',  # Malayalam
            slow=False,  # Normal speed
            lang_check=False  # Skip language check for faster generation
        )
        
        # Save with higher quality settings
        tts.save(str(cache_file))

        return {
            "audio_url": f"http://127.0.0.1:8000/static/audio/cache/{cache_file.name}"
        }

    except Exception as e:
        print(f"Audio generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating audio: {str(e)}"
        )

# Optional: Add cleanup endpoint for cache management
@router.delete("/clear_audio_cache")
async def clear_audio_cache():
    """Clear the audio cache directory"""
    try:
        for file in CACHE_DIR.glob("*.mp3"):
            file.unlink()
        return {"message": "Audio cache cleared"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing cache: {str(e)}"
        )

# Add caching for phonetic map
@lru_cache(maxsize=1)
def get_malayalam_phonetic_map() -> Dict[str, List[str]]:
    """Cached version of Malayalam phonetic mapping"""
    return {
        # Vowels
        'അ': ['a', 'u'],
        'ആ': ['aa', 'a'],
        'ഇ': ['i', 'e'],
        'ഈ': ['ee', 'i'],
        'ഉ': ['u', 'oo'],
        'ഊ': ['oo', 'u'],
        'എ': ['e', 'a'],
        'ഏ': ['e', 'ea'],
        'ഐ': ['ai', 'ei'],
        'ഒ': ['o', 'oh'],
        'ഓ': ['o', 'oh'],
        'ഔ': ['au', 'ow'],

        # Consonants
        'ക': ['ka', 'ga', 'kha'],
        'ഖ': ['kha', 'ka'],
        'ഗ': ['ga', 'ka'],
        'ഘ': ['gha', 'ga'],
        'ങ': ['nga', 'na'],
        'ച': ['cha', 'ja'],
        'ഛ': ['chha', 'cha'],
        'ജ': ['ja', 'cha'],
        'ഝ': ['jha', 'ja'],
        'ഞ': ['nya', 'na'],
        'ട': ['ta', 'da'],
        'ഠ': ['tta', 'ta'],
        'ഡ': ['da', 'ta'],
        'ഢ': ['dha', 'da'],
        'ണ': ['na', 'na'],
        'ത': ['tha', 'da'],
        'ഥ': ['thha', 'tha'],
        'ദ': ['dha', 'da'],
        'ധ': ['dha', 'tha'],
        'ന': ['na', 'nu'],
        'പ': ['pa', 'ba'],
        'ഫ': ['pha', 'fa'],
        'ബ': ['ba', 'pa'],
        'ഭ': ['bha', 'ba'],
        'മ': ['ma', 'mu'],
        'യ': ['ya', 'yu'],
        'ര': ['ra', 'ru'],
        'ല': ['la', 'lu'],
        'വ': ['va', 'wa'],
        'ശ': ['sha', 'sa'],
        'ഷ': ['sha', 'sa'],
        'സ': ['sa', 'sha'],
        'ഹ': ['ha', 'hu'],
        'ള': ['la', 'zha'],
        'ഴ': ['zha', 'la'],
        'റ': ['ra', 'rra'],

        # Special characters
        'ം': ['m', 'um', 'am'],
        '്': ['', 'u'],
        'ാ': ['a', 'aa'],
        'ി': ['i', 'e'],
        'ീ': ['ee', 'i'],
        'ു': ['u', 'oo'],
        'ൂ': ['oo', 'u'],
        'െ': ['e', 'a'],
        'േ': ['e', 'ea'],
        'ൈ': ['ai', 'ei'],
        'ൊ': ['o', 'oh'],
        'ോ': ['o', 'oh'],
        'ൗ': ['au', 'ow']
    }

# Add efficient text normalization
def normalize_text(text: str) -> str:
    """Normalize text by removing spaces and special characters"""
    return re.sub(r'[^\w\s]', '', text.lower())

# Add pattern caching
@lru_cache(maxsize=100)
def get_phonetic_patterns_cached(text: str) -> Set[str]:
    """Cached version of phonetic pattern generation"""
    phonetic_map = get_malayalam_phonetic_map()
    patterns = set()
    
    # Optimize pattern matching by pre-computing lengths
    char_lengths = sorted(set(len(chars) for chars in phonetic_map.keys()), reverse=True)
    
    i = 0
    while i < len(text):
        matched = False
        # Check longest patterns first
        for length in char_lengths:
            if i + length <= len(text):
                chars = text[i:i+length]
                if chars in phonetic_map:
                    patterns.update(phonetic_map[chars])
                    i += length - 1  # Move forward by pattern length
                    matched = True
                    break
        if not matched:
            i += 1
            
    return patterns

# Update the similarity computation
def compute_phonetic_similarity(malayalam_text: str, english_text: str) -> Tuple[float, Dict[str, float]]:
    """Compute similarity with detailed metrics"""
    # Get cached patterns
    malayalam_patterns = get_phonetic_patterns_cached(malayalam_text)
    english_clean = normalize_text(english_text)
    
    # Calculate pattern matches
    pattern_scores = []
    for pattern in malayalam_patterns:
        if pattern in english_clean:
            score = SequenceMatcher(None, pattern, english_clean).ratio()
            pattern_scores.append(score)
    
    # Calculate different similarity metrics
    phonetic_score = max(pattern_scores) if pattern_scores else 0
    
    # Calculate syllable similarity
    malayalam_syllables = re.findall(r'[കഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരലവശഷസഹളഴറ][ാിീുൂെേൈൊോൗം]*', malayalam_text)
    english_syllables = re.findall(r'[bcdfghjklmnpqrstvwxyz][aeiou]*', english_clean)
    
    syllable_ratio = len(english_syllables) / len(malayalam_syllables) if malayalam_syllables else 0
    syllable_score = 1 - abs(1 - syllable_ratio) if syllable_ratio > 0 else 0
    
    # Return detailed metrics
    metrics = {
        'phonetic_score': phonetic_score,
        'syllable_score': syllable_score,
        'pattern_count': len(pattern_scores),
        'syllable_ratio': syllable_ratio
    }
    
    return phonetic_score, metrics

@router.post("/speaking_test")
async def verify_speech(
    audio: UploadFile = File(...),
    expected_text: str = Form(...)
):
    """Verify user's spoken Malayalam pronunciation"""
    try:
        # Transliterate the expected text
        expected_transliteration = transliterate_malayalam(expected_text)
        print(f"Transliterated text: {expected_transliteration}")

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Use Whisper with optimized settings
            result = model.transcribe(
                temp_path,
                language="ml",
                task="transcribe",
                fp16=False,
                beam_size=1  # Reduce beam size for faster processing
            )

            recognized_text = result["text"].strip()
            
            # Transliterate the recognized text
            recognized_transliteration = transliterate_malayalam(recognized_text)
            
            # Compare transliterations for better matching
            similarity = SequenceMatcher(
                None,
                expected_transliteration.lower(),
                recognized_transliteration.lower()
            ).ratio()
            
            # More lenient threshold since we're comparing transliterations
            is_correct = similarity >= 0.7
            
            print(f"Expected (transliterated): {expected_transliteration}")
            print(f"Recognized (transliterated): {recognized_transliteration}")
            print(f"Similarity: {similarity}")

            return {
                "recognized_text": recognized_text,
                "transliterated_expected": expected_transliteration,
                "transliterated_recognized": recognized_transliteration,
                "correct": is_correct,
                "confidence": similarity
            }

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except Exception as e:
        print(f"Processing error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing speech: {str(e)}"
        )