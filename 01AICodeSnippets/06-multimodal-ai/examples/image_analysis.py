import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from src.models.vision_model import VisionModel

# Load environment variables
load_dotenv()

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

async def main():
    # Check for required environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable not set")
        print("Please create a .env file with your Google AI API key")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return

    # Initialize the vision model
    model = VisionModel()
    
    # Example 1: Analyze a single image
    print("\nExample 1: Analyzing a single image")
    print("-" * 50)
    
    # Load image
    image_path = os.path.join(project_root, "examples", "images", "sample.jpg")
    if not os.path.exists(image_path):
        print(f"Please add a sample image at: {image_path}")
        return
        
    image = Image.open(image_path)
    
    # Analyze image
    result = await model.analyze_image(
        image=image,
        prompt="Describe what you see in this image in detail."
    )
    
    print("\nImage Analysis Result:")
    print(result["text"])
    print("\nMetadata:", result["metadata"])
    
    # Example 2: Compare multiple images
    print("\nExample 2: Comparing multiple images")
    print("-" * 50)
    
    # Load images
    image_paths = [
        os.path.join(project_root, "examples", "images", "sample1.jpg"),
        os.path.join(project_root, "examples", "images", "sample2.jpg")
    ]
    
    # Check if images exist
    missing_images = [path for path in image_paths if not os.path.exists(path)]
    if missing_images:
        print("Please add sample images at:")
        for path in missing_images:
            print(f"- {path}")
        return
        
    images = [Image.open(path) for path in image_paths]
    
    # Analyze images
    result = await model.analyze_multiple_images(
        images=images,
        prompt="Compare these images and describe their similarities and differences."
    )
    
    print("\nImage Comparison Result:")
    print(result["text"])
    print("\nMetadata:", result["metadata"])
    
    # Example 3: Streaming response
    print("\nExample 3: Streaming response")
    print("-" * 50)
    
    # Analyze image with streaming
    print("\nStreaming Analysis:")
    result = await model.analyze_image(
        image=image,
        prompt="What emotions or feelings does this image convey?",
        stream=True
    )
    
    print("\nStreaming Result:")
    print(result["text"])
    print("\nMetadata:", result["metadata"])

if __name__ == "__main__":
    asyncio.run(main()) 