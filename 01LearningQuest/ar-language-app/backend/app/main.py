from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import objects, audio, exercises
from .database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all headers
)

# Include routers
app.include_router(objects.router, prefix="/api", tags=["Objects"])
app.include_router(audio.router, prefix="/api", tags=["Audio"])
app.include_router(exercises.router, prefix="/api", tags=["Exercises"])