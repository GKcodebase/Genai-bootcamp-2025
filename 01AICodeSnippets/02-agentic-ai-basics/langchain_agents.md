# LangChain Agents Architecture 🤖

## What is LangChain?

LangChain is a framework for developing applications powered by language models. It provides:

### Core Capabilities
1. **Model Integration**
   - Connect with various LLMs (OpenAI, Anthropic, Google, etc.)
   - Standardized interface for model interactions
   - Easy switching between different providers

2. **Chains**
   - Combine multiple operations into sequences
   - Create complex workflows
   - Handle input/output transformations

3. **Agents**
   - Autonomous task execution
   - Tool usage and selection
   - Dynamic decision making

4. **Memory**
   - Conversation history management
   - State persistence
   - Context windows

### Use Cases

1. **Document Processing**
   - Question answering over documents
   - Summarization
   - Information extraction
   - Document comparison

2. **Chatbots**
   - Customer service
   - Technical support
   - Educational assistants
   - Interactive agents

3. **Data Analysis**
   - Data exploration
   - Pattern recognition
   - Report generation
   - Insights extraction

4. **Code Understanding**
   - Code analysis
   - Documentation generation
   - Bug finding
   - Code explanation

### Architecture Overview

![RAG System Overview](./images/LC-Arch.png)

### Key Components

1. **Models (LLMs)**
   - Text generation
   - Embeddings
   - Chat models
   - Function calling

2. **Prompts**
   - Templates
   - Few-shot examples
   - Dynamic prompting
   - Prompt optimization

3. **Memory Systems**
   - Buffer memory
   - Summary memory
   - Vector store memory
   - Custom memory

4. **Tools & Toolkits**
   - Web tools
   - Math tools
   - API integrations
   - Custom tools

### Integration Methods

1. **Python SDK**
```python
from langchain.llms import OpenAI
from langchain.agents import Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory

# Initialize components
llm = OpenAI()
memory = ConversationBufferMemory()
tools = [Tool(...)]

# Create agent
agent = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory
)
```

2. **LangServe**
   - Deploy as API
   - Serverless functions
   - Cloud deployment
   - Monitoring & logging

## System Overview

![RAG System Overview](./images/LC-systemoverview.png)

## Agent Components

### 1. Base Agent Architecture

![RAG System Overview](./images/LC-BaseAgent.png)

### 2. Tools Agent Architecture

![RAG System Overview](./images/LC-ToolsAgent.png)

## Tool Flow Diagrams

### Weather Tool Flow

![RAG System Overview](./images/LC-WeatherFlow.png)

### Date Calculator Flow

![RAG System Overview](./images/LC-DateCalculator.png)

## Implementation Details

### LLM Provider Selection
1. **Google AI (Gemini)**
   - Model: `gemini-pro`
   - Best for: General purpose, fast responses
   - Rate limits: 15 requests/minute

2. **Anthropic (Claude)**
   - Model: `claude-3-haiku-20240307`
   - Best for: Complex reasoning
   - Rate limits: Varies by account

3. **Groq (Llama)**
   - Model: `llama-3.1-8b-instant`
   - Best for: Fast inference
   - Rate limits: 6,000 tokens/minute

### Available Tools

1. **Weather Information**
   - Input: `City,Country` format
   - Provider: OpenWeather API
   - Returns: Temperature, humidity, conditions

2. **Time Zone Converter**
   - Input: `Region/City` format
   - Provider: pytz library
   - Returns: Current time in specified timezone

3. **Date Calculator**
   - Input: `add N` or `subtract N`
   - Implementation: Python datetime
   - Returns: Calculated date with current date reference

4. **URL Shortener**
   - Input: Full URL
   - Provider: TinyURL API
   - Returns: Shortened URL

5. **Text Analyzer**
   - Input: Text string
   - Implementation: Custom Python
   - Returns: Character count, word count, metrics

### Memory System

```mermaid
graph LR
    A[User Input] --> B[Short-term Memory]
    B --> C[ConversationBufferMemory]
    C --> D[Agent Context]
    D --> E[Tool Selection]
```

### Error Handling

```mermaid
graph TD
    A[API Request] --> B{Success?}
    B -->|Yes| C[Process Response]
    B -->|No| D{Retry Count < 3?}
    D -->|Yes| E[Wait and Retry]
    E --> A
    D -->|No| F[Fallback Provider]
```

## Usage Examples

### Basic Tool Usage
```python
agent = ToolsLangChainAgent()

# Weather lookup
result = agent.run("What's the weather in London,UK?")

# Date calculation
result = agent.run("What date will it be in 14 days?")

# Text analysis
result = agent.run("Analyze this text: 'Hello, World!'")
```

### Complex Multi-Tool Tasks
```python
# Combining multiple tools
complex_task = """
1. Get weather in Tokyo
2. Calculate date in 2 weeks
3. Analyze the weather response
"""
result = agent.run(complex_task)
```

## Best Practices

1. **API Key Management**
   - Store keys in `.env` file
   - Never hardcode keys
   - Rotate keys periodically

2. **Error Handling**
   - Implement retries with backoff
   - Use provider fallbacks
   - Log errors for debugging

3. **Rate Limiting**
   - Respect API limits
   - Implement request throttling
   - Monitor usage

4. **Memory Management**
   - Clear memory when needed
   - Monitor token usage
   - Implement context windows 