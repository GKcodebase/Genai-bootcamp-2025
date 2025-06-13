from typing import Dict, List, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import json
import hashlib

class ModelCapability(str, Enum):
    """Enum for model capabilities."""
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    CODE_GENERATION = "code_generation"
    EMBEDDING = "embedding"
    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"

class SecurityLevel(str, Enum):
    """Enum for security levels."""
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"

class ModelMetadata(BaseModel):
    """Metadata for a registered model."""
    model_id: str
    version: str
    capabilities: List[ModelCapability]
    max_tokens: int
    security_level: SecurityLevel
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContextType(str, Enum):
    """Enum for context types."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    CODE = "code"
    STRUCTURED = "structured"

class ContextData(BaseModel):
    """Base class for context data."""
    type: ContextType
    content: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TextContext(ContextData):
    """Text context data."""
    type: ContextType = ContextType.TEXT
    content: str
    language: str = "en"
    encoding: str = "utf-8"

class ImageContext(ContextData):
    """Image context data."""
    type: ContextType = ContextType.IMAGE
    content: bytes
    format: str
    dimensions: Dict[str, int]

class MCPProtocol:
    """Implementation of the Model Context Protocol."""
    
    def __init__(self):
        self.version = "1.0"
        self.model_registry: Dict[str, ModelMetadata] = {}
        self.context_store: Dict[str, List[ContextData]] = {}
        self.security_tokens: Dict[str, str] = {}
        
    async def register_model(
        self,
        model_id: str,
        version: str,
        capabilities: List[ModelCapability],
        max_tokens: int,
        security_level: SecurityLevel = SecurityLevel.PUBLIC
    ) -> ModelMetadata:
        """Register a new model with the protocol."""
        metadata = ModelMetadata(
            model_id=model_id,
            version=version,
            capabilities=capabilities,
            max_tokens=max_tokens,
            security_level=security_level
        )
        self.model_registry[model_id] = metadata
        return metadata
    
    async def compose_models(
        self,
        model_chain: List[str],
        context_id: str
    ) -> Dict[str, Any]:
        """Compose multiple models into a workflow."""
        # Validate models exist
        for model_id in model_chain:
            if model_id not in self.model_registry:
                raise ValueError(f"Model {model_id} not registered")
        
        # Create workflow
        workflow = {
            "id": hashlib.sha256(f"{context_id}-{datetime.utcnow()}".encode()).hexdigest(),
            "models": model_chain,
            "status": "created",
            "created_at": datetime.utcnow()
        }
        
        return workflow
    
    async def add_context(
        self,
        context_id: str,
        context_data: ContextData,
        security_token: Optional[str] = None
    ) -> None:
        """Add context data to the store."""
        # Validate security if needed
        if context_data.type == ContextType.IMAGE and not security_token:
            raise ValueError("Security token required for image context")
        
        if context_id not in self.context_store:
            self.context_store[context_id] = []
        
        self.context_store[context_id].append(context_data)
    
    async def get_context(
        self,
        context_id: str,
        context_type: Optional[ContextType] = None,
        security_token: Optional[str] = None
    ) -> List[ContextData]:
        """Retrieve context data from the store."""
        if context_id not in self.context_store:
            return []
        
        contexts = self.context_store[context_id]
        
        # Filter by type if specified
        if context_type:
            contexts = [c for c in contexts if c.type == context_type]
        
        # Apply security checks
        if security_token:
            # Implement security checks here
            pass
        
        return contexts
    
    async def generate_security_token(
        self,
        model_id: str,
        capabilities: List[ModelCapability]
    ) -> str:
        """Generate a security token for model access."""
        token = hashlib.sha256(
            f"{model_id}-{'-'.join(capabilities)}-{datetime.utcnow()}".encode()
        ).hexdigest()
        
        self.security_tokens[token] = model_id
        return token
    
    async def validate_security_token(
        self,
        token: str,
        required_capabilities: List[ModelCapability]
    ) -> bool:
        """Validate a security token."""
        if token not in self.security_tokens:
            return False
        
        model_id = self.security_tokens[token]
        if model_id not in self.model_registry:
            return False
        
        model = self.model_registry[model_id]
        return all(cap in model.capabilities for cap in required_capabilities)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the protocol state to a dictionary."""
        return {
            "version": self.version,
            "model_registry": {
                k: v.dict() for k, v in self.model_registry.items()
            },
            "context_store": {
                k: [c.dict() for c in v] for k, v in self.context_store.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPProtocol':
        """Create a protocol instance from a dictionary."""
        protocol = cls()
        protocol.version = data["version"]
        
        # Restore model registry
        for model_id, metadata in data["model_registry"].items():
            protocol.model_registry[model_id] = ModelMetadata(**metadata)
        
        # Restore context store
        for context_id, contexts in data["context_store"].items():
            protocol.context_store[context_id] = [
                ContextData(**context) for context in contexts
            ]
        
        return protocol 