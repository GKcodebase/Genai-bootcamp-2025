# AR Language Learning App Technical Specs

## Business Goal
Develop an augmented reality (AR) mobile application that enhances language learning by allowing users to:
- Scan physical objects using their device camera.
- Identify objects, translate their names into Malayalam, and practice language skills (reading, writing, listening, speaking) using AI-driven features.
- Store identified objects, translations, and generated content in a database for reuse and historical tracking.

The app aims to provide an engaging, interactive experience using AR and AI technologies to make learning Malayalam intuitive and fun.

## Technical Requirements
- **Platforms**: The app will support iOS and Android mobile devices.
- **AI Integration**:
  - **Object Detection**: AI will detect and identify objects from camera scans.
  - **Translation**: AI will translate identified object names into Malayalam.
  - **Audio Generation**: AI will generate audio pronunciations for words and phrases.
  - **Speech Verification**: AI will verify user speech during speaking tests.
  - **Data Utilization**: Once an object is identified, AI will generate the word, audio, and a phrase, storing this data in the database for future use (e.g., history, practice sessions).
- **AR Functionality**: Real-time object scanning with AR overlays displaying Malayalam translations and interactive options.
- **Backend**: A lightweight server built with Python and FastAPI to handle AI processing and data storage.
- **Database**: SQLite3 for simplicity and local storage on the server, storing AI-generated data (objects, translations, audio, phrases).
- **API**: All endpoints will return JSON responses.
- **Authentication**: No authentication or authorization required; the app will operate as a single-user experience.
- **Deployment**: The backend will be deployable as a Docker container; the mobile app will be distributed as APK (Android) and IPA (iOS) files.
- **Hardware Compatibility**: All AI tools must run locally on an Intel Core i5 processor with at least 8 GB RAM.

## UI Requirements
- **Landing Page**:
  - **Scan Object Button**: Initiates the AR scanning process.
  - **History Section**: Displays a list of previously scanned objects with their Malayalam translations and timestamps, clickable to revisit practice options.
- **Post-Scan Screen**:
  - **AR Overlay**: Displays the AI-generated Malayalam word for the identified object overlaid on the real-world object in AR.
  - **Options**:
    - **Practice**: Leads to a practice screen with options for writing, speaking, and listening exercises based on the object.
    - **Cancel**: Returns to the landing page, discarding the current scan.
- **Practice Screen**:
  - **Writing**: Text input to type the Malayalam word, with AI feedback.
  - **Speaking**: Audio playback of the word/phrase, followed by a speaking test with AI verification.
  - **Listening**: Playback of a generated phrase with options to speak or write it back.

## Directory Structure

```
ar-language-app/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── models.py         # SQLAlchemy database models
│   │   ├── schemas.py        # Pydantic schemas for API validation
│   │   ├── crud.py           # Database CRUD operations
│   │   ├── database.py       # SQLite setup
│   │   └── routers/
│   │       ├── objects.py    # Endpoints for object recognition and translation
│   │       ├── audio.py      # Endpoints for audio generation and speech verification
│   │       └── exercises.py  # Endpoints for practice exercises
│   ├── db/
│   │   └── app.db            # SQLite database file
│   ├── ai_models/
│   │   ├── object_detection.tflite  # Pre-trained object detection model
│   │   └── tts_model.pth            # Pre-trained text-to-speech model (unchanged for now)
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Docker configuration for backend
├── frontend/
│   ├── web_app/              # Web UI (Flutter Web)
│   │   ├── lib/              # Flutter Dart files
│   │   ├── public/           # Static assets (e.g., HTML, icons)
│   │   └── pubspec.yaml      # Flutter dependencies
│   └── Dockerfile            # Docker configuration for frontend
├── docker-compose.yml        # Orchestrates backend and frontend containers
└── README.md                 # Setup and run instructions
```

## Database Schema
The app uses a single SQLite database named `app.db`, located in the `db/seed` folder. Below are the tables:

- **objects** - Stores AI-detected objects and their translations
  - `id` integer (primary key)
  - `name` string (English name of the object)
  - `malayalam_translation` string (AI-generated Malayalam translation)
  - `timestamp` datetime (when the object was scanned)
- **exercises** - Stores AI-generated phrases and audio for practice
  - `id` integer (primary key)
  - `object_id` integer (foreign key referencing `objects.id`)
  - `phrase` string (e.g., "ഇത് ഒരു കസേര ആണ്" - "This is a chair")
  - `audio_url` string (URL to AI-generated audio file)

## API Endpoints

### POST /api/recognize_object
- **Description**: Upload an image for AI to detect the object and generate its Malayalam translation, storing the result in the database.
- **Request**: Multipart form data containing an image file.
- **Response**:
```json
{
  "object_id": 1,
  "object_name": "chair",
  "malayalam_translation": "കസേര"
}
```

### GET /api/generate_audio
- **Description**: Use AI to generate audio for a specified Malayalam text, storing the audio URL in the database.
- **Query Parameters**:
  - `text`: string (e.g., "കസേര")
- **Response**:
```json
{
  "audio_url": "https://example.com/audio/file.mp3"
}
```

### POST /api/speaking_test
- **Description**: Submit an audio recording for AI to verify against the expected Malayalam word or phrase.
- **Request**: Multipart form data containing an audio file.
- **Response**:
```json
{
  "recognized_text": "കസേര",
  "correct": true
}
```

