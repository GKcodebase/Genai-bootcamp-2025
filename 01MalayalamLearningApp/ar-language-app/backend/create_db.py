from app.database import Base, engine
from app import models

def create_database():
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("Database recreated successfully!")

if __name__ == "__main__":
    create_database()