# Agentic AI Basics - Implementation 🤖

Build intelligent AI agents that can perform tasks autonomously using **completely free** APIs and tools. This project demonstrates multiple AI agents with different capabilities, memory management, and interactive command-line interfaces.

[Agent System Overview](./agent_flows.md)

## ✨ Features

- **Multiple Agent Types**: Research, Calculator, and Multi-Agent systems
- **Task Planning**: Autonomous task breakdown and execution
- **Tool Usage**: Dynamic tool integration and selection
- **Memory Management**: Short and long-term memory systems
- **Error Handling**: Robust error recovery and retry mechanisms
- **Command Line Interface**: Full CLI support with interactive modes
- **File Operations**: Save research results to files
- **Multi-step Reasoning**: Chain-of-thought processing

## 🛠️ Tools & APIs Used

- **Groq API** (Free tier available) - Using `llama3-8b-8192` or `mistral-saba-24b`
- **DuckDuckGo Search** (Free web search)
- **Wikipedia API** (Free knowledge access)
- **Python httpx** (HTTP client for API calls)
- **Mathematical Computing** (Built-in calculator functions)

## 🎯 Available Agents

### 1. **Research Agent**
- Web search capabilities via DuckDuckGo
- Wikipedia knowledge integration
- Memory management for research history
- Detailed analysis modes

### 2. **Calculator Agent**
- Mathematical expression evaluation
- Trigonometric functions
- Logarithmic calculations
- Safe expression parsing
- Interactive calculation mode

### 3. **Multi-Agent System**
- Combines research and calculator capabilities
- Automatic mode detection
- Interactive command interface

### 4. **LangChain Agents**
The project now includes LangChain-based implementations in the `src/langchain_agents` directory:

#### Base Agent
- `BaseLangChainAgent`: A flexible base agent that supports multiple LLM providers:
  - Google AI (Gemini)
  - Anthropic (Claude)
  - Groq (Llama)

#### Tools Agent
- Location: `tools_langchain_agent.py`
- Features:
  - Weather information lookup
  - Time zone conversions
  - Date calculations
  - URL shortening
  - Text analysis

#### Usage Example
```python
from langchain_agents.tools_langchain_agent import ToolsLangChainAgent

# Initialize the agent
agent = ToolsLangChainAgent(
    model_name="gemini-pro",
    temperature=0.7
)

# Run a simple task
result = agent.run("What date will it be in 14 days?")
print(result["output"])

# Run a complex task
complex_task = """
I need to know the weather in Tokyo, Japan, and then calculate what date it will be 14 days from now.
Also, please analyze this text: 'The quick brown fox jumps over the lazy dog.'
"""
result = agent.run(complex_task)
print(result["output"])
```

#### Additional API Keys for LangChain Agents
Add these to your `.env` file:
```env
# At least one of these API keys is required:
GOOGLE_AI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Optional for weather functionality:
OPENWEATHER_API_KEY=your_key_here
```

## 📚 Examples & Usage

### Basic Research Agent
```bash
# Simple research
python examples/01_basic_agent.py "quantum computing trends"

# Interactive mode
python examples/01_basic_agent.py
# Then enter your research topic when prompted

# Use default topic
python examples/01_basic_agent.py --default
```

### Advanced Research Agent (with Memory)
```bash
# Basic research with memory
python examples/02_research_agent.py "artificial intelligence ethics"

# Detailed research analysis
python examples/02_research_agent.py --detailed "blockchain technology"

# Save results to file
python examples/02_research_agent.py "machine learning" --save ml_research.txt

# Show memory contents
python examples/02_research_agent.py --memory "deep learning"

# Interactive research mode
python examples/02_research_agent.py --interactive

# Combine all options
python examples/02_research_agent.py --detailed --memory --save results.txt "renewable energy"
```

### Calculator Agent
```bash
# Simple calculation
python examples/02_calculator_agent.py "2 + 2 * 3"

# Complex mathematical expressions
python examples/02_calculator_agent.py "sqrt(16) + sin(pi/2)"

# Interactive calculator mode
python examples/02_calculator_agent.py --interactive

# Get mathematical help
python examples/02_calculator_agent.py --help-math trigonometry
```

### Multi-Agent System
```bash
# Auto-detect mode (research or calculate)
python examples/03_multi_agent.py --query "quantum computing"
python examples/03_multi_agent.py --query "sqrt(25) + 10"

# Specific mode
python examples/03_multi_agent.py --mode research --query "AI trends"
python examples/03_multi_agent.py --mode calculate --query "2**8"

# Interactive multi-agent mode
python examples/03_multi_agent.py --interactive
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone and navigate to project
cd 02-agentic-ai-basics

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### 2. Configure API Keys
```bash
# Copy example environment file
cp .env.example .env

