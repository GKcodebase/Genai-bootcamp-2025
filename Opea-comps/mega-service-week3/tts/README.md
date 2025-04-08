# Text-to-Speech Service

Voice cloning and text-to-speech service with multiple duration support.

## 🎯 Features

- Voice cloning (10s, 30s, 1m samples)
- Multiple language support
- GPT-based text generation
- Custom voice modeling

## 🚀 Usage

### Base TTS
```bash
curl http://localhost:7055/v1/audio/speech \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello world", "voice": "default"}' \
  --output ./out/speech.mp3
```

### Voice Cloning
```bash
curl -X POST "http://127.0.0.1:9880" \
  -H "Content-Type: application/json" \
  -d '{
    "refer_wav_path": "/audio/sample.wav",
    "text": "Your text here",
    "text_language": "en"
  }' \
  --output out/output.wav
```