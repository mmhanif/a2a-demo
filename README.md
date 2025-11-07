# A2A Protocol Demo Application

A comprehensive demonstration of the **Agent2Agent (A2A) Protocol** implemented in Python. This project showcases how AI agents can discover each other, communicate, and collaborate using standardized JSON-RPC 2.0 over HTTP.

## What is the A2A Protocol?

The Agent2Agent (A2A) protocol is an open standard enabling communication and interoperability between AI agents built on different frameworks, by different companies, running on separate servers. Key features include:

- **Agent Discovery** via Agent Cards describing capabilities
- **Standardized Communication** using JSON-RPC 2.0 over HTTP(S)
- **Task Lifecycle Management** with create, update, and status tracking
- **Flexible Interaction Modes** supporting text, forms, files, and more
- **Opacity Preservation** - agents collaborate without exposing internal state

Learn more at [a2a-protocol.org](https://a2a-protocol.org)

## Project Structure

```
a2a-demo/
├── src/a2a_demo/
│   ├── models/           # A2A protocol data models
│   │   ├── agent_card.py    # Agent Card, Skill definitions
│   │   ├── jsonrpc.py       # JSON-RPC 2.0 models
│   │   └── task.py          # Task and message models
│   ├── agents/           # Agent implementations
│   │   ├── base_agent.py        # Base agent server class
│   │   ├── calculator_agent.py  # Math calculation agent
│   │   ├── translator_agent.py  # Translation agent
│   │   └── orchestrator_agent.py # Multi-agent orchestrator
│   └── client/           # A2A client for communication
│       └── a2a_client.py    # Client implementation
├── tests/                # Unit tests
└── README.md
```

## Features Demonstrated

### 1. **Agent Cards**
Each agent exposes a card describing its capabilities:
- Name and description
- Available skills with parameters
- Supported interaction modes
- Connection information

### 2. **Three Agent Types**

#### CalculatorAgent (Port 5001)
- Performs mathematical calculations
- Solves simple linear equations
- Skills: `calculate`, `solve_equation`

#### TranslatorAgent (Port 5002)
- Translates text between English and Spanish/French/German
- Skill: `translate`

#### OrchestratorAgent (Port 5000)
- Discovers and coordinates other agents
- Routes tasks to appropriate specialized agents
- Skills: `orchestrate`, `discover_agents`

### 3. **JSON-RPC 2.0 Communication**
All agent communication follows JSON-RPC 2.0 standard:
- Request/response pattern
- Error handling
- Method invocation

### 4. **Task Lifecycle**
- Create tasks
- Send messages
- Track status (pending, in_progress, completed, failed)
- Retrieve task history

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
cd a2a-demo
uv sync
```

## Running the Demo

### Option 1: Gradio Web UI (Recommended)

The easiest way to explore the demo is through the interactive web interface:

```bash
# Quick start
uv run python gradio_ui.py

# Or use the launch script
./launch_ui.sh
```

This will:
1. Start the OrchestratorAgent automatically on port 5003
2. Launch the web interface at http://localhost:7860
3. Open your browser to interact with the agents

**Features:**
- 🎛️ **Agent Management**: Start/stop agents with a click
- 💬 **Chat Interface**: Interactive conversation with the orchestrator
- 📋 **Interaction Log**: Monitor all agent communications in real-time
- 🔄 **Auto-refresh**: Status updates every 3 seconds

See [GRADIO_UI_README.md](GRADIO_UI_README.md) for detailed UI documentation.

### Option 2: Run Individual Agents

In separate terminals:

```bash
# Terminal 1 - Calculator Agent
uv run python -m a2a_demo.agents.calculator_agent

# Terminal 2 - Translator Agent  
uv run python -m a2a_demo.agents.translator_agent

# Terminal 3 - Orchestrator Agent
uv run python -m a2a_demo.agents.orchestrator_agent
```

### Option 3: Interactive Python Session

```python
from a2a_demo.client import A2AClient

# Connect to calculator agent
calc_client = A2AClient("http://localhost:5001")

# Get agent capabilities
card = calc_client.get_agent_card()
print(f"Agent: {card.name}")
print(f"Skills: {[s.name for s in card.skills]}")

# Perform calculation
response = calc_client.chat("Calculate 25 * 4")
print(response)  # "The result of 25 * 4 is 100"

# Solve equation
response = calc_client.chat("x + 10 = 25")
print(response)  # "The solution is x = 15"
```

### Option 4: Using the Orchestrator

```python
from a2a_demo.client import A2AClient

# Connect to orchestrator
orch_client = A2AClient("http://localhost:5000")

# List available agents
response = orch_client.chat("list agents")
print(response)

# Orchestrator routes to calculator
response = orch_client.chat("calculate 100 + 50")
print(response)  # Routed to CalculatorAgent

# Orchestrator routes to translator
response = orch_client.chat("translate hello to spanish")
print(response)  # Routed to TranslatorAgent
```

## A2A Protocol Methods

Each agent implements these standard A2A methods:

### `getAgentCard()`
Returns the agent's capability description.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "getAgentCard",
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "name": "CalculatorAgent",
    "description": "An agent that performs mathematical calculations",
    "url": "http://localhost:5001",
    "skills": [
      {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "parameters": {...}
      }
    ]
  }
}
```

### `createTask(params?)`
Creates a new task for interaction.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "createTask",
  "params": {
    "task_id": "optional-custom-id",
    "metadata": {}
  },
  "id": 2
}
```

### `sendTaskMessage(params)`
Sends a message to a task and receives response.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "sendTaskMessage",
  "params": {
    "task_id": "abc-123",
    "role": "user",
    "content": "Calculate 5 + 5"
  },
  "id": 3
}
```

