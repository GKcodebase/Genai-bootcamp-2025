from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from deep_translator import GoogleTranslator
from gtts import gTTS
from pathlib import Path
import os
from typing import List
import google.generativeai as genai
from ..database import get_db
from .. import models, schemas
from ..core.config import settings

router = APIRouter()
translator = GoogleTranslator(source='en', target='ml')

OMDB_API_KEY = settings.OMDB_API_KEY

# Initialize Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-001')

@router.post("/movie_plot", response_model=schemas.MoviePlotResponse)
async def get_movie_plot(request: schemas.MoviePlotRequest, db: Session = Depends(get_db)):
    try:
        # Check if movie already exists
        movie = db.query(models.MoviePlot).filter(
            models.MoviePlot.movie_name == request.movie_name
        ).first()
        
        if movie:
            return {
                "movie_id": movie.id,
                "movie_name": movie.movie_name,
                "english_plot": movie.english_plot,  # Include this field
                "malayalam_plot": movie.malayalam_plot,
                "audio_url": movie.audio_url
            }
        
        # Fetch plot from OMDB API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://www.omdbapi.com/",
                params={
                    "apikey": settings.OMDB_API_KEY,
                    "t": request.movie_name,
                    "plot": "full"
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch movie data")
            
            movie_data = response.json()
            if movie_data.get("Response") == "False":
                raise HTTPException(status_code=404, detail="Movie not found")
            
            english_plot = movie_data.get("Plot")
            if not english_plot:
                raise HTTPException(status_code=404, detail="No plot found for this movie")
        
        # Translate to Malayalam
        malayalam_plot = translator.translate(english_plot)
        
        # Use absolute paths for audio files
        base_dir = Path(__file__).parent.parent.parent
        audio_path = base_dir / "static" / "audio" / "movies"
        audio_path.mkdir(parents=True, exist_ok=True)

        # Sanitize filename
        safe_filename = "".join(c for c in request.movie_name.lower() if c.isalnum() or c in ('-', '_'))
        audio_filename = f"{safe_filename}.mp3"
        audio_file = audio_path / audio_filename

        # Generate audio
        tts = gTTS(text=malayalam_plot, lang='ml')
        tts.save(str(audio_file))

        # Store relative URL in database
        audio_url = f"/static/audio/movies/{audio_filename}"
        
        # Save to database with correct URL path
        movie = models.MoviePlot(
            movie_name=request.movie_name,
            english_plot=english_plot,
            malayalam_plot=malayalam_plot,
            audio_url=audio_url
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)
        
        return {
            "movie_id": movie.id,
            "movie_name": movie.movie_name,
            "english_plot": movie.english_plot,  # Include this field
            "malayalam_plot": movie.malayalam_plot,
            "audio_url": movie.audio_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/movie_chat", response_model=schemas.ChatResponse)
async def chat_with_movie(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    try:
        movie = db.query(models.MoviePlot).filter(models.MoviePlot.id == request.movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        if not settings.GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")

        context = f"""
        Movie: {movie.movie_name}
        Plot: {movie.english_plot}
        
        Instructions:
        - You are a knowledgeable character from this movie
        - Answer questions based on the movie's plot and story
        - Keep responses concise (2-3 sentences)
        - Be engaging and conversational
        - Stick to the movie's facts
        """
        
        try:
            prompt = f"{context}\nQuestion: {request.message}\nAnswer:"
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                raise ValueError("Empty response from Gemini API")
                
            english_response = response.text.strip()
            malayalam_response = translator.translate(english_response)
            
            if not malayalam_response:
                malayalam_response = "Sorry, translation failed. / ക്ഷമിക്കണം, വിവർത്തനം പരാജയപ്പെട്ടു."
            
            return schemas.ChatResponse(
                english_response=english_response,
                malayalam_response=malayalam_response
            )
            
        except Exception as ai_error:
            print(f"AI generation error: {ai_error}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate response. Please try again."
            )
            
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again."
        )