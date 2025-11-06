"""A2A client for communicating with agents."""

import requests
import uuid
from typing import Optional, Dict, Any, List

from ..models import (
    AgentCard, JSONRPCRequest, JSONRPCResponse,
    Task, TaskMessage, MessageRole
)


class A2AClient:
    """Client for interacting with A2A agents."""
    
    def __init__(self, agent_url: str, timeout: int = 10):
        """Initialize the A2A client.
        
        Args:
            agent_url: Base URL of the agent to communicate with
            timeout: Request timeout in seconds
        """
        self.agent_url = agent_url.rstrip("/")
        self.timeout = timeout
        self._request_id = 0
    
    def _next_id(self) -> int:
        """Generate next request ID.
        
        Returns:
            Next request ID
        """
        self._request_id += 1
        return self._request_id
    
    def _call_method(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Call a JSON-RPC method on the agent.
        
        Args:
            method: Method name
            params: Method parameters
            
        Returns:
            Result from the method call
            
        Raises:
            Exception: If the call fails
        """
        request = JSONRPCRequest(
            method=method,
            params=params,
            id=self._next_id()
        )
        
        try:
            response = requests.post(
                self.agent_url,
                json=request.to_dict(),
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            rpc_response = JSONRPCResponse.from_dict(response.json())
            
            if rpc_response.error:
                raise Exception(
                    f"RPC Error {rpc_response.error.code}: {rpc_response.error.message}"
                )
            
            return rpc_response.result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get_agent_card(self) -> AgentCard:
        """Get the agent card from the agent.
        
        Returns:
            AgentCard describing the agent's capabilities
        """
        result = self._call_method("getAgentCard")
        return AgentCard.from_dict(result)
    
    def create_task(self, task_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Task:
        """Create a new task on the agent.
        
        Args:
            task_id: Optional task ID (generated if not provided)
            metadata: Optional task metadata
            
        Returns:
            Created Task object
        """
        params = {}
        if task_id:
            params["task_id"] = task_id
        if metadata:
            params["metadata"] = metadata
        
        result = self._call_method("createTask", params)
        return Task.from_dict(result)
    
    def send_message(
        self,
        task_id: str,
        content: str,
        role: MessageRole = MessageRole.USER,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Task:
        """Send a message to a task.
        
        Args:
            task_id: Task ID to send the message to
            content: Message content
            role: Message role
            metadata: Optional message metadata
            
        Returns:
            Updated Task object with agent's response
        """
        params = {
            "task_id": task_id,
            "content": content,
            "role": role.value
        }
        if metadata:
            params["metadata"] = metadata
        
        result = self._call_method("sendTaskMessage", params)
        return Task.from_dict(result)
    
    def get_task(self, task_id: str) -> Task:
        """Get a task by ID.
        
        Args:
            task_id: Task ID to retrieve
            
        Returns:
            Task object
        """
        result = self._call_method("getTask", {"task_id": task_id})
        return Task.from_dict(result)
    
    def list_tasks(self) -> List[Task]:
        """List all tasks on the agent.
        
        Returns:
            List of Task objects
        """
        result = self._call_method("listTasks")
        return [Task.from_dict(task_data) for task_data in result["tasks"]]
    
    def chat(self, message: str, task_id: Optional[str] = None) -> str:
        """Simple chat interface - send a message and get a response.
        
        Args:
            message: Message to send
            task_id: Optional existing task ID. If not provided, creates new task.
            
        Returns:
            Agent's response content
        """
        # Create task if not provided
        if not task_id:
            task = self.create_task()
            task_id = task.task_id
        
        # Send message and get response
        updated_task = self.send_message(task_id, message)
        
        # Extract the last agent message
        for msg in reversed(updated_task.messages):
            if msg.role == MessageRole.AGENT:
                return msg.content
        
        return "No response from agent"
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the agent.
        
        Returns:
            Health status dictionary
        """
        try:
            response = requests.get(
                f"{self.agent_url}/health",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
