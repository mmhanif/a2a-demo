"""Agent Card models for A2A protocol."""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from enum import Enum


class InteractionMode(str, Enum):
    """Supported interaction modes for A2A agents."""
    
    TEXT = "text"
    FORM = "form"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"


@dataclass
class Skill:
    """Represents a skill that an agent can perform."""
    
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    interaction_modes: List[InteractionMode] = field(default_factory=lambda: [InteractionMode.TEXT])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "interaction_modes": [mode.value for mode in self.interaction_modes]
        }


@dataclass
class AgentCard:
    """Agent Card describing an agent's capabilities and connection information."""
    
    name: str
    description: str
    url: str
    skills: List[Skill]
    version: str = "1.0"
    supported_interaction_modes: List[InteractionMode] = field(
        default_factory=lambda: [InteractionMode.TEXT]
    )
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent card to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "version": self.version,
            "skills": [skill.to_dict() for skill in self.skills],
            "supported_interaction_modes": [mode.value for mode in self.supported_interaction_modes],
            "metadata": self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentCard":
        """Create an AgentCard from a dictionary."""
        skills = [
            Skill(
                name=s["name"],
                description=s["description"],
                parameters=s.get("parameters", {}),
                interaction_modes=[InteractionMode(m) for m in s.get("interaction_modes", ["text"])]
            )
            for s in data.get("skills", [])
        ]
        
        return cls(
            name=data["name"],
            description=data["description"],
            url=data["url"],
            skills=skills,
            version=data.get("version", "1.0"),
            supported_interaction_modes=[
                InteractionMode(m) for m in data.get("supported_interaction_modes", ["text"])
            ],
            metadata=data.get("metadata")
        )
