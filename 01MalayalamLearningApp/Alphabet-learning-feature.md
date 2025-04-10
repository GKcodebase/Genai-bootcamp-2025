
# AR Language Learning App - Alphabet Learning Feature

## Business Goal
Enhance the AR Language Learning App by adding an interactive feature to teach users the Malayalam alphabet. The feature will allow users to:
- View all Malayalam alphabets with their English transliteration.
- Click an alphabet to hear its pronunciation, see its English pronunciation, and explore AI-generated example words.
- Generate new example words dynamically with each request to expand vocabulary practice.

This targets beginners, providing an engaging way to master the Malayalam script.

## Technical Requirements
- **Platforms**: iOS and Android, consistent with the main app.
- **AI Integration**:
  - **Word Generation**: AI generates unique Malayalam words containing the selected alphabet, ensuring variety each time.
  - **Audio Generation**: AI produces pronunciation audio for alphabets and generated words.
- **Backend**: Extend the existing FastAPI backend with new endpoints.
- **Database**: Add new tables to the existing SQLite database (`app.db`).
- **API**: New JSON-based endpoints for alphabet data and word generation.
- **Authentication**: No authentication required, aligning with the main app.
- **Deployment**: Backend updates deployable within the existing Docker container.
- **Hardware Compatibility**: Must run locally on an Intel Core i5 with 8 GB RAM, using lightweight AI models compatible with existing tools.

## UI Requirements
- **Alphabet Learning Screen** (accessible from the landing page):
  - **Alphabet Grid**: Displays all Malayalam alphabets (e.g., അ, ആ, ഇ, ക, ഖ) with English transliteration below each (e.g., "a," "ā," "i," "ka," "kha").
  - **On Click**:
    - Plays AI-generated audio pronunciation of the alphabet.
    - Shows English pronunciation (e.g., "ka" for ക).
    - Displays 2-3 AI-generated example words (e.g., for ക: കല, കാറ്റ്, കുട).
  - **Generate Words Button**: Refreshes the example words with new AI-generated options.
  - **Listen Buttons**: Next to each generated word for audio playback.

## Directory Structure
*Note*: Integrates with the existing `ar-language-app/` by appending to `models.py`, `schemas.py`, and adding `AlphabetScreen.vue` to `vue_app/src/components/`, minimizing changes to existing files.
```
alphabet-learning/
├── backend/
│ ├── app/
│ │ ├── routers/
│ │ │ └── alphabets.py # New endpoints for alphabet learning
│ │ ├── models.py # New SQLAlchemy models (append to existing file)
│ │ └── schemas.py # New Pydantic schemas (append to existing file)
│ ├── ai_models/
│ │ └── word_gen_model.pth # Optional lightweight word generation model
│ └── requirements.txt # Add any new dependencies (e.g., word generation libs)
├── frontend/
│ ├── vue_app/
│ │ ├── src/
│ │ │ ├── components/
│ │ │ │ └── AlphabetScreen.vue # New UI component
│ └── package.json # Add any new frontend dependencies
└── README.md # Setup instructions for this feature
```
## Database Schema
Append to the existing `app.db`:

- **alphabets**
  - `id` integer (primary key)
  - `malayalam_char` string (e.g., "ക")
  - `english_transliteration` string (e.g., "ka")
  - `audio_url` string (URL to AI-generated pronunciation audio)

- **generated_words**
  - `id` integer (primary key)
  - `alphabet_id` integer (foreign key referencing `alphabets.id`)
  - `word` string (e.g., "കല" - "kala" meaning "art")
  - `audio_url` string (URL to AI-generated audio)
  - `timestamp` datetime (when the word was generated)

## API Endpoints

- **`GET /api/alphabets`**
  - **Description**: Retrieve all Malayalam alphabets with transliteration and audio.
  - **Response**:
    ```json
    {
      "items": [
        {
          "id": 1,
          "malayalam_char": "ക",
          "english_transliteration": "ka",
          "audio_url": "https://example.com/audio/ka.mp3"
        },
        {
          "id": 2,
          "malayalam_char": "ഖ",
          "english_transliteration": "kha",
          "audio_url": "https://example.com/audio/kha.mp3"
        }
        // ... more alphabets
      ]
    }
    ```

- **`GET /api/generate_words`**
  - **Description**: Generate new example words for a specific alphabet.
  - **Query Parameters**:
    - `alphabet_id`: integer (ID from `alphabets` table)
  - **Response**:
    ```json
    {
      "alphabet_id": 1,
      "words": [
        {"word": "കല", "audio_url": "https://example.com/audio/kala.mp3"},
        {"word": "കാറ്റ്", "audio_url": "https://example.com/audio/kattu.mp3"}
        // ... possibly more words
      ]
    }
    ```

## Technology Stack
- **Mobile App**: Reuse existing Flutter or React Native framework.
- **AI Tools**:
  - **Word Generation**: Lightweight model like Hugging Face GPT-2 (small) or a custom Markov chain trained on Malayalam text, optimized for local execution.
  - **Text-to-Speech**: Reuse Mozilla TTS (MPL 2.0) or eSpeak (GPLv3) from the main app.
- **Backend**: FastAPI with SQLite3 (existing).
- **Frontend**: Vue.js, appending to existing `vue_app/` structure.

## Deployment
- Add new endpoints and models to the existing backend Docker container.
- Update the frontend build process to include `AlphabetScreen.vue`.

## Task Runner Tasks
- **Seed Alphabets**: Populate the `alphabets` table with Malayalam characters and transliterations.
- **Run Tests**: Add unit and integration tests for endpoints and UI functionality.

## Hardware Compatibility Notes
All AI tools (e.g., GPT-2 small, Mozilla TTS, eSpeak) are open-source and run locally on an Intel Core i5 with 8 GB RAM, consistent with the main app’s requirements. Word generation uses lightweight models or rule-based logic to ensure performance.

## Non functional hard requirements
- There should be minimal changes in the existing code
- Exisiting functionalities should not be broken
- [Exisiting Featuers](./Technical-Spec.md)
- New Featuers should use existing Technologies
- New Featuers should intergerate with exisiting feature smootly.