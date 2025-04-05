from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import logging
from app import crud, schemas
from app.database import SessionLocal
from datetime import datetime
import google.generativeai as genai
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def process_image(image: UploadFile) -> str:
    """Process the image using Gemini Vision API"""
    try:
        # Log the image details
        logger.info(f"Processing image: {image.filename}, type: {image.content_type}")
        
        # Read and convert image to bytes
        contents = await image.read()
        
        # Convert to PIL Image for validation
        img = Image.open(io.BytesIO(contents))
        
        # Convert image back to bytes for API
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format or 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        image_parts = [{
            "mime_type": image.content_type or "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode('utf-8')
        }]

        prompt = "What object is in this image? Return just the name of the object in a single word."
        
        logger.info("Sending request to Gemini API")
        response = model.generate_content([{
            "text": prompt
        }, image_parts[0]])
        
        # Extract the object name from response
        object_name = response.text.strip().lower()
        logger.info(f"Detected object: {object_name}")
        return object_name
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

async def get_malayalam_translation(object_name: str) -> str:
    """Get Malayalam translation using Gemini API"""
    try:
        prompt = f"Translate the English word '{object_name}' to Malayalam. Return only the Malayalam word, nothing else."
        
        logger.info(f"Requesting translation for: {object_name}")
        response = model.generate_content(prompt)
        
        # Extract the translation from response
        translation = response.text.strip()
        logger.info(f"Received translation: {translation}")
        
        return translation
    except Exception as e:
        logger.error(f"Translation error: {str(e)}", exc_info=True)
        return "വിവർത്തനം ലഭ്യമല്ല"  # "Translation not available" in Malayalam

@router.post("/recognize_object", response_model=schemas.Object)
async def recognize_object(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File uploaded is not an image"
            )
        
        # Process image with Gemini
        logger.info("Starting image recognition")
        object_name = await process_image(image)
        
        # Get Malayalam translation using Gemini
        malayalam_translation = await get_malayalam_translation(object_name)
        logger.info(f"Translation for {object_name}: {malayalam_translation}")
        
        # Create object in database
        object_data = schemas.ObjectCreate(
            name=object_name,
            malayalam_translation=malayalam_translation
        )
        db_object = crud.create_object(db, object_data)
        
        return {
            "id": db_object.id,
            "name": db_object.name,
            "malayalam_translation": db_object.malayalam_translation,
            "timestamp": db_object.timestamp
        }
        
    except HTTPException as he:
        logger.error(f"HTTP Exception: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/history", response_model=list[schemas.Object])
def get_history(db: Session = Depends(get_db)):
    return crud.get_objects(db)