# Local LLM Deployment

A FastAPI-based service for deploying local LLMs using Ollama.

## Features

- FastAPI server for text generation
- Ollama integration for local model inference
- Model management through Ollama
- Configurable generation parameters
- Async API endpoints

## Prerequisites

- Python 3.8+
- Ollama installed and running

## Installation

1. Install Ollama:
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Pull a model using Ollama:
   ```bash
   ollama pull llama2
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   python src/server.py
   ```

2. Run the example script:
   ```bash
   python examples/basic_usage.py
   ```

## API Endpoints

- `GET /`: Server status and available endpoints
- `POST /generate`: Generate text
- `GET /models`: List available models

### Generate Text

```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "Explain quantum computing",
        "max_tokens": 256,
        "temperature": 0.7
    }
)
print(response.json())
```

## Model Management

The server integrates with Ollama's API for model management:

```bash
# List available models
curl http://localhost:8000/models

# Pull a new model
ollama pull llama2

# Get model info
ollama show llama2
```

## Performance Considerations

- Adjust generation parameters based on your needs:
  - `temperature`: Controls randomness (0.0 to 1.0)
  - `top_p`: Nucleus sampling parameter
  - `top_k`: Top-k sampling parameter
  - `max_tokens`: Maximum length of generated text

## License

MIT License 