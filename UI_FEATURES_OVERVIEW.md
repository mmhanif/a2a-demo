# Gradio UI Features Overview

## Visual Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                🤖 Agent-to-Agent (A2A) Protocol Demo                 │
│     Manage agents and interact with the orchestrator to coordinate  │
│                   tasks across specialized agents                    │
├───────────────────────────┬─────────────────────────────────────────┤
│                           │                                         │
│   Agent Management        │     💬 Chat with Orchestrator           │
│   ─────────────────       │     ────────────────────────            │
│                           │                                         │
│   # Agent Status          │   The orchestrator will route your      │
│                           │   requests to the appropriate agents.   │
│   🟢 OrchestratorAgent 🔒 │                                         │
│      Port: 5003           │   ┌─────────────────────────────────┐  │
│      Status: running      │   │                                 │  │
│      Coordinates tasks... │   │  [Chat History Shows Here]      │  │
│                           │   │                                 │  │
│   🔴 CalculatorAgent      │   │  User: list agents              │  │
│      Port: 5001           │   │  Agent: I have access to...     │  │
│      Status: stopped      │   │                                 │  │
│      Performs math...     │   │  User: calculate 50 * 20        │  │
│                           │   │  Agent: Calculator: The         │  │
│   🔴 TranslatorAgent      │   │         result is 1000          │  │
│      Port: 5002           │   │                                 │  │
│      Status: stopped      │   └─────────────────────────────────┘  │
│      Translates text...   │                                         │
│                           │   Message: ________________________    │
│   [🔄 Refresh Status]     │            [Send]                       │
│                           │                                         │
│   Control Agents          │   ### Example Messages                  │
│   ───────────────         │   - list agents                         │
│                           │   - calculate 100 + 50                  │
│   [CalculatorAgent ▼]     │   - x + 15 = 40                        │
│   [▶️ Start] [⏹️ Stop]    │   - translate hello to spanish         │
│                           │                                         │
│   Status Message:         │                                         │
│   ________________         │                                         │
│                           │                                         │
│   ───────────────────     │                                         │
│   Interaction Log         │                                         │
│   ─────────────           │                                         │
│                           │                                         │
│   [14:30:22] USER:        │                                         │
│   list agents             │                                         │
│                           │                                         │
│   [14:30:22] ORCHESTRATOR:│                                         │
│   I have access to 2...   │                                         │
│                           │                                         │
│   [14:30:45] SYSTEM:      │                                         │
│   CalculatorAgent started │                                         │
│                           │                                         │
│   [🔄 Refresh] [🗑️ Clear] │                                         │
│                           │                                         │
└───────────────────────────┴─────────────────────────────────────────┘
```

## Key Features

### 🎛️ Agent Management Panel (Left Side)

#### 1. Agent Status Display
- **Real-time indicators**:
  - 🟢 = Agent is running and healthy
  - 🔴 = Agent is stopped
  - 🔒 = Always-running (cannot be stopped)
- **Information shown**:
  - Agent name
  - Port number
  - Current status
  - Brief description
- **Auto-refresh**: Updates every 3 seconds
- **Manual refresh**: Click "🔄 Refresh Status" button

#### 2. Agent Control
- **Dropdown selector**: Choose which agent to control
  - CalculatorAgent
  - TranslatorAgent
  - (OrchestratorAgent not selectable - always running)
- **Start button (▶️)**: Launch a stopped agent
- **Stop button (⏹️)**: Terminate a running agent
- **Status message**: Shows result of start/stop operations

#### 3. Interaction Log
- **Timestamped entries**: Every interaction marked with [HH:MM:SS]
- **Role indicators**: USER, ORCHESTRATOR, SYSTEM, ERROR
- **Shows last 20 interactions**: Automatically scrolls
- **Manual controls**:
  - "🔄 Refresh Log" - Update the display
  - "🗑️ Clear Log" - Reset the log

### 💬 Chat Interface (Right Side)

#### 1. Conversation Display
- **Full chat history**: All messages preserved
- **Turn-by-turn format**: User message → Agent response
- **Auto-scroll**: Newest messages at bottom
- **Persistent**: History maintained during session

#### 2. Message Input
- **Text input field**: Type your message
- **Send button**: Click to submit
- **Enter key**: Press Enter to send
- **Auto-clear**: Input clears after sending

#### 3. Example Messages
- **Quick reference**: Common commands displayed
- **Copy-paste ready**: Just copy and use
- **Categories**:
  - Discovery: `list agents`
  - Calculation: `calculate 100 + 50`
  - Equations: `x + 15 = 40`
  - Translation: `translate hello to spanish`

## Workflow Examples

### Scenario 1: First-Time User

```
1. Launch UI
   └─→ Orchestrator automatically starts (🟢)
   
