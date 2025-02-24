## Running LLM service

check the docker file and Readme on  root file.

## How to access the Jaeger UI

When you run docker compose it should start up Jager.

```sh
http://localhost:16686/
```

## How to Run the Mega Service Example

```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Testing the App

Install Jq so we can pretty JSON on output.
```sh
sudo apt-get install jq
```
https://jqlang.org/download/


cd opea-comps/mega-service
Command to get full response 
```sh
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "why earth is flat?"
      }
    ],
    "model": "llama3.2:1b",
    "max_tokens": 100,
    "temperature": 0.7
  }' > output/raw-response.txt
```
```sh
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "messages": "Hello, how are you?"
  }' | jq '.' > output/$(date +%s)-response.json
```

```sh
  curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "why earth is flat?"
      }
    ],
    "model": "llama3.2:1b",
    "max_tokens": 100,
    "temperature": 0.7
  }' | jq '.' > output/$(date +%s)-response.json
```