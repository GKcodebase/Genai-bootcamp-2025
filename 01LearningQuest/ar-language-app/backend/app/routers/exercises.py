from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
import google.generativeai as genai
import json
import time
from pathlib import Path
import os
from gtts import gTTS
import base64
from datetime import datetime

router = APIRouter()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-001')

# Define audio directory
AUDIO_DIR = Path("static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/exercises/{object_id}")
async def get_exercises(object_id: int):
    return {
        "object_id": object_id,
        "exercises": [
            {
                "type": "writing",
                "prompt": "Write the Malayalam word for this object"
            },
            {
                "type": "speaking",
                "prompt": "Pronounce the Malayalam word"
            }
        ],
        "timestamp": datetime.now()
    }

@router.get("/generate_exercise")
async def generate_exercise(object_id: int, db: Session = Depends(get_db)):
    """Generate a practice exercise with audio"""
    try:
        # Get object from database
        object_data = await crud.get_object(db, object_id)
        if not object_data:
            raise HTTPException(status_code=404, detail="Object not found")

        # Generate exercise using Gemini
        prompt = f"""
        Create a simple Malayalam learning exercise using the word '{object_data.malayalam_translation}' (meaning: {object_data.name}).
        Return a JSON object in this exact format:
        {{
            "malayalam_phrase": "A simple Malayalam phrase using the word",
            "english_translation": "The English translation of the phrase"
        }}
        Only return the JSON, no other text.
        """

        # Generate content with Gemini
        response = model.generate_content(prompt)
        
        # Clean up the response text
        response_text = response.text.strip()
        
        # Handle possible markdown formatting
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].strip()

        print("Raw Gemini response:", response_text)  # Debug log
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print(f"Attempted to parse: {response_text}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate valid exercise content"
            )

        # Generate audio for the Malayalam phrase
        filename = f"exercise_{object_id}_{int(time.time())}.mp3"
        output_path = AUDIO_DIR / filename

        tts = gTTS(
            text=result["malayalam_phrase"],
            lang='ml',
            slow=False
        )
        tts.save(str(output_path))

        # Return exercise data
        return {
            "phrase": result["malayalam_phrase"],
            "english_translation": result["english_translation"],
            "audio_url": f"http://127.0.0.1:8000/static/audio/{filename}"
        }

    except Exception as e:
        print(f"Exercise generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating exercise: {str(e)}"
        )