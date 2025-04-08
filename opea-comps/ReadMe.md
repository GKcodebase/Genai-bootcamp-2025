
# OPEA Components

Open Platform for Enterprise AI (OPEA) components repository containing various AI service implementations.

## 🚀 Services

- **Mega Service**: Base LLM integration service
- **TTS Service**: Text-to-Speech with voice cloning
- **DB QnA**: Database question answering system

## 🛠️ Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js 20.11.1+ (for React applications)
- Ollama (for local LLM)

## 📦 Installation

### Docker Setup (Mac)

```bash
# Install Docker Desktop for Mac
brew install docker

# Start Docker service
open -a Docker
```

### Ollama Setup

1. Install Ollama:
```bash
brew install ollama
```

2. Pull required model:
```bash
ollama pull llama3.2:1b
```

## 🚀 Quick Start

1. Start services:
```bash
HOST_IP=$(ipconfig getifaddr en0) \
NO_PROXY=localhost \
LLM_ENDPOINT_PORT=9000 \
LLM_MODEL_ID="llama3.2:1b" \
docker compose up
```

2. Verify installation:
```bash
# Test Ollama API
curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Hello!"
}'
```

## 🔍 Services Overview

### Mega Service
- Port: 8000
- FastAPI-based LLM service
- Jaeger UI available at http://localhost:16686

### TTS Service
- Port: 9880
- Voice cloning capabilities
- Multiple voice duration support


### DB QnA
- React-based frontend
- Natural language to SQL conversion
- Database visualization
# Running Ollama in Local

### Choosing a Model

[Ollama Library](https://ollama.com/library)

eg. LLM_MODEL_ID="llama3.2:1b"

### Getting Host IP

```sh
`$(hostname -I | awk '{print $1}')`
```

HOST_IP=$(hostname -I | awk '{print $1}') NO_PROXY=localhost LLM_ENDPOINT_PORT=9000 LLM_MODEL_ID="llama3.2:1b" docker compose up

### Ollama API

Once the Ollama server is running we can make API calls to the ollama API

https://github.com/ollama/ollama/blob/main/docs/api.md

## Download (Pull) a model

curl http://localhost:8008/api/pull -d '{
  "model": "llama3.2:1b"
}'

## Generate a Request

curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Why is the sky blue?"
}'

## Installing Docker 

### Set up Docker's apt repository.

```sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
### Install the Docker packages.

```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
### Running Docker without Sudo

```sh
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

## 📚 Documentation

- [Mega Service](./mega-service/README.md)
- [TTS Service](./mega-service-week3/tts/README.md)
- [DB QnA](./mega-service-week3/dbqna/README.md)