### GET /api/generate_exercise
- **Description**: Use AI to generate a practice phrase based on a recognized object, storing it in the database.
- **Query Parameters**:
  - `object_id`: integer (ID of the object from the `objects` table)
- **Response**:
```json
{
  "phrase": "ഇത് ഒരു കസേര ആണ്",
  "audio_url": "https://example.com/audio/phrase.mp3"
}
```

### GET /api/history
- **Description**: Retrieve a list of previously scanned objects from the database.
- **Response**:
```json
{
  "items": [
    {
      "object_id": 1,
      "object_name": "chair",
      "malayalam_translation": "കസേര",
      "timestamp": "2025-03-29T10:00:00Z"
    },
    {
      "object_id": 2,
      "object_name": "table",
      "malayalam_translation": "മേശ",
      "timestamp": "2025-03-29T10:05:00Z"
    }
  ]
}
```

## AR Functionality
- **Object Scanning**: AI detects objects in real-time via the device camera.
- **AR Overlay**: Displays the AI-generated Malayalam translation over the object, with buttons for "Practice" or "Cancel."
- **Interactive Features**:
  - **Writing**: User types the Malayalam word, with AI checking accuracy.
  - **Speaking**: AI generates audio, user repeats, and AI verifies pronunciation.
  - **Listening**: AI generates a phrase and audio; user can respond by speaking or writing.

## Technology Stack
### Mobile App
- **Framework**: Flutter or React Native for cross-platform development.
- **AR Tools**:
  - Flutter: `arcore_flutter_plugin` (Android), `ar_kit_plugin` (iOS).
  - React Native: `react-native-arcore` (Android), `react-native-arkit` (iOS).
- **UI Components**:
  - Landing page with "Scan Object" button and "History" list.
  - AR camera view with overlay text and buttons.
  - Text input, audio playback, and microphone access for practice screens.

### AI Tools
All AI tools are open-source, free, and verified to run locally on an Intel Core i5 processor with at least 8 GB RAM:
- **Object Recognition**: 
  - **TensorFlow Lite**: Open-source (Apache 2.0), lightweight for on-device inference, runs efficiently on an i5 with pre-trained models (e.g., MobileNet SSD).
  - **PyTorch Mobile**: Open-source (BSD), supports local execution with optimized models; requires model conversion but works on i5-grade hardware.
- **Translation**: 
  - **Hugging Face Models**: Open-source (Apache 2.0/MIT), pre-trained translation models (e.g., MarianMT) can run locally on an i5 with sufficient RAM; fallback to a custom English-to-Malayalam dictionary if needed (stored locally).
- **Text-to-Speech (TTS)**: 
  - **Mozilla TTS**: Open-source (MPL 2.0), generates high-quality audio locally, compatible with i5 processors (CPU-based inference).
  - **eSpeak**: Open-source (GPLv3), lightweight TTS engine with Malayalam support, runs easily on low-spec hardware like an i5.
- **Speech-to-Text (STT)**: 
  - **DeepSpeech**: Open-source (MPL 2.0), performs local speech recognition, optimized for CPU execution on an i5.
  - **Whisper**: Open-source (MIT), developed by OpenAI, runs locally on an i5 with smaller models (e.g., "tiny" or "base") for efficient speech verification.

### Backend
- **Framework**: FastAPI with Python.
- **Database**: SQLite3 for lightweight storage of AI-generated data.
- **Server**: Uvicorn for running the FastAPI app.
- **Containerization**: Docker for deployment.

## Deployment
- **Backend**: Deployed as a Docker container for easy setup and scalability.
- **Mobile App**: Built as an APK for Android and IPA for iOS, suitable for testing or distribution.

## Task Runner Tasks
- **Initialize Database**: Create and seed the SQLite database (`app.db`) with initial data if needed.
- **Run Backend Server**: Launch the FastAPI server using Uvicorn.
- **Build Mobile App**: Compile the app for Android (APK) and iOS (IPA).
- **Run Tests**: Execute unit and integration tests for backend, mobile app, and AI components.

## Hardware Compatibility Notes
- All listed AI tools (TensorFlow Lite, PyTorch Mobile, Hugging Face models, Mozilla TTS, eSpeak, DeepSpeech, Whisper) are open-source and free under their respective licenses.
- They can run locally on an Intel Core i5 processor (e.g., 6th Gen or later) with 8 GB RAM, assuming lightweight models are used (e.g., TensorFlow Lite’s MobileNet, Whisper’s "tiny" model).
- For optimal performance, pre-trained models should be quantized or optimized, and processing can be offloaded to the mobile device where possible.

## Demo on PC
1. **Run the App**:
   - Clone the repository.
   - **Important:** Set the `GEMINI_API_KEY` environment variable in the `docker-compose.yml` file.
   - Run `docker-compose up --build` in the root directory.
2. **Access the UI**:
   - Open a browser and go to `http://localhost:3000`.
3. **Simulate Scanning**:
   - Upload an image or use a webcam to "scan" an object.
4. **Interact**:
   - View the Malayalam translation overlay on the image.
   - Click "Practice" to access writing, speaking, and listening exercises.
