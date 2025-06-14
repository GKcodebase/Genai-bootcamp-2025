# AI & GenAI Code Snippets - Developer Tutorials

A comprehensive collection of developer-level tutorials covering cutting-edge AI and GenAI topics.

**🎯 Focus on FREE APIs**: All tutorials primarily use free APIs (Groq, Google AI, Ollama) to make learning accessible!

## 🚀 Projects Overview

| Project | Topic | Technologies | Cost | Difficulty |
|---------|-------|-------------|------|------------|
| [01-rag-with-chroma](./01-rag-with-chroma/) | Retrieval Augmented Generation | ChromaDB, Groq, Free Embeddings | 🆓 | ⭐⭐ |
| [02-agentic-ai-basics](./02-agentic-ai-basics/) | Agentic AI Fundamentals | LangChain, Groq, Free Tools | 🆓 | ⭐⭐ |
| [03-agentic-rag](./03-agentic-rag/) | Agentic RAG Systems | ChromaDB, Groq, Function Calling | 🆓 | ⭐⭐⭐ |
| [04-ai-workflows](./07-ai-workflows/) | Complex AI Pipelines | LangGraph, Multiple Free APIs | 🆓 | ⭐⭐⭐ |
| [05-mcp-integration](./05-mcp-integration/) | Model Context Protocol | MCP, Claude (Free tier) | 🆓 | ⭐⭐⭐ |
| [06-multimodal-ai](./06-multimodal-ai/) | Vision & Audio Processing | Gemini Vision, Whisper | 🆓 | ⭐⭐ |
| [07-google-agentic-sdk](./07-google-agentic-sdk/) | Google Vertex AI Agents | Gemini API (Free tier) | 🆓 | ⭐⭐ |
| [08-Ollama-deployment](./08-Ollama-deployment/) | Local ollama Deployment | Ollama, FastAPI | 🆓 | ⭐⭐⭐ |

## 💰 Cost Breakdown

### 🆓 Completely Free
- **Ollama**: Run models locally (Llama2, CodeLlama, Mistral)
- **Sentence Transformers**: Free embeddings
- **Whisper**: Free speech-to-text
- **ChromaDB/Qdrant**: Free vector databases

### 🆓 Free Tiers (Generous Limits)
- **Groq**: 6,000 tokens/minute (very fast inference)
- **Google AI Studio**: 15 requests/minute for Gemini
- **Together AI**: $25 free credit
- **Claude**: Free tier available
- **Hugging Face**: Free inference API

### 💳 Optional Paid (for advanced features)
- OpenAI GPT-4
- Google Cloud Vertex AI

## 🛠️ Quick Start

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd 01AICodeSnippets
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Get Free API Keys** (5 minutes setup)
   ```bash
   # Get Groq API key (fastest setup)
   # Visit: https://console.groq.com/keys
   
   # Get Google AI API key 
   # Visit: https://makersuite.google.com/app/apikey
   
   # Setup environment
   cp .env.example .env
   # Edit .env with your free API keys
   ```

3. **Install Ollama (Optional - for local models)**
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama2
   ```

4. **Choose a Project**
   Navigate to any project folder and follow its README.

## 🎓 Learning Path

**🆓 Start Completely Free → 🚀 Scale with Premium APIs**

1. **Start Local**: `08-vllm-deployment` (Ollama + local models)
2. **Try Free APIs**: `01-rag-with-chroma` (Groq + free embeddings)
3. **Multi-modal**: `06-multimodal-ai` (Gemini Vision - free)
4. **Advanced**: `03-agentic-rag`, `07-ai-workflows`

## 🔧 Free API Setup Guide

### Groq API (Recommended - Very Fast)
1. Visit [console.groq.com](https://console.groq.com/keys)
2. Sign up and get API key
3. Models: Mixtral 8x7B, Llama2 70B (very fast inference)

### Google AI Studio
1. Visit [makersuite.google.com](https://makersuite.google.com/app/apikey)
2. Create API key
3. Models: Gemini Pro, Gemini Vision

### Ollama (Local)
1. Install Ollama
2. Pull models: `ollama pull llama2`
3. Models run locally (no API key needed)

## 📊 Performance Comparison

| Provider | Speed | Quality | Limit | Best For |
|----------|--------|---------|-------|----------|
| Groq | ⚡⚡⚡ | ⭐⭐⭐ | 6k tokens/min | Fast prototyping |
| Gemini | ⚡⚡ | ⭐⭐⭐⭐ | 15 req/min | Multi-modal tasks |
| Ollama | ⚡ | ⭐⭐⭐ | Unlimited | Local development |
| Claude | ⚡⚡ | ⭐⭐⭐⭐⭐ | Limited free | Complex reasoning |

## 📋 Prerequisites

- Python 3.9+
- API Keys (OpenAI, Google Cloud, Anthropic)
- Basic understanding of Python and AI concepts

## 🔑 Required API Keys

- `OPENAI_API_KEY` - OpenAI API access
- `GOOGLE_APPLICATION_CREDENTIALS` - Google Cloud credentials
- `ANTHROPIC_API_KEY` - Claude API access

## 🤝 Contributing

Feel free to add more examples, improve documentation, or fix bugs!

## 📄 License

MIT License - see individual projects for specific licenses. 