# Add your Groq API key (get from: https://console.groq.com/keys)
# Edit .env file:
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Test Installation
```bash
# Test basic functionality
python examples/01_basic_agent.py "test research topic"

# Test calculator
python examples/02_calculator_agent.py "2+2"
```

## 📁 Project Structure 

```folder
├── src/
│ ├── agents/
│ │ ├── init.py
│ │ ├── base_agent.py # Base agent class with Groq API
│ │ ├── research_agent.py # Research capabilities
│ │ └── calculator_agent.py # Mathematical calculations
│ ├── tools/
│ │ ├── init.py
│ │ └── calculator.py # Calculator utilities
│ ├── memory/
│ │ ├── init.py
│ │ └── simple_memory.py # Memory management system
│ └── utils/
│ ├── init.py
│ └── error_handler.py # Error handling and retry logic
├── examples/
│ ├── 01_basic_agent.py # Basic research agent with CLI
│ ├── 02_calculator_agent.py # Calculator agent with interactive mode
│ ├── 02_research_agent.py # Advanced research with memory & file saving
│ └── 03_multi_agent.py # Combined research and calculator system
├── tests/ # Test files (coming soon)
├── images/ # Documentation images
├── requirements.txt # Python dependencies
├── setup.py # Package configuration
├── .env.example # Environment variables template
├── .env # Your API keys (create from .env.example)
└── README.md # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Available Models
The system supports these Groq models:
- `llama3-8b-8192` (default)
- `mistral-saba-24b`
- Other Groq-supported models

## 🎮 Interactive Modes

### Research Agent Interactive Commands
```bash
python examples/02_research_agent.py --interactive
```
Commands:
- `research <topic>` - Research a topic
- `memory` - Show memory contents  
- `clear` - Clear memory
- `quit` - Exit

### Calculator Agent Interactive Commands
```bash
python examples/02_calculator_agent.py --interactive
```
Examples:
- `2 + 2`
- `sqrt(16)`
- `sin(pi/2)`
- `quit` - Exit

### Multi-Agent Interactive Commands
```bash
python examples/03_multi_agent.py --interactive
```
Commands:
- `research: <topic>` - Research mode
- `calculate: <expression>` - Calculator mode
- `quit` - Exit

## 🧠 Memory System

The research agents include a memory system that:
- **Short-term memory**: Stores last 10 interactions
- **Long-term memory**: Stores research by topic
- **Persistent storage**: Can save to files
- **Memory commands**: View and clear stored information

## 🔍 Error Handling

Built-in error handling features:
- **Retry mechanism**: Automatic retry on failures (up to 3 attempts)
- **API error handling**: Graceful handling of API issues
- **Input validation**: Safe expression evaluation for calculator
- **Timeout management**: Request timeouts to prevent hanging

## 📊 Use Cases

### Research Applications
- **Academic Research**: Literature reviews, trend analysis
- **Market Research**: Industry analysis, competitor research  
- **Technical Research**: Technology deep-dives, comparisons
- **News Analysis**: Current events, breaking news research

### Calculator Applications
- **Scientific Computing**: Complex mathematical calculations
- **Engineering**: Mathematical modeling and analysis
- **Education**: Interactive math learning and problem solving
- **Finance**: Mathematical analysis and calculations

### Multi-Agent Applications
- **Data Analysis**: Research + calculations in one workflow
- **Educational Tools**: Learning with both research and math
- **Problem Solving**: Complex problems requiring multiple approaches
- **Workflow Automation**: Combined research and computational tasks

## 🚀 Advanced Usage

### Batch Processing
```bash
# Research multiple topics
for topic in "AI" "ML" "Blockchain"; do
    python examples/02_research_agent.py "$topic" --save "${topic}_research.txt"
done
```

### Custom Prompts
Modify the prompts in agent files to customize behavior for specific domains.

### Extending Agents
Add new tools by:
1. Creating tool functions in agent classes
2. Adding them to `_get_default_tools()` method
3. Testing with the CLI interfaces

## 🤝 Contributing

Feel free to contribute by:
- Adding new agent types
- Improving existing functionality
- Adding more tools and integrations
- Enhancing error handling
- Adding tests

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   # Make sure your .env file has the correct API key
   cat .env
   ```

2. **Model Not Found**
   ```bash
   # Update to supported model in base_agent.py
   # Current supported: llama3-8b-8192, mistral-saba-24b
   ```

3. **Import Errors**
   ```bash
   # Make sure you installed the package
   pip install -e .
   ```

4. **Network Issues**
   ```bash
   # Check internet connection and API status
   # Groq API status: https://status.groq.com/
   ```

## 📞 Support

- Check the examples in the `examples/` directory
- Review error messages for specific guidance
- Ensure all dependencies are installed
- Verify API keys are correctly configured

---

**Ready to build intelligent agents? Start with any of the examples above!** 🚀