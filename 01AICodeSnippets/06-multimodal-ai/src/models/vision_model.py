import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from PIL import Image

class VisionModel:
    """Vision model implementation using Google's Gemini Vision."""
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """Initialize the vision model.
        
        Args:
            model_name: Name of the Gemini model to use
        """
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
            
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(model_name)
        
    async def analyze_image(
        self,
        image: Image.Image,
        prompt: str,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Analyze a single image.
        
        Args:
            image: PIL Image object
            prompt: Text prompt for analysis
            stream: Whether to stream the response
            
        Returns:
            Dict containing analysis results and metadata
        """
        try:
            # Prepare the image part
            image_part = {
                "mime_type": "image/jpeg",
                "data": self._image_to_bytes(image)
            }
            
            # Generate content
            if stream:
                response = self.model.generate_content(
                    [prompt, image_part],
                    stream=True
                )
                # Collect streamed response
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        print(chunk.text, end="", flush=True)
                print()  # New line after streaming
                text = full_response
            else:
                response = self.model.generate_content(
                    [prompt, image_part]
                )
                text = response.text
            
            return {
                "text": text,
                "metadata": {
                    "model": self.model.model_name,
                    "prompt": prompt,
                    "stream": stream
                }
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")
    
    async def analyze_multiple_images(
        self,
        images: List[Image.Image],
        prompt: str,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Analyze multiple images.
        
        Args:
            images: List of PIL Image objects
            prompt: Text prompt for analysis
            stream: Whether to stream the response
            
        Returns:
            Dict containing analysis results and metadata
        """
        try:
            # Prepare image parts
            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": self._image_to_bytes(img)
                }
                for img in images
            ]
            
            # Combine prompt and images
            content = [prompt] + image_parts
            
            # Generate content
            if stream:
                response = self.model.generate_content(
                    content,
                    stream=True
                )
                # Collect streamed response
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        print(chunk.text, end="", flush=True)
                print()  # New line after streaming
                text = full_response
            else:
                response = self.model.generate_content(content)
                text = response.text
            
            return {
                "text": text,
                "metadata": {
                    "model": self.model.model_name,
                    "prompt": prompt,
                    "num_images": len(images),
                    "stream": stream
                }
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing images: {str(e)}")
    
    def _image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes.
        
        Args:
            image: PIL Image object
            
        Returns:
            Image data as bytes
        """
        import io
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()
    
    def to_dict(self) -> Dict[str, Any]:
        """Get model information as dictionary."""
        return {
            "name": "Gemini Vision",
            "model": self.model.model_name
        } 