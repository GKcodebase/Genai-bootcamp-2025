from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Association table for many-to-many relationship between words and groups
word_groups = Table(
    'word_groups', Base.metadata,
    Column('word_id', Integer, ForeignKey('words.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    kanji = Column(String, index=True)
    romaji = Column(String)
    english = Column(String)
    parts = Column(JSON)

    reviews = relationship("WordReviewItem", back_populates="word")
    groups = relationship("Group", secondary=word_groups, back_populates="words")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    words_count = Column(Integer, default=0)

    words = relationship("Word", secondary=word_groups, back_populates="groups")

class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    thumbnail_url = Column(String)  # Add this line to include the preview_url attribute

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"))
    created_at = Column(DateTime, default=func.now())

    group = relationship("Group")
    study_activity = relationship("StudyActivity")
    word_reviews = relationship("WordReviewItem", back_populates="session")

class WordReviewItem(Base):
    __tablename__ = "word_review_items"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"))
    correct = Column(Boolean)
    created_at = Column(DateTime, default=func.now())

    word = relationship("Word", back_populates="reviews")
    session = relationship("StudySession", back_populates="word_reviews")