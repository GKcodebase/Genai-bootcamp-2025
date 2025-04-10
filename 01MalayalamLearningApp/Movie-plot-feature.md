# AR Language Learning App - Movie Plot Feature

## Business Goal
Expand the AR Language Learning App to enable users to:
- Input a movie name to retrieve its plot summary from Wikipedia.
- View the plot translated into Malayalam with audio playback.
- Chat with an AI chatbot in Manglish (Malayalam-English mix), playing the role of a main character from the movie.

This feature connects language learning with popular culture, offering immersive reading, listening, and conversational practice.

## Technical Requirements
- **Platforms**: iOS and Android, consistent with the main app.
- **AI Integration**:
  - **Plot Retrieval**: Fetch movie plot summaries from Wikipedia.
  - **Translation**: Translate the English plot into Malayalam.
  - **Audio Generation**: Generate audio for the translated plot.
  - **Chatbot**: AI-driven chatbot in Manglish, acting as a main character, using plot data for context.
- **Backend**: Extend the existing FastAPI backend with new endpoints.
- **Database**: Add a new table to the existing SQLite database (`app.db`).
- **API**: New JSON-based endpoints for plot retrieval and chatbot interaction.
- **Authentication**: No authentication required, aligning with the main app.
- **Deployment**: Backend updates deployable within the existing Docker container.
- **Hardware Compatibility**: Must run locally on an Intel Core i5 with 8 GB RAM, using lightweight AI models compatible with existing tools.

## UI Requirements
- **Movie Plot Screen** (accessible from the landing page):
  - **Input Field**: Text box for entering a movie name (e.g., "The Matrix").
  - **Search Button**: Initiates plot retrieval and translation.
  - **Result Display**:
    - Translated Malayalam plot text (e.g., "മാട്രിക്സ് ഒരു സാങ്കൽപ്പിക ലോകത്തെക്കുറിച്ചാണ്...").
    - **Listen Button**: Plays AI-generated audio of the translated plot.
    - **Chat Button**: Opens a chat interface with the Manglish chatbot.
  - **Chat Interface**:
    - Text input for user messages.
    - Chatbot responses in Manglish (e.g., "Njan Neo aanu, Matrix il ninnu escape cheythu! Ninakku help veno?").
    - Optional: Display a static character image next to the chat.

## Directory Structure
movie-plot/
├── backend/
│ ├── app/
│ │ ├── routers/
│ │ │ └── movies.py # New endpoints for movie plots and chatbot
│ │ ├── models.py # New SQLAlchemy models (append to existing file)
│ │ └── schemas.py # New Pydantic schemas (append to existing file)
│ ├── ai_models/
│ │ └── chatbot_model.pth # Optional lightweight chatbot model
│ └── requirements.txt # Add dependencies (e.g., wikipedia-api)
├── frontend/
│ ├── vue_app/
│ │ ├── src/
│ │ │ ├── components/
│ │ │ │ └── MoviePlotScreen.vue # New UI component
│ └── package.json # Add any new frontend dependencies
└── README.md # Setup instructions for this feature


*Note*: Integrates with the existing `ar-language-app/` by appending to `models.py`, `schemas.py`, and adding `MoviePlotScreen.vue` to `vue_app/src/components/`, minimizing changes to existing files.

## Database Schema
Append to the existing `app.db`:

- **movie_plots**
  - `id` integer (primary key)
  - `movie_name` string (e.g., "The Matrix")
  - `english_plot` text (original Wikipedia plot)
  - `malayalam_plot` text (AI-translated plot)
  - `audio_url` string (URL to AI-generated audio)
  - `timestamp` datetime (when the plot was retrieved)

## API Endpoints

- **`POST /api/movie_plot`**
  - **Description**: Retrieve a movie plot from Wikipedia and translate it to Malayalam.
  - **Request**:
    ```json
    {
      "movie_name": "The Matrix"
    }
    ```
  - **Response**:
    ```json
    {
      "movie_id": 1,
      "movie_name": "The Matrix",
      "malayalam_plot": "മാട്രിക്സ് ഒരു സാങ്കൽപ്പിക ലോകത്തെക്കുറിച്ചാണ്...",
      "audio_url": "https://example.com/audio/matrix_plot.mp3"
    }
    ```

- **`POST /api/movie_chat`**
  - **Description**: Chat with a Manglish chatbot playing a main character from the movie.
  - **Request**:
    ```json
    {
      "movie_id": 1,
      "message": "Hi, who are you?"
    }
    ```
  - **Response**:
    ```json
    {
      "response": "Njan Neo aanu, Matrix il ninnu escape cheythu! Ninakku help veno?"
    }
    ```

## Technology Stack
- **Mobile App**: Reuse existing Flutter or React Native framework.
- **AI Tools**:
  - **Plot Retrieval**: `wikipedia-api` (MIT license) or `BeautifulSoup` (MIT license) for scraping.
  - **Translation**: Reuse Hugging Face MarianMT (Apache 2.0/MIT) from the main app.
  - **Text-to-Speech**: Reuse Mozilla TTS (MPL 2.0) or eSpeak (GPLv3).
  - **Chatbot**: Lightweight GPT-2 (Hugging Face, Apache 2.0) or rule-based Manglish generator, trained or configured for Manglish output, runs locally.
- **Backend**: FastAPI with SQLite3 (existing).
- **Frontend**: Vue.js, appending to existing `vue_app/` structure.

## Deployment
- Add new endpoints and models to the existing backend Docker container.
- Update the frontend build process to include `MoviePlotScreen.vue`.

## Task Runner Tasks
- **Run Tests**: Add unit and integration tests for plot retrieval, translation, audio generation, and chatbot interaction.

## Hardware Compatibility Notes
All AI tools (e.g., MarianMT, Mozilla TTS, GPT-2 small) are open-source and run locally on an Intel Core i5 with 8 GB RAM, consistent with the main app’s requirements. The chatbot uses a lightweight model or rule-based logic to ensure performance, with Manglish output generated by mixing Malayalam and English based on plot context.

## Non functional hard requirements
- There should be minimal changes in the existing code
- Exisiting functionalities should not be broken
- [Exisiting Featuers](./Technical-Spec.md)
- New Featuers should use existing Technologies
- New Featuers should intergerate with exisiting feature smootly.