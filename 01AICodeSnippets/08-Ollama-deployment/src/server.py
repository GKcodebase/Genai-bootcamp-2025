import os
import time
import random
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import requests
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Local LLM Deployment",
    description="Local LLM deployment using Ollama and FastAPI",
    version="1.0.0"
)

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama2"

class GenerateRequest(BaseModel):
    """Request model for text generation."""
    prompt: str
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 50
    stop: Optional[List[str]] = None

class GenerateResponse(BaseModel):
    """Response model for text generation."""
    generated_text: str
    metadata: Dict[str, Any]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI."""
    # Check if Ollama is running
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        logger.info("Ollama server is running")
    except Exception as e:
        logger.error(f"Error connecting to Ollama server: {str(e)}")
        raise RuntimeError("Ollama server is not running. Please start it first.")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "online",
        "model": DEFAULT_MODEL,
        "endpoints": {
            "/generate": "POST - Generate text",
            "/models": "GET - List available models"
        }
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text using Ollama."""
    try:
        # Prepare request to Ollama
        ollama_request = {
            "model": DEFAULT_MODEL,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "top_p": request.top_p,
                "top_k": request.top_k,
                "num_predict": request.max_tokens
            }
        }
        
        # Generate text using Ollama
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=ollama_request
        )
        response.raise_for_status()
        result = response.json()
        
        return GenerateResponse(
            generated_text=result["response"],
            metadata={
                "model": DEFAULT_MODEL,
                "prompt_length": len(request.prompt),
                "generated_length": len(result["response"]),
                "total_duration": result.get("total_duration", 0),
                "load_duration": result.get("load_duration", 0),
                "prompt_eval_duration": result.get("prompt_eval_duration", 0),
                "eval_duration": result.get("eval_duration", 0)
            }
        )
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models from Ollama."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server."""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server() 