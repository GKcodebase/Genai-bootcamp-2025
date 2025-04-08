# Language Learning Assistant Backend

Backend services for Japanese language learning application.

## 📦 Components

### 1. Interactive Learning (`interactive.py`)
- Question generation
- Audio synthesis
- Voice configuration
- AWS Bedrock integration

### 2. Transcript Processing (`get_transcript.py`)
- YouTube transcript downloading
- Text extraction
- File management

### 3. RAG Implementation (`rag.py`)
- ChromaDB integration
- Content embedding
- Context retrieval

## 🛠️ Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

## 🚀 Running the Backend

1. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # For Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
# Install AWS CLI if not installed
brew install awscli

# Configure AWS credentials
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-west-2)
# - Default output format (json)
```

4. Set up environment variables:
```bash
# Create .env file
cat << EOF > .env
AWS_REGION=us-west-2
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
CHROMADB_PATH=./data/chromadb
TRANSCRIPTS_PATH=./data/transcripts
QUESTIONS_PATH=./data/questions
EOF
```

5. Initialize the database:
```bash
# Create required directories
mkdir -p data/chromadb data/questions data/transcripts

# Initialize ChromaDB
python -c "from rag import initialize_db; initialize_db()"
```

6. Start the FastAPI server:
```bash
# Install uvicorn if not installed
pip install uvicorn

# Start server
uvicorn main:app --reload --port 8000
```

7. Verify the installation:
```bash
# Test the API endpoint
curl http://localhost:8000/health
```

## 📁 Directory Structure

```
backend/
├── __init__.py
├── chat.py
├── get_transcript.py
├── interactive.py
├── rag.py
├── requirements.txt
└── data/
    ├── chromadb/
    ├── questions/
    └── transcripts/
```

## 🔍 API Endpoints

### Health Check
```http
GET /health
```

### Chat Completion
```http
POST /chat
Content-Type: application/json

{
    "message": "How do I use は particle?"
}
```

### Process YouTube Transcript
```http
POST /process-transcript
Content-Type: application/json

{
    "video_id": "youtube_video_id",
    "language": "ja"
}
```

### Generate Questions
```http
POST /generate-questions
Content-Type: application/json

{
    "transcript_id": "transcript_uuid"
}
```

## 🐛 Troubleshooting

Common issues and solutions:

1. AWS Credentials Error:
```bash
# Verify AWS configuration
aws sts get-caller-identity
```

2. ChromaDB Initialization Error:
```bash
# Clear ChromaDB cache
rm -rf ./data/chromadb/*
python -c "from rag import initialize_db; initialize_db()"
```

3. Port Already in Use:
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

## 📊 Monitoring

View logs:
```bash
tail -f logs/app.log
```

Monitor API requests:
```bash
# Install httpie for prettier output
brew install httpie
http :8000/health
```