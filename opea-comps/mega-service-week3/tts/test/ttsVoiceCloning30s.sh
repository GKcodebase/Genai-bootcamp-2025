#!/usr/bin/bash

#!/usr/bin/bash

mkdir -p out  # Make sure output folder exists

curl -X POST "http://127.0.0.1:9880" \
  -H "Content-Type: application/json" \
  --output out/output-30s.wav \
  -d @- << 'EOF'
{
  "refer_wav_path": "/audio/audio30.wav",
  "prompt_text": "Raise the load to your left shoulder.",
  "prompt_language": "en",
  "text": "This is latest 30 second sentence I want to convert to speech",
  "text_language": "en"
}
EOF

