# Song To Vocab APP
### Functionality
App where you can run get vocab and tranlation in the language you are learning from your favourite song.
Insert 
- song name
- Primary language (language in which song is written.)
- Target language (language in which you need tanslation.)
- Click Enter

## Run UI
```sh
streamlit run ui.py
```

## Run Backend

### Run local Ollama 

#### Choosing a Model

[Ollama Library](https://ollama.com/library)

eg. LLM_MODEL_ID="llama3.2:1b"


#### Ollama API

Once the Ollama server is running we can make API calls to the ollama API

https://github.com/ollama/ollama/blob/main/docs/api.md


#### Download (Pull) a model

curl http://localhost:8008/api/pull -d '{
  "model": "llama3.2:1b"
}'

#### Generate a Request

curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Why is the sky blue?"
}'

### Running Python Backedn

#### Creating venv
```sh
    python3 -m venv .venv
    source .venv/bin/activate
```

#### Run Uvicorn Application

```sh
    pip install -r requirements.txt
    uvicorn main:app --reload
```