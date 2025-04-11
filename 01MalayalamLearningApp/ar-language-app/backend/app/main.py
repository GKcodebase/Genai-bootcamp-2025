from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import objects, audio, exercises, alphabets, movies
from .database import engine
from . import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create base static directory and subdirectories
base_dir = Path(__file__).parent.parent
static_dir = base_dir / "static"
static_dir.mkdir(exist_ok=True)
movies_dir = static_dir / "audio" / "movies"
movies_dir.mkdir(parents=True, exist_ok=True)

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

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
app.include_router(movies.router, prefix="/api")