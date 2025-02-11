from sqlalchemy.orm import Session
from . import models, schemas

def get_all_words(db: Session):
    return db.query(models.Word).all()

def get_word(db: Session, word_id: int):
    return db.query(models.Word).filter(models.Word.id == word_id).first()

def get_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Word).offset(skip).limit(limit).all()

def create_word(db: Session, word: schemas.WordCreate):
    db_word = models.Word(**word.dict())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_study_session(db: Session, study_session_id: int):
    return db.query(models.StudySession).filter(models.StudySession.id == study_session_id).first()

def get_study_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StudySession).offset(skip).limit(limit).all()

def create_study_session(db: Session, study_session: schemas.StudySessionCreate):
    db_study_session = models.StudySession(**study_session.dict())
    db.add(db_study_session)
    db.commit()
    db.refresh(db_study_session)
    return db_study_session

def get_study_activity(db: Session, study_activity_id: int):
    return db.query(models.StudyActivity).filter(models.StudyActivity.id == study_activity_id).first()

def get_study_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StudyActivity).offset(skip).limit(limit).all()

def create_study_activity(db: Session, study_activity: schemas.StudyActivityCreate):
    db_study_activity = models.StudyActivity(**study_activity.dict())
    db.add(db_study_activity)
    db.commit()
    db.refresh(db_study_activity)
    return db_study_activity

def log_review(db: Session, word_review_item: schemas.WordReviewItem):
    db_review = models.WordReviewItem(**word_review_item.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_word_review_item(db: Session, word_review_item_id: int):
    return db.query(models.WordReviewItem).filter(models.WordReviewItem.id == word_review_item_id).first()

def get_word_review_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WordReviewItem).offset(skip).limit(limit).all()

def create_word_review_item(db: Session, word_review_item: schemas.WordReviewItemCreate):
    db_word_review_item = models.WordReviewItem(**word_review_item.dict())
    db.add(db_word_review_item)
    db.commit()
    db.refresh(db_word_review_item)
    return db_word_review_item