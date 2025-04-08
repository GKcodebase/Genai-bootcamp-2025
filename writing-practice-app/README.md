# Writing Practice App

A Gradio-based application for Japanese writing practice with automated grading.

## Overview
The Writing Practice App is designed to help users practice their language skills by generating sentences and providing a grading system for their responses. The app utilizes a Sentence Generator LLM and an OCR system to enhance the learning experience.

## Features
- Generate sentences using a specified vocabulary and grammar rules
- Upload images for grading and receive feedback on responses
- Transition between different states (Setup, Practice, Review)
- OCR-based handwriting recognition using MangaOCR
- AI-powered grading with detailed feedback
- JLPT N5 grammar scope

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
cat << EOF > .env
GROQ_API_KEY=your_groq_api_key_here
SESSION_ID=1
EOF
```

4. Run the application:
```bash
cd src
python app.py
```

The application will be available at http://localhost:7860

## Usage

1. Click "Generate Sentence" to get a new sentence to practice
2. Write the sentence in Japanese and upload a photo of your writing
3. Click "Submit for Review" to get feedback
4. Review the feedback and click "Next Question" to continue practicing

## Project Structure
```
writing-practice-app/
├── src/
│   ├── app.py              # Main application entry point
│   ├── api/                # API integration
│   ├── llm/                # LLM implementations
│   ├── ocr/                # OCR functionality
│   └── types/              # Data models
├── screenshots/            # Application screenshots
├── requirements.txt        # Project dependencies
├── config.py              # Configuration settings
└── README.md              # This file
```

## Adding Screenshots
To add new screenshots:

1. Create screenshots directory if it doesn't exist:
```bash
mkdir -p screenshots
```

2. Add screenshots following the naming convention:
```
screenshots/
├── setup-screen.png
├── practice-interface.png
├── review-screen.png
└── grading-example.png
```

3. Optimize images for web:
```bash
# Install ImageOptim if not present
brew install imageoptim

# Optimize screenshots
imageoptim screenshots/*.png
```

## 🔑 Environment Variables

### Required Variables
Create a `.env` file in the project root:

```env
# Groq AI API Key (Required)
GROQ_API_KEY=your_groq_api_key_here

# Optional Configuration
OCR_LIBRARY=MangaOCR
GRAMMAR_SCOPE=JLPTN5
```

### Setting Up Environment Variables

1. Create `.env` file:
```bash
touch .env
```

2. Add your Groq API key:
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
```

3. Verify environment variables:
```bash
# Check if .env is loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('GROQ_API_KEY'))"
```

### Security Notes
- Never commit `.env` file to version control
- Keep your API keys secure
- Add `.env` to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.