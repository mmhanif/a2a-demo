"""Orchestrator agent that coordinates multiple agents."""

import requests
from typing import Dict, List
from ..models import AgentCard, Skill, TaskMessage, InteractionMode, JSONRPCRequest
from .base_agent import BaseAgent


class OrchestratorAgent(BaseAgent):
    """An agent that orchestrates tasks across multiple other agents."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5000):
        """Initialize the orchestrator agent."""
        super().__init__(
            name="OrchestratorAgent",
            description="An orchestrator that coordinates tasks across multiple specialized agents",
            host=host,
            port=port
        )
        self.registered_agents: Dict[str, AgentCard] = {}
    
    def get_agent_card(self) -> AgentCard:
        """Return the agent card for the orchestrator."""
        return AgentCard(
            name=self.name,
            description=self.description,
            url=f"http://{self.host}:{self.port}",
            skills=[
                Skill(
                    name="orchestrate",
                    description="Coordinate tasks across multiple agents",
                    parameters={
                        "task": {
                            "type": "string",
                            "description": "Complex task that may require multiple agents"
                        }
                    },
                    interaction_modes=[InteractionMode.TEXT]
                ),
                Skill(
                    name="discover_agents",
                    description="Discover and list available agents",
                    parameters={},
                    interaction_modes=[InteractionMode.TEXT]
                )
            ],
            supported_interaction_modes=[InteractionMode.TEXT],
            metadata={"version": "1.0.0", "type": "orchestrator"}
        )
    
    def register_agent(self, agent_url: str) -> bool:
        """Register an agent by fetching its agent card.
        
        Args:
            agent_url: URL of the agent to register
            
        Returns:
            True if registration successful
        """
        try:
            # Fetch agent card
            response = requests.post(
                agent_url,
                json=JSONRPCRequest(method="getAgentCard", id=1).to_dict(),
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    agent_card = AgentCard.from_dict(result["result"])
                    self.registered_agents[agent_card.name] = agent_card
                    print(f"Registered agent: {agent_card.name}")
                    return True
            
            return False
        except Exception as e:
            print(f"Error registering agent at {agent_url}: {e}")
            return False
    
    def handle_task(self, task_id: str, message: TaskMessage) -> str:
        """Process an orchestration request.
        
        Args:
            task_id: The task ID
            message: The message containing the request
            
        Returns:
            The orchestrated response
        """
        content = message.content.lower().strip()
        
        # Check if this is a discovery request
        if "list agents" in content or "discover agents" in content or "what agents" in content:
            return self._list_agents()
        
        # Try to route to appropriate agent
        return self._orchestrate_task(content)
    
    def _list_agents(self) -> str:
        """List all registered agents and their capabilities.
        
        Returns:
            Description of registered agents
        """
        if not self.registered_agents:
            return "No agents are currently registered. Please register agents using the orchestrator's register_agent() method."
        
        result = f"I have access to {len(self.registered_agents)} agent(s):\n\n"
        
        for agent_name, agent_card in self.registered_agents.items():
            result += f"**{agent_name}**\n"
            result += f"  Description: {agent_card.description}\n"
            result += f"  Skills:\n"
            for skill in agent_card.skills:
                result += f"    - {skill.name}: {skill.description}\n"
            result += "\n"
        
        return result
    
    def _orchestrate_task(self, content: str) -> str:
        """Orchestrate a task by routing to appropriate agents.
        
        Args:
            content: The task content
            
        Returns:
            Result from the appropriate agent(s)
        """
        # Simple routing logic based on keywords
        results = []
        
        # Check for calculator tasks
        if any(word in content for word in ["calculate", "solve", "+", "-", "*", "/", "=", "equation"]):
            calc_agent = self.registered_agents.get("CalculatorAgent")
            if calc_agent:
                result = self._delegate_to_agent(calc_agent, content)
                results.append(f"Calculator: {result}")
        
        # Check for translation tasks
        if any(word in content for word in ["translate", "spanish", "french", "german"]):
            translator_agent = self.registered_agents.get("TranslatorAgent")
            if translator_agent:
                result = self._delegate_to_agent(translator_agent, content)
                results.append(f"Translator: {result}")
        
        if results:
            return "\n\n".join(results)
        
        return f"I'm not sure which agent can handle this task. Available agents: {', '.join(self.registered_agents.keys())}"
    
    def _delegate_to_agent(self, agent_card: AgentCard, content: str) -> str:
        """Delegate a task to a specific agent.
        
        Args:
            agent_card: The agent to delegate to
            content: The task content
            
        Returns:
            Result from the agent
        """
        try:
            # Create task on the target agent
            create_response = requests.post(
                agent_card.url,
                json=JSONRPCRequest(method="createTask", id=1).to_dict(),
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if create_response.status_code != 200:
                return f"Failed to create task on {agent_card.name}"
            
            task_data = create_response.json()["result"]
            task_id = task_data["task_id"]
            
            # Send message to the task
            message_response = requests.post(
                agent_card.url,
                json=JSONRPCRequest(
                    method="sendTaskMessage",
                    params={
                        "task_id": task_id,
                        "role": "user",
                        "content": content
                    },
                    id=2
                ).to_dict(),
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if message_response.status_code != 200:
                return f"Failed to send message to {agent_card.name}"
            
            # Extract the agent's response
            result = message_response.json()["result"]
            messages = result.get("messages", [])
            
            # Find the last agent message
            for msg in reversed(messages):
                if msg["role"] == "agent":
                    return msg["content"]
            
            return "No response from agent"
            
        except Exception as e:
            return f"Error delegating to {agent_card.name}: {str(e)}"


if __name__ == "__main__":
    agent = OrchestratorAgent()
    
    # Register other agents (assuming they're running)
    agent.register_agent("http://localhost:5001")  # Calculator
    agent.register_agent("http://localhost:5002")  # Translator
    
    agent.run(debug=True)
