import asyncio
import requests
import json
from typing import Dict, Any

async def generate_text(prompt: str, **kwargs) -> Dict[str, Any]:
    """Generate text using the vLLM server.
    
    Args:
        prompt: Input prompt
        **kwargs: Additional generation parameters
        
    Returns:
        Dict[str, Any]: Generated text and metadata
    """
    url = "http://localhost:8000/generate"
    payload = {
        "prompt": prompt,
        **kwargs
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

async def list_models() -> Dict[str, Any]:
    """List available models.
    
    Returns:
        Dict[str, Any]: List of available models
    """
    url = "http://localhost:8000/models"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

async def main():
    """Main function demonstrating basic usage."""
    # List available models
    print("\nListing available models:")
    models = await list_models()
    print(json.dumps(models, indent=2))
    
    # Generate text
    print("\nGenerating text:")
    prompt = "Explain the concept of quantum computing in simple terms."
    result = await generate_text(
        prompt=prompt,
        max_tokens=256,
        temperature=0.7
    )
    
    print("\nGenerated Text:")
    print(result["generated_text"])
    print("\nMetadata:")
    print(json.dumps(result["metadata"], indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 