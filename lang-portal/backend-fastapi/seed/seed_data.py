import os
import sys
import json
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base, Word, StudyActivity
from app.database import engine

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def seed_words(db: Session, data: list):
    for item in data:
        print(f"Inserting word: {item['kanji']}")  # Log the word being inserted
        word = Word(
            kanji=item.get('kanji'),
            romaji=item.get('romaji'),
            english=item.get('english'),
            parts={str(i): part for i, part in enumerate(item.get('parts', []))}  # Convert list to dictionary
        )
        db.add(word)
    db.commit()
    print("Words have been successfully inserted.")

def seed_study_activities(db: Session, data: list):
    for item in data:
        print(f"Inserting study activity: {item['name']}")  # Log the study activity being inserted
        study_activity = StudyActivity(
            name=item.get('name'),
            url=item.get('url'),
            thumbnail_url=item.get('thumbnail_url')
        )
        db.add(study_activity)
    db.commit()
    print("Study activities have been successfully inserted.")

def load_json_data(file_path, seed_function):
    if (os.path.exists(file_path)):
        print(f"Loading data from {file_path}")
        data = read_json_file(file_path)
        print(f"Loaded {len(data)} items from JSON.")
        seed_function(db, data)
    else:
        print(f"File {file_path} does not exist.")

def main():
    # Ensure the database schema is created
    Base.metadata.create_all(bind=engine)

    # Path to the seeds folder
    seeds_folder = os.path.dirname(__file__)

    # Seed words
    words_file_path = os.path.join(seeds_folder, 'data_adjectives.json')
    load_json_data(words_file_path, seed_words)
    words_file_path = os.path.join(seeds_folder, 'data_verbs.json')
    load_json_data(words_file_path, seed_words)

    # Seed study activities
    study_activities_file_path = os.path.join(seeds_folder, 'study_activities.json')
    load_json_data(study_activities_file_path, seed_study_activities)

    db.close()

if __name__ == '__main__':
    main()