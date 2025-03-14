curl http://localhost:9088/v1/audio/speech \
-X POST \
-H "Content-Type: application/json" \
-d '{"input":"Who are you?", "voice": "default"}' \
--output ./out/speech.wav