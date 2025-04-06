from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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