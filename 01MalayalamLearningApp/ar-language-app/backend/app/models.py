from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime

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

class Alphabet(Base):
    __tablename__ = "alphabets"
    
    id = Column(Integer, primary_key=True, index=True)
    malayalam_char = Column(String, unique=True)
    english_transliteration = Column(String)
    audio_url = Column(String)  # Keep this field
    
    words = relationship("GeneratedWord", back_populates="alphabet")

class GeneratedWord(Base):
    __tablename__ = "generated_words"
    
    id = Column(Integer, primary_key=True, index=True)
    alphabet_id = Column(Integer, ForeignKey("alphabets.id"))
    word = Column(String)
    english_translation = Column(String)
    pronunciation = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    alphabet = relationship("Alphabet", back_populates="words")