from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_object(db: Session, obj: schemas.ObjectCreate):
    db_object = models.Object(**obj.dict())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

def get_objects(db: Session):
    return db.query(models.Object).all()

async def get_object(db: Session, object_id: int):
    """Retrieve an object by its ID from the database"""
    object_data = db.query(models.Object).filter(models.Object.id == object_id).first()
    if object_data is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return object_data

async def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    """Create a new exercise in the database"""
    db_exercise = models.Exercise(
        object_id=exercise.object_id,
        phrase=exercise.phrase,
        audio_url=exercise.audio_url
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise