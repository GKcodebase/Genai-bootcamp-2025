from ..database import Base, engine
from .. import models

def create_database():
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Create new tables
    print("Database recreated successfully!")

if __name__ == "__main__":
    create_database()