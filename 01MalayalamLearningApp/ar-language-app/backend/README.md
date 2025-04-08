# Interactive Malaylam Learning App - Backend

FastAPI backend server for AR language learning application.

## Technologies Used

- Python 3.10.12
- FastAPI
- SQLite3
- Google Gemini API
- Whisper (OpenAI)
- gTTS (Google Text-to-Speech)
- SQLAlchemy

## Features

- Object recognition using Gemini Vision API
- Malayalam translation generation
- Audio generation for Malayalam text
- Speech verification using Whisper
- Exercise generation for practice
- History tracking and storage

## Project Structure

```
backend/
├── app/
│   ├── routers/
│   │   ├── objects.py
│   │   ├── audio.py
│   │   └── exercises.py
│   ├── utils/
│   │   └── transliteration.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
├── db/
│   └── app.db
├── requirements.txt
└── .env
```

## Setup and Installation

1. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
cp .env.example .env

# Add your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

4. Initialize database:
```bash
# Database will be created automatically on first run
```

5. Start the server:
```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Object Recognition
- `POST /api/recognize_object`
  - Upload image for object detection
  - Returns object name and Malayalam translation

### Audio
- `GET /api/generate_audio`
  - Generate audio for Malayalam text
- `POST /api/speaking_test`
  - Verify pronunciation accuracy

### Exercises
- `GET /api/generate_exercise`
  - Generate practice exercises
- `GET /api/history`
  - Retrieve scan history

## Database Schema

### Objects Table
```sql
CREATE TABLE objects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    malayalam_translation TEXT,
    timestamp DATETIME
);
```

### Exercises Table
```sql
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    object_id INTEGER,
    phrase TEXT,
    audio_url TEXT,
    FOREIGN KEY(object_id) REFERENCES objects(id)
);
```

## Dependencies

Key packages:
```txt
fastapi==0.103.0
uvicorn==0.23.2
sqlalchemy==2.0.20
google-generativeai==0.3.0
openai-whisper==20231117
gTTS==2.5.1
python-multipart==0.0.6
```

## Error Handling

The API includes comprehensive error handling for:
- Invalid image uploads
- AI processing failures
- Database errors
- Audio generation issues
- Speech recognition errors

## License

MIT License

Copyright (c) 2025 GK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...