"""Task models for A2A protocol."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class TaskStatus(str, Enum):
    """Task status values."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MessageRole(str, Enum):
    """Message role in a conversation."""
    
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


@dataclass
class TaskMessage:
    """A message in a task conversation."""
    
    role: MessageRole
    content: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat() + "Z"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskMessage":
        """Create a TaskMessage from a dictionary."""
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=data.get("timestamp"),
            metadata=data.get("metadata")
        )


@dataclass
class Task:
    """Represents a task in the A2A protocol."""
    
    task_id: str
    status: TaskStatus
    messages: List[TaskMessage] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        """Set timestamps if not provided."""
        now = datetime.utcnow().isoformat() + "Z"
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
    
    def add_message(self, message: TaskMessage) -> None:
        """Add a message to the task."""
        self.messages.append(message)
        self.updated_at = datetime.utcnow().isoformat() + "Z"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata or {},
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create a Task from a dictionary."""
        messages = [TaskMessage.from_dict(m) for m in data.get("messages", [])]
        
        return cls(
            task_id=data["task_id"],
            status=TaskStatus(data["status"]),
            messages=messages,
            metadata=data.get("metadata"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
