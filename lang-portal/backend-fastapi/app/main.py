from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from typing import List

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/words", response_model=List[schemas.Word])
# def get_words(page: int = 1, sort_by: str = "kanji", order: str = "asc", db: Session = Depends(get_db)):
#     return crud.get_words(db, page, sort_by, order)

@app.get("/words", response_model=List[schemas.Word])
def get_words(db: Session = Depends(get_db)):
    words = crud.get_all_words(db)  # Get the words from the database
    word_list = []
    for word in words:
        # Ensure 'parts' is properly structured as per the above model
        parts_dict = {str(i): part for i, part in enumerate(word.parts)} if isinstance(word.parts, list) else word.parts
        word_list.append({
            'id': word.id,
            'kanji': word.kanji,
            'romaji': word.romaji,
            'english': word.english,
            'parts': parts_dict  # Ensure 'parts' is a dictionary
        })
    return word_list

@app.get("/groups", response_model=List[schemas.Group])
def get_groups(page: int = 1, sort_by: str = "name", order: str = "asc", db: Session = Depends(get_db)):
    return crud.get_groups(db, page, sort_by, order)

@app.get("/groups/{group_id}", response_model=List[schemas.Word])
def get_group_words(group_id: int, page: int = 1, db: Session = Depends(get_db)):
    # Fetch words associated with this group
    return db.query(models.Word).join(models.WordGroup).filter(models.WordGroup.group_id == group_id).offset((page - 1) * 10).limit(10).all()

@app.post("/study_sessions", response_model=schemas.StudySession)
def create_study_session(study_session: schemas.StudySessionBase, db: Session = Depends(get_db)):
    return crud.create_study_session(db, study_session)

@app.post("/study_sessions/{session_id}/review", response_model=schemas.WordReviewItem)
def log_review(session_id: int, word_review_item: schemas.WordReviewItem, db: Session = Depends(get_db)):
    word_review_item.study_session_id = session_id  # Assign session ID to the review item
    return crud.log_review(db, word_review_item)
