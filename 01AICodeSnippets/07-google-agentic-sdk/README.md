# Google Agentic SDK Project

This project demonstrates the use of Google's Vertex AI Agents with the Gemini API. It provides a comprehensive implementation for building AI agents that can perform tasks, use tools, and maintain conversation memory.

## Features

- **Basic Agent Tasks**: Run simple tasks using Gemini
- **Tool Integration**: Use custom tools with the agent
- **Conversation Memory**: Maintain context across multiple interactions
- **REST API**: FastAPI endpoints for agent interaction
- **Async Support**: All operations are asynchronous for better performance

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Get API Keys**
   - Google Cloud Project ID: [Get it here](https://console.cloud.google.com/)
   - Google AI API Key: [Get it here](https://makersuite.google.com/app/apikey)

## Usage

### Running the API Server
```bash
uvicorn src.api.app:app --reload
```

### API Endpoints

- `POST /agent/run`: Run a basic agent task
- `POST /agent/run-with-memory`: Run agent with conversation memory
- `GET /agent/info`: Get agent information
- `GET /health`: Health check endpoint

### Example Scripts

Run the example script:
```bash
python examples/agent_example.py
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Examples

### Basic Agent Task
```python
from src.agent import GoogleAgent

# Initialize agent
agent = GoogleAgent()

# Run task
result = await agent.run_agent(
    task="Explain quantum computing"
)
```

### Agent with Tools
```python
tools = [
    {
        "name": "calculator",
        "description": "Perform calculations"
    }
]

result = await agent.run_agent(
    task="Calculate 2+2",
    tools=tools
)
```

### Agent with Memory
```python
history = [
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": "AI is..."}
]

result = await agent.run_agent_with_memory(
    task="Tell me more about AI",
    conversation_history=history
)
```

## Project Structure

```
07-google-agentic-sdk/
├── src/
│   ├── api/
│   │   └── app.py
│   └── agent.py
├── examples/
│   └── agent_example.py
├── requirements.txt
├── .env.example
└── README.md
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - see LICENSE file for details 