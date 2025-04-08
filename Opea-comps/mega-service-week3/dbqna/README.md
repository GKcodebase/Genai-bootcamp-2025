# Database Question Answering System

Natural language to SQL converter with visualization.

## 🛠️ Technology Stack

- React + Vite
- Node.js 20.11.1
- Nginx
- Docker

## 🚀 Quick Start

1. Build Docker image:
```bash
docker build -f docker/Dockerfile.react \
  --build-arg texttosql_url=http://localhost:8000 \
  -t dbqna-frontend .
```

2. Run container:
```bash
docker run -p 80:80 dbqna-frontend
```

## 💻 Development

1. Install dependencies:
```bash
cd react
npm install
```

2. Start development server:
```bash
npm run dev
```

## 🔨 Building

```bash
npm run build
```