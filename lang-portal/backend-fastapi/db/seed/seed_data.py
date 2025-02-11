from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_data(db: Session):
    # Add initial data here
    word1 = schemas.WordCreate(kanji="こんにちは", romaji="konnichiwa", english="hello", parts={})
    crud.create_word(db, word1)
    group1 = schemas.GroupCreate(name="Basic Greetings")
    crud.create_group(db, group1)

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    seed_data(db)
    db.close()