### `getTask(params)`
Retrieves task status and message history.

### `listTasks()`
Lists all tasks on the agent.

## Running Tests

Run the comprehensive unit test suite:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=a2a_demo

# Run specific test file
uv run pytest tests/test_models.py -v

# Run specific test
uv run pytest tests/test_agents.py::TestCalculatorAgent::test_calculate_addition -v
```

## Architecture

### Communication Flow

```
┌─────────────┐                    ┌─────────────┐
│             │   JSON-RPC 2.0     │             │
│   Client    │◄──────────────────►│  Agent 1    │
│             │    over HTTP       │             │
└─────────────┘                    └─────────────┘
       │                                  
       │                                  
       ▼                                  
┌─────────────┐                    ┌─────────────┐
│             │                    │             │
│Orchestrator │◄──────────────────►│  Agent 2    │
│   Agent     │   Agent-to-Agent   │             │
└─────────────┘   Communication    └─────────────┘
```

### Key Components

1. **Models** (`models/`)
   - Data classes for protocol structures
   - JSON serialization/deserialization
   - Type-safe enums for statuses and roles

2. **Base Agent** (`agents/base_agent.py`)
   - Flask-based HTTP server
   - JSON-RPC request handler
   - Standard method implementations
   - Abstract methods for customization

3. **Specialized Agents** (`agents/`)
   - Extend BaseAgent
   - Implement `get_agent_card()` and `handle_task()`
   - Domain-specific logic

4. **A2A Client** (`client/`)
   - Convenience wrapper for agent communication
   - Type-safe method calls
   - Error handling

## Extending the Demo

### Creating a New Agent

```python
from a2a_demo.agents import BaseAgent
from a2a_demo.models import AgentCard, Skill, TaskMessage

class WeatherAgent(BaseAgent):
    def __init__(self, host="0.0.0.0", port=5003):
        super().__init__(
            name="WeatherAgent",
            description="An agent that provides weather information",
            host=host,
            port=port
        )
    
    def get_agent_card(self) -> AgentCard:
        return AgentCard(
            name=self.name,
            description=self.description,
            url=f"http://{self.host}:{self.port}",
            skills=[
                Skill(
                    name="get_weather",
                    description="Get current weather for a location",
                    parameters={
                        "location": {
                            "type": "string",
                            "description": "City name"
                        }
                    }
                )
            ]
        )
    
    def handle_task(self, task_id: str, message: TaskMessage) -> str:
        # Your weather logic here
        return f"Weather info for: {message.content}"

if __name__ == "__main__":
    agent = WeatherAgent()
    agent.run()
```

## Key Concepts

### Agent Cards
Agent Cards are self-describing documents that allow agents to advertise their capabilities without exposing implementation details.

### Task Lifecycle
Tasks represent conversations or work sessions between agents:
1. **Create** - Initialize a new task
2. **Message** - Exchange messages (user → agent → user)
3. **Track** - Monitor status and history
4. **Complete** - Mark task as done

### Agent Opacity
Agents collaborate without sharing:
- Internal prompts or models
- Tool implementations
- Memory or context
- Proprietary algorithms

### Interoperability
Different agent implementations can communicate as long as they follow the A2A protocol standard.

## Resources

- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A Project on GitHub](https://github.com/a2aproject/A2A)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)

## License

This demo application is provided as-is for educational purposes.

## Contributing

Feel free to extend this demo with:
- Additional agent types
- Support for streaming (SSE)
- Authentication mechanisms
- More complex orchestration patterns
- Integration with real AI models