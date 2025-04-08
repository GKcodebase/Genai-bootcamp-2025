from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    malayalam_translation = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    exercises = relationship("Exercise", back_populates="object")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey("objects.id"))
    phrase = Column(String)
    audio_url = Column(String)
    object = relationship("Object", back_populates="exercises")