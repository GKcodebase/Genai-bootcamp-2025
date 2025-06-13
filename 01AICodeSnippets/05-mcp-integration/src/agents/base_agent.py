from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.models.context import ConversationContext

class BaseAgent(ABC):
    """Base class for all agents implementing the Model Context Protocol."""
    
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ):
        """Initialize the base agent.
        
        Args:
            model_name: Name of the model to use
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional model-specific parameters
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model_params = kwargs

    @abstractmethod
    async def chat(
        self,
        message: str,
        context: ConversationContext,
        **kwargs
    ) -> Dict[str, Any]:
        """Process a chat message and return a response.
        
        Args:
            message: User message to process
            context: Current conversation context
            **kwargs: Additional parameters for the chat request
            
        Returns:
            Dictionary containing the response and any metadata
        """
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the agent and any required resources."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up any resources used by the agent."""
        pass

    def _validate_context(self, context: ConversationContext) -> None:
        """Validate the conversation context.
        
        Args:
            context: Conversation context to validate
            
        Raises:
            ValueError: If the context is invalid
        """
        if not isinstance(context, ConversationContext):
            raise ValueError("Invalid conversation context")
        
        if not context.conversation_id:
            raise ValueError("Conversation ID is required")

    def _prepare_prompt(
        self,
        message: str,
        context: ConversationContext,
        **kwargs
    ) -> str:
        """Prepare the prompt for the model.
        
        Args:
            message: User message
            context: Conversation context
            **kwargs: Additional parameters
            
        Returns:
            Formatted prompt string
        """
        # Get recent message history
        history = context.get_message_history(limit=5)
        
        # Format the prompt with context
        prompt_parts = []
        
        # Add system message if provided
        if "system_message" in kwargs:
            prompt_parts.append(f"System: {kwargs['system_message']}")
        
        # Add conversation history
        for msg in history:
            prompt_parts.append(f"{msg.role.capitalize()}: {msg.content}")
        
        # Add current message
        prompt_parts.append(f"User: {message}")
        
        return "\n".join(prompt_parts) 