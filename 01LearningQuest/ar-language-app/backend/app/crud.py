from sqlalchemy.orm import Session
from app import models, schemas

def create_object(db: Session, obj: schemas.ObjectCreate):
    db_object = models.Object(**obj.dict())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

def get_objects(db: Session):
    return db.query(models.Object).all()

def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    db_exercise = models.Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise