from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ObjectBase(BaseModel):
    name: str
    malayalam_translation: str

class ObjectCreate(ObjectBase):
    pass

class Object(ObjectBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True  # Changed from orm_mode = True

class ExerciseBase(BaseModel):
    object_id: int
    phrase: str
    audio_url: str

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int

    class Config:
        from_attributes = True

class Alphabet(BaseModel):
    id: int
    malayalam_char: str
    english_transliteration: str
    audio_url: str

    class Config:
        from_attributes = True  # replaces orm_mode

class GeneratedWord(BaseModel):
    word: str
    english_translation: str
    pronunciation: str

    class Config:
        from_attributes = True

class WordResponse(BaseModel):
    alphabet_id: int
    words: List[GeneratedWord]

class MoviePlotRequest(BaseModel):
    movie_name: str

class MoviePlotResponse(BaseModel):
    movie_id: int
    movie_name: str
    english_plot: str  # Required field
    malayalam_plot: str
    audio_url: str

    class Config:
        from_attributes = True  # Enable ORM mode

class ChatRequest(BaseModel):
    movie_id: int
    message: str

class ChatResponse(BaseModel):
    english_response: str
    malayalam_response: str

    class Config:
        from_attributes = True