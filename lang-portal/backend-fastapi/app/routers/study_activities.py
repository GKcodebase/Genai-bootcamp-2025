from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal
from typing import List

router = APIRouter(
    prefix="/api/study_activities",
    tags=["study_activities"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.StudyActivity])
def read_study_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    study_activities = crud.get_study_activities(db, skip=skip, limit=limit)
    return study_activities

@router.post("/", response_model=schemas.StudyActivity)
def create_study_activity(study_activity: schemas.StudyActivityCreate, db: Session = Depends(get_db)):
    return crud.create_study_activity(db=db, study_activity=study_activity)

@router.get("/{study_activity_id}", response_model=schemas.StudyActivity)
def read_study_activity(study_activity_id: int, db: Session = Depends(get_db)):
    db_study_activity = crud.get_study_activity(db, study_activity_id=study_activity_id)
    if db_study_activity is None:
        raise HTTPException(status_code=404, detail="Study activity not found")
    return db_study_activity
