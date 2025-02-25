Create a vocabulary language importer with the following features:

1. UI Components:
    - Model selection dropdown for Groq LLM
        - Should be a small size
        - Should have all the models supported by Groq
    - Text field for inputting thematic category
    - Output field with copy button
    - Success alert for clipboard operations

2. Technical Requirements:
    - Next.js App Router implementation
    - Server-side API route for Groq LLM integration
    - JSON output structure:
      ```json
      [
         {
            "kanji": "良い",
            "romaji": "yoi",
            "english": "good",
            "parts": [
              { "kanji": "良", "romaji": ["yo"] },
              { "kanji": "い", "romaji": ["i"] }
            ]
         }
      ]
      ```

3. Workflow:
    - User selects the Groq model and enters the thematic category
    - Form submission triggers server-side API endpoint
    - LLM processes request and returns structured JSON
    - Result displays in the copyable input field
    - Copy button transfers JSON to the clipboard with user notification

Use the latest Next.js version and implement all LLM processing on the server side.