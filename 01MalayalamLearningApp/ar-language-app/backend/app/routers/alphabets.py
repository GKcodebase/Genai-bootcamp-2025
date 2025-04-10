from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import google.generativeai as genai
from ..core.config import settings
from ..database import get_db
from .. import models, schemas

router = APIRouter()

# Configure Gemini only if API key is available
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    model = None

@router.get("/alphabets", response_model=List[schemas.Alphabet])
async def get_alphabets(db: Session = Depends(get_db)):
    return db.query(models.Alphabet).all()

@router.get("/generate_words", response_model=schemas.WordResponse)
async def generate_words(alphabet_id: int, db: Session = Depends(get_db)):
    alphabet = db.query(models.Alphabet).filter(models.Alphabet.id == alphabet_id).first()
    if not alphabet:
        raise HTTPException(status_code=404, detail="Alphabet not found")

    if not model:
        raise HTTPException(status_code=500, detail="Generative AI model is not configured")

    prompt = f"""
    Generate 3 simple Malayalam words that start with the letter '{alphabet.malayalam_char}'.
    For each word provide:
    1. Malayalam word
    2. English translation
    3. Pronunciation in English
    Format: word1|translation1|pronunciation1, word2|translation2|pronunciation2, word3|translation3|pronunciation3
    """
    
    response = model.generate_content(prompt)
    word_data = [item.strip().split('|') for item in response.text.split(',')]
    
    # Save generated words to database
    generated_words = []
    for word_info in word_data[:3]:
        if len(word_info) == 3:  # Ensure we have all three parts
            word, translation, pronunciation = word_info
            word_entry = models.GeneratedWord(
                alphabet_id=alphabet_id,
                word=word.strip(),
                english_translation=translation.strip(),
                pronunciation=pronunciation.strip()
            )
            db.add(word_entry)
            generated_words.append({
                "word": word.strip(),
                "english_translation": translation.strip(),
                "pronunciation": pronunciation.strip()
            })
    
    db.commit()
    
    return {
        "alphabet_id": alphabet_id,
        "words": generated_words
    }