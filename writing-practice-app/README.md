# Writing Practice App

A Gradio-based application for Japanese writing practice with automated grading.

## Overview
The Writing Practice App is designed to help users practice their language skills by generating sentences and providing a grading system for their responses. The app utilizes a Sentence Generator LLM and an OCR system to enhance the learning experience.

## Features
- Generate sentences using a specified vocabulary and grammar rules.
- Upload images for grading and receive feedback on responses.
- Transition between different states (Setup, Practice, Review) based on user interactions.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:7860

## Usage

1. Click "Generate Sentence" to get a new sentence to practice
2. Write the sentence in Japanese and upload a photo of your writing
3. Click "Submit for Review" to get feedback
4. Review the feedback and click "Next Question" to continue practicing

## Project Structure
- `src/api/group_service.py`: Handles API requests related to groups.
- `src/llm/sentence_generator.py`: Contains the SentenceGenerator class for sentence construction.
- `src/llm/grading_system.py`: Implements the GradingSystem class for grading responses.
- `src/ocr/manga_ocr.py`: Provides OCR functionality to transcribe text from images.
- `src/app.py`: Main entry point for the application.
- `src/types/models.py`: Defines data models and types used in the app.
- `requirements.txt`: Lists the project dependencies.
- `config.py`: Contains configuration settings for the application.

## License
This project is licensed under the MIT License. See the LICENSE file for details.