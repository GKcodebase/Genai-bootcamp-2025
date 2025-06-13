import os
import whisper
from typing import Optional, Dict, Any, List
import torch

class AudioModel:
    """Audio transcription model using Whisper."""
    
    def __init__(self, model_name: str = "base"):
        """Initialize the audio model.
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Load the Whisper model."""
        if self.model is None:
            print(f"Loading Whisper {self.model_name} model...")
            self.model = whisper.load_model(self.model_name, device=self.device)
            print("Model loaded successfully!")
    
    async def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        initial_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe an audio file.
        
        Args:
            audio_path: Path to the audio file
            language: Language code (e.g., 'en', 'es', 'fr')
            task: 'transcribe' or 'translate'
            initial_prompt: Optional initial prompt for the model
            
        Returns:
            Dict containing transcription results
        """
        try:
            # Load model if not loaded
            self.load_model()
            
            # Transcribe audio
            result = self.model.transcribe(
                audio_path,
                language=language,
                task=task,
                initial_prompt=initial_prompt
            )
            
            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"],
                "metadata": {
                    "model": self.model_name,
                    "task": task,
                    "device": self.device
                }
            }
            
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
    
    async def transcribe_from_bytes(
        self,
        audio_bytes: bytes,
        file_format: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        initial_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe audio from bytes.
        
        Args:
            audio_bytes: Audio file bytes
            file_format: Audio file format (e.g., 'wav', 'mp3')
            language: Language code
            task: 'transcribe' or 'translate'
            initial_prompt: Optional initial prompt
            
        Returns:
            Dict containing transcription results
        """
        try:
            # Save bytes to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=f".{file_format}", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name
            
            # Transcribe the temporary file
            result = await self.transcribe(
                audio_path=temp_path,
                language=language,
                task=task,
                initial_prompt=initial_prompt
            )
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return result
            
        except Exception as e:
            raise Exception(f"Error transcribing audio bytes: {str(e)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get model information as dictionary."""
        return {
            "name": "Whisper",
            "model": self.model_name,
            "device": self.device,
            "status": "loaded" if self.model is not None else "unloaded"
        } 