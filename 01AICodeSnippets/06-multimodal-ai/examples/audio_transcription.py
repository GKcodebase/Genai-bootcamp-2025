import asyncio
import os
from src.models.audio_model import AudioModel

async def main():
    # Initialize the audio model
    model = AudioModel()
    
    # Example 1: Transcribe an audio file
    print("\nExample 1: Transcribing an audio file")
    print("-" * 50)
    
    # Transcribe audio
    audio_path = "examples/audio/sample.wav"  # Replace with your audio path
    result = await model.transcribe(
        audio_path=audio_path,
        language="en",  # Optional: specify language
        task="transcribe"
    )
    
    print("\nTranscription Result:")
    print(result["text"])
    print("\nSegments:")
    for segment in result["segments"]:
        print(f"[{segment['start']:.1f}s -> {segment['end']:.1f}s] {segment['text']}")
    print("\nMetadata:", result["metadata"])
    
    # Example 2: Translate audio
    print("\nExample 2: Translating audio to English")
    print("-" * 50)
    
    # Translate audio
    result = await model.transcribe(
        audio_path=audio_path,
        language="es",  # Source language
        task="translate"  # Translate to English
    )
    
    print("\nTranslation Result:")
    print(result["text"])
    print("\nMetadata:", result["metadata"])
    
    # Example 3: Transcribe with initial prompt
    print("\nExample 3: Transcribing with initial prompt")
    print("-" * 50)
    
    # Transcribe with prompt
    result = await model.transcribe(
        audio_path=audio_path,
        language="en",
        task="transcribe",
        initial_prompt="This is a conversation about artificial intelligence."
    )
    
    print("\nTranscription with Prompt Result:")
    print(result["text"])
    print("\nMetadata:", result["metadata"])

if __name__ == "__main__":
    asyncio.run(main()) 