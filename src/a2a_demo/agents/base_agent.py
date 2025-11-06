"""Base agent server for A2A protocol."""

from flask import Flask, request, jsonify
from typing import Dict, Any, Callable, Optional
import uuid
from abc import ABC, abstractmethod

from ..models import (
    AgentCard, Task, TaskStatus, TaskMessage, MessageRole,
    JSONRPCRequest, JSONRPCResponse, JSONRPCError,
    METHOD_NOT_FOUND, INVALID_PARAMS, INTERNAL_ERROR
)


class BaseAgent(ABC):
    """Base class for A2A agents."""
    
    def __init__(self, name: str, description: str, host: str = "0.0.0.0", port: int = 5000):
        """Initialize the base agent.
        
        Args:
            name: Agent name
            description: Agent description
            host: Host to bind the server to
            port: Port to bind the server to
        """
        self.name = name
        self.description = description
        self.host = host
        self.port = port
        self.app = Flask(name)
        self.tasks: Dict[str, Task] = {}
        self.methods: Dict[str, Callable] = {}
        
        # Register standard A2A methods
        self._register_standard_methods()
        self._setup_routes()
    
    @abstractmethod
    def get_agent_card(self) -> AgentCard:
        """Return the agent card describing this agent's capabilities.
        
        Returns:
            AgentCard with agent capabilities
        """
        pass
    
    @abstractmethod
    def handle_task(self, task_id: str, message: TaskMessage) -> str:
        """Handle a task message and return a response.
        
        Args:
            task_id: The task ID
            message: The message to process
            
        Returns:
            Response message content
        """
        pass
    
    def _register_standard_methods(self) -> None:
        """Register standard A2A protocol methods."""
        self.register_method("getAgentCard", self._get_agent_card)
        self.register_method("createTask", self._create_task)
        self.register_method("sendTaskMessage", self._send_task_message)
        self.register_method("getTask", self._get_task)
        self.register_method("listTasks", self._list_tasks)
    
    def register_method(self, method_name: str, handler: Callable) -> None:
        """Register a JSON-RPC method handler.
        
        Args:
            method_name: Name of the method
            handler: Callable that handles the method
        """
        self.methods[method_name] = handler
    
    def _setup_routes(self) -> None:
        """Set up Flask routes."""
        
        @self.app.route("/", methods=["POST"])
        def handle_jsonrpc():
            """Handle JSON-RPC requests."""
            try:
                data = request.get_json()
                if not data:
                    return jsonify(
                        JSONRPCResponse(
                            id=None,
                            error=JSONRPCError(code=INVALID_PARAMS, message="Invalid JSON")
                        ).to_dict()
                    ), 400
                
                rpc_request = JSONRPCRequest.from_dict(data)
                response = self._handle_request(rpc_request)
                return jsonify(response.to_dict())
                
            except Exception as e:
                return jsonify(
                    JSONRPCResponse(
                        id=None,
                        error=JSONRPCError(code=INTERNAL_ERROR, message=str(e))
                    ).to_dict()
                ), 500
        
        @self.app.route("/health", methods=["GET"])
        def health():
            """Health check endpoint."""
            return jsonify({"status": "healthy", "agent": self.name})
    
    def _handle_request(self, rpc_request: JSONRPCRequest) -> JSONRPCResponse:
        """Handle a JSON-RPC request.
        
        Args:
            rpc_request: The JSON-RPC request
            
        Returns:
            JSON-RPC response
        """
        method = rpc_request.method
        
        if method not in self.methods:
            return JSONRPCResponse(
                id=rpc_request.id,
                error=JSONRPCError(code=METHOD_NOT_FOUND, message=f"Method '{method}' not found")
            )
        
        try:
            handler = self.methods[method]
            result = handler(rpc_request.params or {})
            return JSONRPCResponse(id=rpc_request.id, result=result)
        except Exception as e:
            return JSONRPCResponse(
                id=rpc_request.id,
                error=JSONRPCError(code=INTERNAL_ERROR, message=str(e))
            )
    
    def _get_agent_card(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get the agent card.
        
        Args:
            params: Request parameters
            
        Returns:
            Agent card as dictionary
        """
        return self.get_agent_card().to_dict()
    
    def _create_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task.
        
        Args:
            params: Request parameters with optional 'task_id' and 'metadata'
            
        Returns:
            Created task as dictionary
        """
        task_id = params.get("task_id", str(uuid.uuid4()))
        metadata = params.get("metadata", {})
        
        task = Task(
            task_id=task_id,
            status=TaskStatus.PENDING,
            metadata=metadata
        )
        
        self.tasks[task_id] = task
        return task.to_dict()
    
    def _send_task_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to a task.
        
        Args:
            params: Request parameters with 'task_id', 'role', and 'content'
            
        Returns:
            Updated task with agent's response
        """
        task_id = params.get("task_id")
        if not task_id or task_id not in self.tasks:
            raise ValueError(f"Task '{task_id}' not found")
        
        task = self.tasks[task_id]
        
        # Add the incoming message
        message = TaskMessage(
            role=MessageRole(params.get("role", "user")),
            content=params["content"],
            metadata=params.get("metadata")
        )
        task.add_message(message)
        task.status = TaskStatus.IN_PROGRESS
        
        # Process the message and generate response
        try:
            response_content = self.handle_task(task_id, message)
            
            # Add agent's response
            response_message = TaskMessage(
                role=MessageRole.AGENT,
                content=response_content
            )
            task.add_message(response_message)
            task.status = TaskStatus.COMPLETED
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            error_message = TaskMessage(
                role=MessageRole.SYSTEM,
                content=f"Error processing task: {str(e)}"
            )
            task.add_message(error_message)
        
        return task.to_dict()
    
    def _get_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get a task by ID.
        
        Args:
            params: Request parameters with 'task_id'
            
        Returns:
            Task as dictionary
        """
        task_id = params.get("task_id")
        if not task_id or task_id not in self.tasks:
            raise ValueError(f"Task '{task_id}' not found")
        
        return self.tasks[task_id].to_dict()
    
    def _list_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all tasks.
        
        Args:
            params: Request parameters (unused)
            
        Returns:
            Dictionary with list of tasks
        """
        return {
            "tasks": [task.to_dict() for task in self.tasks.values()]
        }
    
    def run(self, debug: bool = False) -> None:
        """Run the agent server.
        
        Args:
            debug: Whether to run in debug mode
        """
        print(f"Starting {self.name} on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=debug)
