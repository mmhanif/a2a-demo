# Gradio UI for A2A Agent Demo

A web-based interface for managing and interacting with A2A (Agent-to-Agent) protocol agents.

## Features

### 🎛️ Agent Management
- **Real-time Status Display**: View the status of all agents (OrchestratorAgent, CalculatorAgent, TranslatorAgent)
- **Start/Stop Controls**: Manage agent lifecycle with simple buttons
- **Auto-refresh**: Agent status updates automatically every 3 seconds
- **Always-Running Orchestrator**: The OrchestratorAgent runs continuously and cannot be stopped

### 💬 Chat Interface
- **Direct Communication**: Chat with the OrchestratorAgent through an intuitive interface
- **Automatic Routing**: The orchestrator intelligently routes requests to specialized agents
- **Conversation History**: All messages are preserved in the chat window

### 📋 Interaction Log
- **Monitor Agent Communication**: See all interactions between user, orchestrator, and specialized agents
- **Timestamps**: Each interaction is timestamped for tracking
- **Clear/Refresh**: Manage the log with convenient controls

## Installation

1. Install dependencies:
```bash
cd a2a-demo
uv sync
```

This will install all required packages including Gradio.

## Running the UI

### Quick Start

Simply run:
```bash
uv run python gradio_ui.py
```

This will:
1. Automatically start the OrchestratorAgent on port 5000
2. Launch the Gradio web interface on port 7860
3. Open your browser to `http://localhost:7860`

### Step-by-Step Usage

1. **Launch the UI**:
   ```bash
   uv run python gradio_ui.py
   ```

2. **Start Agents**:
   - The OrchestratorAgent starts automatically (indicated by 🟢 and 🔒)
   - Select CalculatorAgent or TranslatorAgent from the dropdown
   - Click "▶️ Start" to launch the agent
   - Wait for the status to change to 🟢 (running)

3. **Chat with the Orchestrator**:
   - Type messages in the chat input field
   - Press Enter or click "Send"
   - The orchestrator will route your request to the appropriate agent

4. **Monitor Interactions**:
   - View the Interaction Log to see all agent communications
   - Use "🔄 Refresh Log" to update manually
   - Use "🗑️ Clear Log" to reset the log

## Example Interactions

### List Available Agents
```
User: list agents
Orchestrator: I have access to 2 agent(s):

**CalculatorAgent**
  Description: An agent that performs basic mathematical calculations
  Skills:
    - calculate: Perform mathematical calculations
    - solve_equation: Solve simple linear equations

**TranslatorAgent**
  Description: An agent that translates text between English and other languages
  Skills:
    - translate: Translate text from English to Spanish, French, or German
```

### Perform Calculations
```
User: calculate 50 * 20
Orchestrator: Calculator: The result of 50 * 20 is 1000
```

### Solve Equations
```
User: x + 15 = 40
Orchestrator: Calculator: The solution is x = 25
```

### Translate Text
```
User: translate hello to spanish
Orchestrator: Translator: "hello" in spanish is "hola"
```

## UI Components

### Left Panel: Agent Management
- **Agent Status**: Shows all agents with status indicators
  - 🟢 = Running
  - 🔴 = Stopped
  - 🔒 = Always running (cannot be stopped)
- **Control Agents**: Dropdown to select and start/stop agents
- **Interaction Log**: Real-time log of all communications

### Right Panel: Chat Interface
- **Conversation**: Full chat history with the orchestrator
- **Message Input**: Type and send messages
- **Example Messages**: Quick reference for supported commands

## Architecture

The UI consists of:

1. **AgentManager Class**: 
   - Manages agent lifecycle (start/stop)
   - Monitors agent health
   - Logs interactions
   - Handles communication with agents

2. **Gradio Interface**:
   - Two-column layout
   - Auto-refreshing status displays
   - Event handlers for all interactions
   - Responsive design

3. **Agent Communication**:
   - Uses A2AClient for all agent communication
   - Orchestrator runs in embedded mode (same process)
   - Other agents run as separate subprocesses
   - All communication follows A2A protocol (JSON-RPC 2.0)

## Technical Details

### Ports
- Orchestrator: 5003
- CalculatorAgent: 5001
- TranslatorAgent: 5002
- Gradio UI: 7860

### Agent Lifecycle
- **Orchestrator**: Starts automatically in a daemon thread within the UI process
- **Other Agents**: Start as separate Python subprocesses
- **Health Checks**: Performed via HTTP requests to agent `/health` endpoints
- **Registration**: Agents automatically register with orchestrator when started

### Auto-Refresh
- Agent status refreshes every 3 seconds
- Interaction log refreshes every 3 seconds
- Status can also be refreshed manually with buttons

## Troubleshooting

### Agents Won't Start
- Ensure ports 5000-5002 are available
- Check the Status Message field for error details
- Verify agents can be started manually: `uv run python -m a2a_demo.agents.calculator_agent`

### Orchestrator Not Responding
- Check that the orchestrator status shows 🟢
- Try refreshing the page
- Restart the UI application

### Agents Don't Show as Running
- Wait a few seconds after starting (agents take time to initialize)
- Click "🔄 Refresh Status" to update manually
- Check the Interaction Log for error messages

## Stopping the UI

To stop the UI and all agents:
1. Press `Ctrl+C` in the terminal
2. This will stop the Gradio server and terminate all agent subprocesses

## Development Notes

- The UI does not modify any existing agent code
- All agent management is done through subprocess spawning
- The orchestrator runs in embedded mode for better integration
- Interaction logging happens at the UI level, not within agents
