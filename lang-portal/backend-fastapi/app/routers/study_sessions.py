from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal
from typing import List

router = APIRouter(
    prefix="/api/study_sessions",
    tags=["study_sessions"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.StudySession])
def read_study_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    study_sessions = crud.get_study_sessions(db, skip=skip, limit=limit)
    return study_sessions

@router.post("/", response_model=schemas.StudySession)
def create_study_session(study_session: schemas.StudySessionCreate, db: Session = Depends(get_db)):
    return crud.create_study_session(db=db, study_session=study_session)

@router.get("/{study_session_id}", response_model=schemas.StudySession)
def read_study_session(study_session_id: int, db: Session = Depends(get_db)):
    db_study_session = crud.get_study_session(db, study_session_id=study_session_id)
    if db_study_session is None:
        raise HTTPException(status_code=404, detail="Study session not found")
    return db_study_session
