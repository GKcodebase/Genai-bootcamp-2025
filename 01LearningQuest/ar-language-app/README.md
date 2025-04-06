# Interactive Malaylam Learning App

An augmented reality application that helps users learn Malayalam through real-world object detection and interactive language exercises.

## Features

- Real-time object detection using device camera
- Malayalam translation with AR overlay
- Interactive practice exercises (Writing, Speaking, Listening)
- History tracking of scanned objects
- Audio generation for pronunciations
- Speech verification for practice

## Screenshots

- Landing page with AR scanner/ camera capture and Image upload
    ![alt text](<Screenshot 2025-04-06 at 3.34.54 PM.png>)
- Object detection with Malayalam overlay
    ![alt text](<Screenshot 2025-04-06 at 3.36.40 PM.png>)
- Object detection with camera/Photo
    ![alt text](<Screenshot 2025-04-06 at 3.37.38 PM.png>)
- Image upload.
    ![alt text](<Screenshot 2025-04-06 at 3.37.51 PM.png>)
- Practice screen
    - Writing practice: Write the translation of detected word
        ![alt text](<Screenshot 2025-04-06 at 3.38.06 PM.png>)
    - Speaking Practice: practice prounciation
        ![alt text](<Screenshot 2025-04-06 at 3.40.50 PM.png>)
    - Listeniing Practice: Listen to a phrase and type the word
        ![alt text](<Screenshot 2025-04-06 at 3.41.10 PM.png>)
- History view: See the historic practice and retry learning.
    ![alt text](<Screenshot 2025-04-06 at 3.50.04 PM.png>)

## Tech Stack

### Frontend
- Vue.js 3
- Vite
- AR.js & A-Frame
- WebRTC for camera access

### Backend
- FastAPI (Python)
- SQLite3
- Google Gemini API for AI features
- Whisper for speech recognition
- gTTS for text-to-speech

## System Requirements
- Intel Core i5 processor / Mac book air m1
- 8GB RAM minimum
- Camera access for AR features
- Modern web browser (Chrome/Safari recommended)
- HTTPS for camera permissions

## Architecture

```
ar-language-app/
├── frontend/      # Vue.js web application
├── backend/       # FastAPI server
└── docker/        # Docker configuration
```

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ar-language-app.git
cd ar-language-app
```

2. Set up environment variables:
```bash
# In backend/.env
GEMINI_API_KEY=your_api_key_here
```

3. Start the backend:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

4. Start the frontend:
```bash
cd frontend/vue_app
npm install
npm run dev
```

5. Access the application:
   - Open https://localhost:3000 in your browser
   - Accept the SSL certificate warning
   - Grant camera permissions when prompted

## Workflow

1. **Object Detection**
   - Click "Start AR Scan"
   - Point camera at object
   - Click "Detect Object"
   - View Malayalam translation overlay

2. **Practice**
   - Click "Practice" after detection
   - Try writing exercises
   - Practice pronunciation
   - Listen to generated phrases

3. **History**
   - View previously scanned objects
   - Access practice exercises for any item
   - Track learning progress

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the individual README files in frontend and backend directories for details.