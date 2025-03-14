curl -X POST "http://127.0.0.1:9880" \
-H "Content-Type: application/json" \
--output out/output-1m.wav \
-d @- << 'EOF'
{
  "refer_wav_path": "/audio/andrew-ref-1m.wav",
  "prompt_text": "",
  "prompt_language": "en",
  "text": "This is latest one minute sentence I want to convert to speech",
  "text_language": "en"
}
EOF
