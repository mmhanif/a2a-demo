"""Tests for A2A protocol models."""

import pytest
from a2a_demo.config import DEFAULT_AGENT_URL
from a2a_demo.models import (
    AgentCard,
    Skill,
    InteractionMode,
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCError,
    Task,
    TaskStatus,
    TaskMessage,
    MessageRole,
    PARSE_ERROR,
    METHOD_NOT_FOUND,
)


class TestAgentCard:
    """Test AgentCard model."""
    
    def test_create_agent_card(self):
        """Test creating an agent card."""
        skill = Skill(
            name="test_skill",
            description="A test skill",
            parameters={"param1": "value1"}
        )
        
        card = AgentCard(
            name="TestAgent",
            description="A test agent",
            url=DEFAULT_AGENT_URL,
            skills=[skill],
            version="1.0",
        )
        
        assert card.name == "TestAgent"
        assert card.description == "A test agent"
        assert card.url == DEFAULT_AGENT_URL
        assert len(card.skills) == 1
        assert card.skills[0].name == "test_skill"
    
    def test_agent_card_to_dict(self):
        """Test converting agent card to dictionary."""
        skill = Skill(
            name="test_skill",
            description="A test skill"
        )
        
        card = AgentCard(
            name="TestAgent",
            description="A test agent",
            url=DEFAULT_AGENT_URL,
            skills=[skill],
        )
        
        card_dict = card.to_dict()
        
        assert card_dict["name"] == "TestAgent"
        assert card_dict["description"] == "A test agent"
        assert card_dict["url"] == DEFAULT_AGENT_URL
        assert len(card_dict["skills"]) == 1
        assert card_dict["skills"][0]["name"] == "test_skill"
    
    def test_agent_card_from_dict(self):
        """Test creating agent card from dictionary."""
        data = {
            "name": "TestAgent",
            "description": "A test agent",
            "url": DEFAULT_AGENT_URL,
            "version": "1.0",
            "skills": [
                {
                    "name": "test_skill",
                    "description": "A test skill",
                    "parameters": {},
                    "interaction_modes": ["text"]
                }
            ],
            "supported_interaction_modes": ["text"],
            "metadata": {}
        }
        
        card = AgentCard.from_dict(data)
        
        assert card.name == "TestAgent"
        assert card.description == "A test agent"
        assert len(card.skills) == 1
        assert card.skills[0].name == "test_skill"


class TestJSONRPC:
    """Test JSON-RPC models."""
    
    def test_create_request(self):
        """Test creating a JSON-RPC request."""
        request = JSONRPCRequest(
            method="testMethod",
            params={"param1": "value1"},
            id=1
        )
        
        assert request.method == "testMethod"
        assert request.params == {"param1": "value1"}
        assert request.id == 1
        assert request.jsonrpc == "2.0"
    
    def test_request_to_dict(self):
        """Test converting request to dictionary."""
        request = JSONRPCRequest(
            method="testMethod",
            params={"param1": "value1"},
            id=1
        )
        
        req_dict = request.to_dict()
        
        assert req_dict["jsonrpc"] == "2.0"
        assert req_dict["method"] == "testMethod"
        assert req_dict["params"] == {"param1": "value1"}
        assert req_dict["id"] == 1
    
    def test_request_from_dict(self):
        """Test creating request from dictionary."""
        data = {
            "jsonrpc": "2.0",
            "method": "testMethod",
            "params": {"param1": "value1"},
            "id": 1
        }
        
        request = JSONRPCRequest.from_dict(data)
        
        assert request.method == "testMethod"
        assert request.params == {"param1": "value1"}
        assert request.id == 1
    
    def test_create_response_with_result(self):
        """Test creating a JSON-RPC response with result."""
        response = JSONRPCResponse(
            id=1,
            result={"data": "test"}
        )
        
        assert response.id == 1
        assert response.result == {"data": "test"}
        assert response.error is None
    
    def test_create_response_with_error(self):
        """Test creating a JSON-RPC response with error."""
        error = JSONRPCError(
            code=METHOD_NOT_FOUND,
            message="Method not found"
        )
        
        response = JSONRPCResponse(
            id=1,
            error=error
        )
        
        assert response.id == 1
        assert response.error is not None
        assert response.error.code == METHOD_NOT_FOUND
        assert response.error.message == "Method not found"
    
    def test_response_to_dict(self):
        """Test converting response to dictionary."""
        response = JSONRPCResponse(
            id=1,
            result={"data": "test"}
        )
        
        resp_dict = response.to_dict()
        
        assert resp_dict["jsonrpc"] == "2.0"
        assert resp_dict["id"] == 1
        assert resp_dict["result"] == {"data": "test"}
        assert "error" not in resp_dict


class TestTask:
    """Test Task models."""
    
    def test_create_task(self):
        """Test creating a task."""
        task = Task(
            task_id="test-123",
            status=TaskStatus.PENDING
        )
        
        assert task.task_id == "test-123"
        assert task.status == TaskStatus.PENDING
        assert len(task.messages) == 0
        assert task.created_at is not None
        assert task.updated_at is not None
    
    def test_add_message_to_task(self):
        """Test adding a message to a task."""
        task = Task(
            task_id="test-123",
            status=TaskStatus.PENDING
        )
        
        message = TaskMessage(
            role=MessageRole.USER,
            content="Hello, agent!"
        )
        
        task.add_message(message)
        
        assert len(task.messages) == 1
        assert task.messages[0].content == "Hello, agent!"
        assert task.messages[0].role == MessageRole.USER
    
    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            task_id="test-123",
            status=TaskStatus.COMPLETED
        )
        
        message = TaskMessage(
            role=MessageRole.USER,
            content="Test message"
        )
        task.add_message(message)
        
        task_dict = task.to_dict()
        
        assert task_dict["task_id"] == "test-123"
        assert task_dict["status"] == "completed"
        assert len(task_dict["messages"]) == 1
        assert task_dict["messages"][0]["content"] == "Test message"
    
    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            "task_id": "test-123",
            "status": "in_progress",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello",
                    "timestamp": "2023-01-01T00:00:00Z"
                }
            ],
            "metadata": {},
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:01:00Z"
        }
        
        task = Task.from_dict(data)
        
        assert task.task_id == "test-123"
        assert task.status == TaskStatus.IN_PROGRESS
        assert len(task.messages) == 1
        assert task.messages[0].content == "Hello"
    
    def test_task_message_timestamp(self):
        """Test that task messages get timestamps."""
        message = TaskMessage(
            role=MessageRole.AGENT,
            content="Response"
        )
        
        assert message.timestamp is not None
        assert "Z" in message.timestamp
