import requests
import logging
from typing import List, Dict, Any, Optional
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaManager:
    """Manager for Ollama models."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama manager.
        
        Args:
            base_url: Base URL for Ollama API
        """
        self.base_url = base_url
        self.available_models = self._get_available_models()
    
    def _get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json().get("models", [])
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama.
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name}
            )
            response.raise_for_status()
            logger.info(f"Successfully pulled model: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {str(e)}")
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a model from Ollama.
        
        Args:
            model_name: Name of the model to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name}
            )
            response.raise_for_status()
            logger.info(f"Successfully deleted model: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting model {model_name}: {str(e)}")
            return False
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Optional[Dict[str, Any]]: Model information if found, None otherwise
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model_name}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting model info for {model_name}: {str(e)}")
            return None
    
    def list_models(self) -> List[Dict[str, Any]]:
        """Get list of all available models.
        
        Returns:
            List[Dict[str, Any]]: List of available models
        """
        return self.available_models
    
    def update_available_models(self) -> None:
        """Update the list of available models."""
        self.available_models = self._get_available_models()

class ModelConfig:
    """Configuration for model deployment."""
    
    def __init__(self, config_path: str = "model_config.json"):
        """Initialize model configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading config: {str(e)}")
                return self._get_default_config()
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "default_model": "mistralai/Mistral-7B-v0.1",
            "gpu_memory_utilization": 0.9,
            "tensor_parallel_size": 1,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 50
        }
    
    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self.config
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update configuration.
        
        Args:
            new_config: New configuration values
        """
        self.config.update(new_config)
        self.save_config() 