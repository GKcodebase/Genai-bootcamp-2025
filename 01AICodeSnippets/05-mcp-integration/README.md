# Model Context Protocol (MCP) Integration

This project demonstrates how to implement and use the Model Context Protocol (MCP) with Groq to create more structured and reliable AI interactions. MCP helps in maintaining context, managing state, and ensuring consistent responses across multiple interactions.

## Features

- **Structured Context Management**: Maintain conversation context using MCP
- **State Management**: Track and update conversation state
- **Error Handling**: Robust error handling and retry mechanisms
- **Type Safety**: Pydantic models for type-safe interactions
- **Testing**: Comprehensive test suite

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd 05-mcp-integration
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp env.example .env
```

Edit `.env` with your API key:
```
GROQ_API_KEY=your_groq_api_key
```

## Project Structure

```
05-mcp-integration/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   └── mcp_agent.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── context.py
│   │   └── state.py
│   └── __init__.py
├── tests/
│   └── test_mcp.py
├── examples/
│   └── basic_usage.py
├── requirements.txt
├── setup.py
├── env.example
└── README.md
```

## Usage

### Basic MCP Integration

```python
from src.agents.mcp_agent import MCPAgent
from src.models.context import ConversationContext

# Initialize the MCP agent
agent = MCPAgent(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# Create a conversation context
context = ConversationContext(
    conversation_id="unique_id",
    metadata={"purpose": "example"}
)

# Start a conversation
response = agent.chat(
    message="What is Model Context Protocol?",
    context=context
)

print(response.content)
```

### Managing State

```python
# Update context with new information
context.update_state({
    "last_topic": "MCP",
    "user_preferences": {"language": "en"}
})

# Continue conversation with updated context
response = agent.chat(
    message="Can you explain more about state management?",
    context=context
)
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Key Concepts

### Model Context Protocol (MCP)

MCP is a protocol for managing context and state in AI conversations. It provides:
- Structured context management
- State tracking
- Consistent response formatting
- Error handling

### Context Management

The `ConversationContext` class handles:
- Conversation history
- Metadata
- State management
- Context updates

### State Management

The state system provides:
- Persistent state across interactions
- Type-safe state updates
- State validation
- State history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 