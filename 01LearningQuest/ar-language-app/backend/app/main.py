from fastapi import FastAPI
from .routers import objects, audio, exercises
from .database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(objects.router, prefix="/api", tags=["Objects"])
app.include_router(audio.router, prefix="/api", tags=["Audio"])
app.include_router(exercises.router, prefix="/api", tags=["Exercises"])