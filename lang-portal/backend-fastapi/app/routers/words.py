from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/api/words",
    tags=["words"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Word])
def read_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    words = crud.get_words(db, skip=skip, limit=limit)
    return [
        schemas.Word(
            id=word.id,
            kanji=word.kanji,
            romaji=word.romaji,
            english=word.english,
            parts=word.parts
        ) for word in words
    ]

@router.post("/", response_model=schemas.Word)
def create_word(word: schemas.WordCreate, db: Session = Depends(get_db)):
    return crud.create_word(db=db, word=word)

@router.get("/{word_id}", response_model=schemas.Word)
def read_word(word_id: int, db: Session = Depends(get_db)):
    db_word = crud.get_word(db, word_id=word_id)
    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return db_word
