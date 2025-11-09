"""Tests for A2A agents."""

import pytest
from unittest.mock import Mock, patch
from a2a_demo.agents import CalculatorAgent, TranslatorAgent, OrchestratorAgent
from a2a_demo.client import A2AClient
from a2a_demo.config import CALCULATOR_URL, DEFAULT_AGENT_URL
from a2a_demo.models import TaskMessage, MessageRole, TaskStatus, InteractionMode


class TestCalculatorAgent:
    """Test CalculatorAgent."""
    
    def test_agent_card(self):
        """Test calculator agent card."""
        agent = CalculatorAgent()
        card = agent.get_agent_card()
        
        assert card.name == "CalculatorAgent"
        assert "calculation" in card.description.lower()
        assert len(card.skills) == 2
        
        skill_names = [skill.name for skill in card.skills]
        assert "calculate" in skill_names
        assert "solve_equation" in skill_names
    
    def test_calculate_addition(self):
        """Test simple addition."""
        agent = CalculatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="5 + 3")
        
        result = agent.handle_task("test-task", message)
        
        assert "8" in result
    
    def test_calculate_multiplication(self):
        """Test multiplication."""
        agent = CalculatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="7 * 6")
        
        result = agent.handle_task("test-task", message)
        
        assert "42" in result
    
    def test_calculate_complex_expression(self):
        """Test complex expression."""
        agent = CalculatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="(10 + 5) * 2")
        
        result = agent.handle_task("test-task", message)
        
        assert "30" in result
    
    def test_solve_simple_equation(self):
        """Test solving simple equation."""
        agent = CalculatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="x + 5 = 10")
        
        result = agent.handle_task("test-task", message)
        
        assert "5" in result or "x = 5" in result
    
    def test_invalid_expression(self):
        """Test handling invalid expression."""
        agent = CalculatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="invalid expression!")
        
        result = agent.handle_task("test-task", message)
        
        assert "invalid" in result.lower() or "error" in result.lower()


class TestTranslatorAgent:
    """Test TranslatorAgent."""
    
    def test_agent_card(self):
        """Test translator agent card."""
        agent = TranslatorAgent()
        card = agent.get_agent_card()
        
        assert card.name == "TranslatorAgent"
        assert "translat" in card.description.lower()
        assert len(card.skills) >= 1
        
        translate_skill = next((s for s in card.skills if s.name == "translate"), None)
        assert translate_skill is not None
    
    def test_translate_to_spanish(self):
        """Test translation to Spanish."""
        agent = TranslatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="translate hello to spanish")
        
        result = agent.handle_task("test-task", message)
        
        assert "hola" in result.lower()
    
    def test_translate_to_french(self):
        """Test translation to French."""
        agent = TranslatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="translate thank you to french")
        
        result = agent.handle_task("test-task", message)
        
        assert "merci" in result.lower()
    
    def test_translate_to_german(self):
        """Test translation to German."""
        agent = TranslatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="translate yes to german")
        
        result = agent.handle_task("test-task", message)
        
        assert "ja" in result.lower()
    
    def test_unsupported_language(self):
        """Test handling unsupported language."""
        agent = TranslatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="translate hello to japanese")
        
        result = agent.handle_task("test-task", message)
        
        assert "unsupported" in result.lower() or "support" in result.lower()
    
    def test_unknown_phrase(self):
        """Test handling unknown phrase."""
        agent = TranslatorAgent()
        message = TaskMessage(role=MessageRole.USER, content="translate unknown phrase to spanish")
        
        result = agent.handle_task("test-task", message)
        
        assert "don't have" in result.lower() or "demo" in result.lower()


