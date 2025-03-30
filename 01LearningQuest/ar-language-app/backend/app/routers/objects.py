from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recognize_object", response_model=schemas.Object)
async def recognize_object(object_data: schemas.ObjectCreate):
    # Dummy implementation for now
    return {
        "id": 1,
        "name": object_data.name,
        "malayalam_translation": "dummy translation",
        "timestamp": datetime.now()
    }

@router.get("/history", response_model=list[schemas.Object])
def get_history(db: Session = Depends(get_db)):
    return crud.get_objects(db)