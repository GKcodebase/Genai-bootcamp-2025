import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# API Endpoints
API_ENDPOINT = "http://localhost:5000/api/groups"

# OCR Settings
OCR_LIBRARY = "MangaOCR"

# Language Settings
GRAMMAR_SCOPE = "JLPTN5"

# LLM Configuration
LLM_CONFIG = {
    "model": "llama2-70b-4096",
    "temperature": 0.7,
    "max_tokens": 1000
}