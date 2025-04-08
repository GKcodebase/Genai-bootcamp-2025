# Mega Service

LLM integration service with distributed tracing support.

## 🛠️ Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start service:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### LLM Service
```bash
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model": "llama3.2:1b",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

## 🔍 Monitoring

- Jaeger UI: http://localhost:16686
- Service metrics: http://localhost:8000/metrics