class TestOrchestratorAgent:
    """Test OrchestratorAgent."""
    
    def test_agent_card(self):
        """Test orchestrator agent card."""
        agent = OrchestratorAgent()
        card = agent.get_agent_card()
        
        assert card.name == "OrchestratorAgent"
        assert "orchestrat" in card.description.lower()
        assert len(card.skills) >= 2
        
        skill_names = [skill.name for skill in card.skills]
        assert "orchestrate" in skill_names
        assert "discover_agents" in skill_names
    
    def test_list_agents_empty(self):
        """Test listing agents when none registered."""
        agent = OrchestratorAgent()
        message = TaskMessage(role=MessageRole.USER, content="list agents")
        
        result = agent.handle_task("test-task", message)
        
        assert "no agents" in result.lower()
    
    @patch('a2a_demo.agents.orchestrator_agent.requests.post')
    def test_register_agent(self, mock_post):
        """Test registering an agent."""
        # Mock the response from getAgentCard
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "name": "TestAgent",
                "description": "A test agent",
                "url": CALCULATOR_URL,
                "skills": [],
                "supported_interaction_modes": ["text"],
                "version": "1.0",
                "metadata": {},
            }
        }
        mock_post.return_value = mock_response
        
        agent = OrchestratorAgent()
        success = agent.register_agent(CALCULATOR_URL)
        
        assert success is True
        assert "TestAgent" in agent.registered_agents
    
    def test_list_agents_with_registered(self):
        """Test listing agents with registered agents."""
        agent = OrchestratorAgent()
        
        # Manually add a mock agent card
        from a2a_demo.models import AgentCard, Skill
        test_card = AgentCard(
            name="TestAgent",
            description="A test agent",
            url=CALCULATOR_URL,
            skills=[Skill(name="test", description="test skill")],
        )
        agent.registered_agents["TestAgent"] = test_card
        
        message = TaskMessage(role=MessageRole.USER, content="list agents")
        result = agent.handle_task("test-task", message)
        
        assert "TestAgent" in result
        assert "1 agent" in result.lower()


class TestBaseAgent:
    """Test BaseAgent functionality."""
    
    def test_create_task(self):
        """Test task creation."""
        agent = CalculatorAgent()
        params = {}
        
        result = agent._create_task(params)
        
        assert "task_id" in result
        assert result["status"] == TaskStatus.PENDING.value
    
    def test_send_task_message(self):
        """Test sending task message."""
        agent = CalculatorAgent()
        
        # Create task first
        task_result = agent._create_task({})
        task_id = task_result["task_id"]
        
        # Send message
        params = {
            "task_id": task_id,
            "content": "5 + 5",
            "role": "user"
        }
        
        result = agent._send_task_message(params)
        
        assert result["task_id"] == task_id
        assert len(result["messages"]) >= 2  # User message + agent response
        assert result["status"] == TaskStatus.COMPLETED.value
    
    def test_get_task(self):
        """Test getting a task."""
        agent = CalculatorAgent()
        
        # Create task
        task_result = agent._create_task({})
        task_id = task_result["task_id"]
        
        # Get task
        result = agent._get_task({"task_id": task_id})
        
        assert result["task_id"] == task_id
        assert "status" in result
    
    def test_list_tasks(self):
        """Test listing tasks."""
        agent = CalculatorAgent()
        
        # Create a couple of tasks
        agent._create_task({})
        agent._create_task({})
        
        result = agent._list_tasks({})
        
        assert "tasks" in result
        assert len(result["tasks"]) == 2


class TestA2AClient:
    """Test A2AClient."""
    
    @patch('a2a_demo.client.a2a_client.requests.post')
    def test_get_agent_card(self, mock_post):
        """Test getting agent card via client."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "name": "TestAgent",
                "description": "A test agent",
                "url": DEFAULT_AGENT_URL,
                "skills": [],
                "supported_interaction_modes": ["text"],
                "version": "1.0",
                "metadata": {}
            }
        }
        mock_post.return_value = mock_response
        
        client = A2AClient(DEFAULT_AGENT_URL)
        card = client.get_agent_card()
        
        assert card.name == "TestAgent"
        assert card.description == "A test agent"
    
    @patch('a2a_demo.client.a2a_client.requests.post')
    def test_create_task(self, mock_post):
        """Test creating a task via client."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "task_id": "test-123",
                "status": "pending",
                "messages": [],
                "metadata": {},
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }
        mock_post.return_value = mock_response
        
        client = A2AClient(DEFAULT_AGENT_URL)
        task = client.create_task()
        
        assert task.task_id == "test-123"
        assert task.status == TaskStatus.PENDING
    
    @patch('a2a_demo.client.a2a_client.requests.get')
    def test_health_check(self, mock_get):
        """Test health check via client."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "agent": "TestAgent"
        }
        mock_get.return_value = mock_response
        
        client = A2AClient(DEFAULT_AGENT_URL)
        health = client.health_check()
        
        assert health["status"] == "healthy"
        assert health["agent"] == "TestAgent"
