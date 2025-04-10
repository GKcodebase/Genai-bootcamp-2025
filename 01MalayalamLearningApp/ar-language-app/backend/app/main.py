from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import objects, audio, exercises, alphabets
from .database import engine
from . import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files directory
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
audio_dir = static_dir / "audio"
audio_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Update CORS middleware with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "https://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],           # Allow all methods
    allow_headers=["*"],           # Allow all headers
    expose_headers=["*"],          # Expose all headers
    max_age=3600                   # Cache preflight response for 1 hour
)

# Include routers
app.include_router(objects.router, prefix="/api")
app.include_router(audio.router, prefix="/api")
app.include_router(exercises.router, prefix="/api")
app.include_router(alphabets.router, prefix="/api")