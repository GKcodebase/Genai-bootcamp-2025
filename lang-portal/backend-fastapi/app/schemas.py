from pydantic import BaseModel
from typing import List, Optional


class WordBase(BaseModel):
    kanji: str
    romaji: str
    english: str
    parts: dict


class Word(WordBase):
    id: int

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str


class Group(GroupBase):
    id: int
    words_count: int

    class Config:
        orm_mode = True


class StudyActivity(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


class StudySessionBase(BaseModel):
    group_id: int
    study_activity_id: int


class StudySession(StudySessionBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True


class WordReviewItem(BaseModel):
    word_id: int
    study_session_id: int
    correct: bool

    class Config:
        orm_mode = True
