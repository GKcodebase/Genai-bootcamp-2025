# Agentic Workflows

A Python framework for building complex AI workflows using specialized agents. This project provides a modular and extensible system for creating AI-powered workflows that can handle research, content generation, and document analysis tasks.

## Features

- **Modular Agent System**: Specialized agents for different tasks
  - Research Agents (Web Research, Document Analysis, Synthesis)
  - Content Agents (Research, Writing, Editing)
  - Extensible base classes for custom agents

- **Error Handling & Resilience**:
  - Automatic retries with exponential backoff
  - Comprehensive error reporting
  - Graceful degradation

- **Multiple LLM Support**:
  - Groq
  - Anthropic Claude
  - Google AI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd 04-agentic-workflows
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env.example .env
```

Edit `.env` with your API keys:
```
GROQ_API_KEY=your_groq_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
```

## Project Structure

```
04-agentic-workflows/
├── src/
│   ├── agents/
│   │   ├── base_workflow_agent.py
│   │   ├── content.py
│   │   └── research.py
│   └── workflows/
│       ├── research_workflow.py
│       └── content_workflow.py
├── tests/
│   └── test_setup.py
├── examples/
│   └── workflow_example.py
├── requirements.txt
├── setup.py
├── env.example
└── README.md
```

## Dependencies

The project uses the following key dependencies:
- `groq==0.27.0`: For Groq LLM integration
- `anthropic==0.8.1`: For Claude API integration
- `google-generativeai==0.3.2`: For Google AI integration
- `langchain==0.1.12`: For LLM workflow orchestration
- `pydantic==2.6.3`: For data validation
- `tenacity==8.2.3`: For retry mechanisms
- `python-dotenv==1.0.1`: For environment variable management

## Usage

### Research Workflow

```python
from src.workflows import ResearchWorkflow

# Initialize research workflow
research = ResearchWorkflow(
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)

# Execute research
results = research.execute_research("AI Safety and Ethics")

print(results['synthesis'])  # Get synthesized research
print(results['sources'])    # Get sources
```

### Content Generation Workflow

```python
from src.workflows import ContentWorkflow

# Initialize content workflow
content = ContentWorkflow(
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)

# Generate content
article = content.generate_content(
    topic="The Future of AI",
    style="technical blog post"
)

print(article['final_content'])  # Get the final content
```

## Testing

The project includes a comprehensive test suite. To run the tests:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_setup.py
```

## Agent Types

### Research Agents

1. **WebResearchAgent**
   - Web search and content extraction
   - Source verification
   - Information synthesis

2. **DocumentAnalysisAgent**
   - Key concept extraction
   - Relationship analysis
   - Insight generation

3. **SynthesisAgent**
   - Pattern identification
   - Research synthesis
   - Executive summary generation

### Content Agents

1. **ResearchAgent**
   - Topic research
   - Source gathering
   - Information organization

2. **WritingAgent**
   - Content outline generation
   - Draft writing
   - Style adaptation

3. **EditingAgent**
   - Grammar and style checking
   - Content refinement
   - Final polishing

## Error Handling

The system implements comprehensive error handling:

```python
try:
    result = agent.run(task)
    if result['status'] == 'error':
        print(f"Error: {result['error']}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 