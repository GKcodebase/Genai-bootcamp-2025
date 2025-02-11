from sqlalchemy.orm import Session
from . import models, schemas

def get_all_words(db: Session):
    return db.query(models.Word).all()

def get_words(db: Session, page: int = 1, sort_by: str = "kanji", order: str = "asc"):
    offset = (page - 1) * 10  # Pagination logic
    return db.query(models.Word).order_by(getattr(models.Word, sort_by).asc() if order == "asc" else getattr(models.Word, sort_by).desc()).offset(offset).limit(10).all()

def get_groups(db: Session, page: int = 1, sort_by: str = "name", order: str = "asc"):
    offset = (page - 1) * 10
    return db.query(models.Group).order_by(getattr(models.Group, sort_by).asc() if order == "asc" else getattr(models.Group, sort_by).desc()).offset(offset).limit(10).all()

def create_study_session(db: Session, study_session: schemas.StudySessionBase):
    db_study_session = models.StudySession(**study_session.dict())
    db.add(db_study_session)
    db.commit()
    db.refresh(db_study_session)
    return db_study_session

def log_review(db: Session, word_review_item: schemas.WordReviewItem):
    db_review = models.WordReviewItem(**word_review_item.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review