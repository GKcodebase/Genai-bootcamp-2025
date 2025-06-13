import os
from typing import Dict, List, Any, Optional
from groq import Groq
from ..models.mcp_protocol import (
    MCPProtocol,
    ModelCapability,
    SecurityLevel,
    ContextType,
    TextContext,
    ImageContext
)

class MCPAgent:
    """Agent that implements the Model Context Protocol."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "llama-3.3-70b-versatile",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.95,
        security_level: SecurityLevel = SecurityLevel.PUBLIC
    ):
        """Initialize the MCP agent."""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        
        # Initialize MCP protocol
        self.protocol = MCPProtocol()
        
        # Register the model with MCP
        self._model_metadata = None
    
    async def _ensure_model_registered(self, security_level: SecurityLevel) -> None:
        """Ensure the model is registered with MCP."""
        if self._model_metadata is None:
            self._model_metadata = await self.protocol.register_model(
                model_id=self.model_name,
                version="1.0",
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.SUMMARIZATION
                ],
                max_tokens=self.max_tokens,
                security_level=security_level
            )
    
    async def generate_response(
        self,
        prompt: str,
        context_id: Optional[str] = None,
        security_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a response using the model."""
        # Ensure model is registered
        await self._ensure_model_registered(SecurityLevel.PUBLIC)
        
        # Get conversation history if context_id is provided
        messages = []
        if context_id:
            history = await self.get_conversation_history(context_id)
            for entry in history:
                if "role" in entry["metadata"]:
                    messages.append({
                        "role": entry["metadata"]["role"],
                        "content": entry["content"]
                    })
        
        # Add the current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Create text context
        context = TextContext(
            content=prompt,
            metadata={
                "model": self.model_name,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "role": "user"
            }
        )
        
        # Add context to store if context_id provided
        if context_id:
            await self.protocol.add_context(
                context_id=context_id,
                context_data=context,
                security_token=security_token
            )
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p
        )
        
        # Create response context
        response_context = TextContext(
            content=response.choices[0].message.content,
            metadata={
                "model": self.model_name,
                "finish_reason": response.choices[0].finish_reason,
                "usage": response.usage.dict(),
                "role": "assistant"
            }
        )
        
        # Add response to context store if context_id provided
        if context_id:
            await self.protocol.add_context(
                context_id=context_id,
                context_data=response_context,
                security_token=security_token
            )
        
        return {
            "response": response.choices[0].message.content,
            "metadata": response_context.metadata,
            "context_id": context_id
        }
    
    async def get_conversation_history(
        self,
        context_id: str,
        security_token: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get the conversation history for a context."""
        contexts = await self.protocol.get_context(
            context_id=context_id,
            context_type=ContextType.TEXT,
            security_token=security_token
        )
        
        return [
            {
                "content": context.content,
                "metadata": context.metadata,
                "created_at": context.created_at
            }
            for context in contexts
        ]
    
    async def generate_security_token(
        self,
        capabilities: List[ModelCapability]
    ) -> str:
        """Generate a security token for model access."""
        # Ensure model is registered
        await self._ensure_model_registered(SecurityLevel.PRIVATE)
        return await self.protocol.generate_security_token(
            model_id=self.model_name,
            capabilities=capabilities
        )
    
    async def validate_security_token(
        self,
        token: str,
        required_capabilities: List[ModelCapability]
    ) -> bool:
        """Validate a security token."""
        # Ensure model is registered
        await self._ensure_model_registered(SecurityLevel.PRIVATE)
        return await self.protocol.validate_security_token(
            token=token,
            required_capabilities=required_capabilities
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the agent state to a dictionary."""
        return {
            "model_name": self.model_name,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "protocol": self.protocol.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPAgent':
        """Create an agent instance from a dictionary."""
        agent = cls(
            model_name=data["model_name"],
            max_tokens=data["max_tokens"],
            temperature=data["temperature"],
            top_p=data["top_p"]
        )
        agent.protocol = MCPProtocol.from_dict(data["protocol"])
        return agent 