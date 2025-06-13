from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    """Represents a single message in the conversation."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ConversationContext(BaseModel):
    """Manages the context of a conversation."""
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    messages: List[Message] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    state: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a new message to the conversation."""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.updated_at = datetime.utcnow()

    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update the conversation state."""
        self.state.update(new_state)
        self.updated_at = datetime.utcnow()

    def get_last_message(self) -> Optional[Message]:
        """Get the last message in the conversation."""
        return self.messages[-1] if self.messages else None

    def get_message_history(self, limit: Optional[int] = None) -> List[Message]:
        """Get the message history, optionally limited to the last N messages."""
        if limit is None:
            return self.messages
        return self.messages[-limit:]

    def clear_history(self) -> None:
        """Clear the message history while preserving metadata and state."""
        self.messages = []
        self.updated_at = datetime.utcnow() 