2. Type "list agents" in chat
   └─→ See available agents
   
3. Select "CalculatorAgent" from dropdown
   └─→ Click "▶️ Start"
   └─→ Wait for 🟢 indicator
   
4. Type "calculate 100 * 50" in chat
   └─→ Get result: "The result of 100 * 50 is 5000"
```

### Scenario 2: Testing Agent Routing

```
1. Start both CalculatorAgent and TranslatorAgent
   
2. Send mixed messages:
   - "calculate 25 + 75"
     └─→ Routes to Calculator
   
   - "translate hello to french"
     └─→ Routes to Translator
   
   - "x + 10 = 30"
     └─→ Routes to Calculator
   
3. Check Interaction Log to see routing decisions
```

### Scenario 3: Agent Lifecycle Management

```
1. Start CalculatorAgent
   └─→ Status shows 🟢
   └─→ Log shows "CalculatorAgent started successfully"
   
2. Test calculation
   └─→ "calculate 50 * 2"
   └─→ Works correctly
   
3. Stop CalculatorAgent
   └─→ Status shows 🔴
   └─→ Log shows "CalculatorAgent stopped"
   
4. Try calculation again
   └─→ Error message (agent not available)
```

## Special Indicators

### Status Emojis
- 🟢 **Green Circle**: Agent is healthy and responding
- 🔴 **Red Circle**: Agent is not running
- 🔒 **Lock**: Agent cannot be stopped (always running)
- ⏹️ **Stop Square**: Button to stop agent
- ▶️ **Play Triangle**: Button to start agent
- 🔄 **Refresh Arrows**: Update display manually
- 🗑️ **Trash**: Clear the log

### Log Role Indicators
```
[14:30:22] USER:         ← Messages you send
[14:30:22] ORCHESTRATOR: ← Responses from orchestrator
[14:30:22] SYSTEM:       ← UI system messages (start/stop)
[14:30:22] ERROR:        ← Error messages
```

## Auto-Refresh Behavior

Every 3 seconds, the UI automatically:
1. ✅ Checks health of all agents (HTTP /health endpoint)
2. ✅ Updates status indicators (🟢/🔴)
3. ✅ Refreshes agent status text
4. ✅ Updates interaction log display

You can also manually refresh at any time with the refresh buttons.

## Communication Flow

```
User types message
    ↓
[Send Button]
    ↓
AgentManager.chat_with_orchestrator()
    ↓
A2AClient.chat() → HTTP POST to localhost:5003
    ↓
OrchestratorAgent receives request
    ↓
Orchestrator analyzes message content
    ↓
    ├─→ Math keywords? → Route to CalculatorAgent
    ├─→ Translation keywords? → Route to TranslatorAgent
    └─→ Meta queries? → Handle directly
    ↓
Specialized agent processes request
    ↓
Response flows back through chain
    ↓
Displayed in chat interface
    ↓
Logged in interaction log
```

## Ports Reference

| Component | Port | Always Running? |
|-----------|------|-----------------|
| Gradio UI | 7860 | While UI is active |
| OrchestratorAgent | 5003 | Yes (embedded) |
| CalculatorAgent | 5001 | On-demand |
| TranslatorAgent | 5002 | On-demand |

## Keyboard Shortcuts

- **Enter**: Send message (when in message input)
- **Ctrl+C**: Stop the UI (in terminal)

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## Performance Notes

- **Startup time**: ~2-3 seconds for orchestrator to initialize
- **Agent start time**: ~2 seconds per agent
- **Response time**: Typically < 1 second per message
- **Auto-refresh impact**: Minimal (lightweight health checks)
- **Memory usage**: ~100-200MB total for all components

## Tips & Tricks

1. **Fast Testing**: Keep agents running between tests, just refresh the page
2. **Debug Mode**: Check interaction log for detailed message flow
3. **Multiple Tabs**: Open multiple browser tabs to test concurrency
4. **Log Management**: Clear log periodically if it gets too long
5. **Quick Restart**: Ctrl+C and relaunch to reset everything

---

**Everything works without modifying existing agent code!** 🎉
