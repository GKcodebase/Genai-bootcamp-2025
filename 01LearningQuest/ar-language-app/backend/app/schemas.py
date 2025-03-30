from pydantic import BaseModel
from datetime import datetime

class ObjectBase(BaseModel):
    name: str
    malayalam_translation: str

class Object(ObjectBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ObjectCreate(ObjectBase):
    pass

class ExerciseBase(BaseModel):
    phrase: str
    audio_url: str

class ExerciseCreate(ExerciseBase):
    object_id: int

class Exercise(ExerciseBase):
    id: int
    object: Object

    class Config:
        orm_mode = True