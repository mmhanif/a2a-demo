"""JSON-RPC 2.0 models for A2A protocol."""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


@dataclass
class JSONRPCRequest:
    """JSON-RPC 2.0 request."""
    
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Union[str, int, None] = None
    jsonrpc: str = "2.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "id": self.id
        }
        if self.params is not None:
            result["params"] = self.params
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JSONRPCRequest":
        """Create a JSONRPCRequest from a dictionary."""
        return cls(
            method=data["method"],
            params=data.get("params"),
            id=data.get("id"),
            jsonrpc=data.get("jsonrpc", "2.0")
        )


@dataclass
class JSONRPCError:
    """JSON-RPC 2.0 error."""
    
    code: int
    message: str
    data: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "code": self.code,
            "message": self.message
        }
        if self.data is not None:
            result["data"] = self.data
        return result


@dataclass
class JSONRPCResponse:
    """JSON-RPC 2.0 response."""
    
    id: Union[str, int, None]
    result: Optional[Any] = None
    error: Optional[JSONRPCError] = None
    jsonrpc: str = "2.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        response = {
            "jsonrpc": self.jsonrpc,
            "id": self.id
        }
        
        if self.error:
            response["error"] = self.error.to_dict()
        else:
            response["result"] = self.result
        
        return response
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JSONRPCResponse":
        """Create a JSONRPCResponse from a dictionary."""
        error = None
        if "error" in data:
            error = JSONRPCError(
                code=data["error"]["code"],
                message=data["error"]["message"],
                data=data["error"].get("data")
            )
        
        return cls(
            id=data.get("id"),
            result=data.get("result"),
            error=error,
            jsonrpc=data.get("jsonrpc", "2.0")
        )


# Standard JSON-RPC error codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
