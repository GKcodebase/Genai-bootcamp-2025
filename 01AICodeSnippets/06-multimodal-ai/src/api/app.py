import os
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

from ..models.vision_model import VisionModel
from ..models.audio_model import AudioModel

# Initialize FastAPI app
app = FastAPI(
    title="Multimodal AI API",
    description="API for image analysis and audio transcription using Gemini Vision and Whisper",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
vision_model = VisionModel()
audio_model = AudioModel()

@app.post("/analyze/image")
async def analyze_image(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    stream: bool = Form(False)
):
    """Analyze a single image."""
    try:
        # Read and validate image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # Analyze image
        result = await vision_model.analyze_image(
            image=img,
            prompt=prompt,
            stream=stream
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/images")
async def analyze_multiple_images(
    images: List[UploadFile] = File(...),
    prompt: str = Form(...),
    stream: bool = Form(False)
):
    """Analyze multiple images."""
    try:
        # Read and validate images
        img_list = []
        for image in images:
            contents = await image.read()
            img = Image.open(io.BytesIO(contents))
            img_list.append(img)
        
        # Analyze images
        result = await vision_model.analyze_multiple_images(
            images=img_list,
            prompt=prompt,
            stream=stream
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe/audio")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(None),
    task: str = Form("transcribe"),
    initial_prompt: Optional[str] = Form(None)
):
    """Transcribe an audio file."""
    try:
        # Read audio file
        contents = await audio.read()
        
        # Get file format
        file_format = audio.filename.split(".")[-1].lower()
        
        # Transcribe audio
        result = await audio_model.transcribe_from_bytes(
            audio_bytes=contents,
            file_format=file_format,
            language=language,
            task=task,
            initial_prompt=initial_prompt
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "vision_model": vision_model.to_dict(),
        "audio_model": audio_model.to_dict()
    } 