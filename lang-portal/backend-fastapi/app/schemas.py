from pydantic import BaseModel
from typing import List, Optional, Dict, Union
from datetime import datetime

class KanjiPart(BaseModel):
    kanji: str
    romaji: List[str]

class WordBase(BaseModel):
    kanji: str
    romaji: str
    english: str
    parts: List[KanjiPart]

class WordCreate(WordBase):
    pass

class Word(WordBase):
    id: int

    class Config:
        from_attributes = True  # Updated configuration key

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    words_count: int

    class Config:
        from_attributes = True  # Updated configuration key

class StudySessionBase(BaseModel):
    group_id: int
    created_at: datetime
    study_activity_id: int

class StudySessionCreate(StudySessionBase):
    pass

class StudySession(StudySessionBase):
    id: int

    class Config:
        from_attributes = True  # Updated configuration key

class StudyActivityBase(BaseModel):
    name: str
    url: str
    thumbnail_url: str

class StudyActivityCreate(StudyActivityBase):
    pass

class StudyActivity(StudyActivityBase):
    id: int

    class Config:
        from_attributes = True  # Updated configuration key

class WordReviewItemBase(BaseModel):
    word_id: int
    study_session_id: int
    correct: bool
    created_at: datetime

class WordReviewItemCreate(WordReviewItemBase):
    pass

class WordReviewItem(WordReviewItemBase):
    id: int

    class Config:
        from_attributes = True  # Updated configuration key
