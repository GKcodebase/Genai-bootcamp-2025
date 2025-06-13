# Multimodal AI Project

This project demonstrates the integration of vision and audio processing capabilities using Google's Gemini Vision and OpenAI's Whisper models. It provides a comprehensive API for image analysis and audio transcription.

## Features

### Vision Processing (Gemini Vision)
- Single image analysis
- Multiple image comparison
- Streaming responses
- Detailed image descriptions
- Emotion and context analysis

### Audio Processing (Whisper)
- Audio transcription
- Multi-language support
- Audio translation
- Timestamp-based segmentation
- Initial prompt support

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Get API Keys**
   - Google AI API Key: [Get it here](https://makersuite.google.com/app/apikey)
   - (Optional) OpenAI API Key: [Get it here](https://platform.openai.com/api-keys)

## Usage

### Running the API Server
```bash
uvicorn src.api.app:app --reload
```

### API Endpoints

#### Vision Endpoints
- `POST /analyze/image`: Analyze a single image
- `POST /analyze/images`: Compare multiple images
- `GET /health`: Health check endpoint

#### Audio Endpoints
- `POST /transcribe/audio`: Transcribe audio files

### Example Scripts

1. **Image Analysis**
   ```bash
   python examples/image_analysis.py
   ```

2. **Audio Transcription**
   ```bash
   python examples/audio_transcription.py
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Examples

### Image Analysis
```python
from src.models.vision_model import VisionModel

# Initialize model
model = VisionModel()

# Analyze image
result = await model.analyze_image(
    image=image,
    prompt="Describe what you see in this image."
)
```

### Audio Transcription
```python
from src.models.audio_model import AudioModel

# Initialize model
model = AudioModel()

# Transcribe audio
result = await model.transcribe(
    audio_path="path/to/audio.wav",
    language="en"
)
```

## Project Structure

```
06-multimodal-ai/
├── src/
│   ├── api/
│   │   └── app.py
│   └── models/
│       ├── vision_model.py
│       └── audio_model.py
├── examples/
│   ├── images/
│   ├── audio/
│   ├── image_analysis.py
│   └── audio_transcription.py
├── requirements.txt
├── .env.example
└── README.md
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - see LICENSE file for details 