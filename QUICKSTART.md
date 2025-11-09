# Quick Start Guide

Get up and running with the A2A Protocol Demo in 5 minutes!

## 1. Installation

```bash
cd a2a-demo
uv sync
```

## 2. Run Tests (Optional)

Verify everything works:

```bash
uv run pytest tests/ -v
```

Expected: All 37 tests should pass ✓

## 3. Start the Agents

Open 3 terminal windows and run:

**Terminal 1 - Calculator Agent:**
```bash
uv run python -m a2a_demo.agents.calculator_agent
```

**Terminal 2 - Translator Agent:**
```bash
uv run python -m a2a_demo.agents.translator_agent
```

**Terminal 3 - Orchestrator Agent:**
```bash
uv run python -m a2a_demo.agents.orchestrator_agent
```

## 4. Run the Demo

In a 4th terminal:

```bash
uv run python example.py
```

This will demonstrate:
- Agent discovery via Agent Cards
- Mathematical calculations
- Text translation
- Agent orchestration
- Task lifecycle management

## 5. Try It Yourself

Start a Python session:

```bash
uv run python
```

Then interact with agents:

```python
from a2a_demo.client import A2AClient
from a2a_demo.config import CALCULATOR_URL, TRANSLATOR_URL, ORCHESTRATOR_URL

# Talk to the calculator
calc = A2AClient(CALCULATOR_URL)
print(calc.chat("100 + 250"))
print(calc.chat("x + 20 = 50"))

# Talk to the translator
trans = A2AClient(TRANSLATOR_URL)
print(trans.chat("translate hello to spanish"))
print(trans.chat("translate thank you to french"))

# Talk to the orchestrator (routes to other agents)
orch = A2AClient(ORCHESTRATOR_URL)
print(orch.chat("list agents"))
print(orch.chat("calculate 15 * 8"))
print(orch.chat("translate goodbye to german"))
```

## What's Happening?

The A2A protocol enables:

1. **Discovery**: Each agent publishes an Agent Card describing its capabilities
2. **Communication**: Agents talk via JSON-RPC 2.0 over HTTP
3. **Task Management**: Conversations are tracked as tasks with message history
4. **Orchestration**: Agents can delegate work to other specialized agents
5. **Opacity**: Agents collaborate without exposing internal implementation

## Next Steps

- Read the full [README.md](README.md) for architecture details
- Explore the code in `src/a2a_demo/`
- Create your own agent by extending `BaseAgent`
- Check out the [A2A Protocol Specification](https://a2a-protocol.org)

## Troubleshooting

**"Connection refused" error?**
- Make sure all 3 agent servers are running
- Confirm they're using the default ports from `a2a_demo.config`

**Import errors?**
- Run `uv sync` to install dependencies
- Make sure you're in the `a2a-demo` directory

**Tests failing?**
- Check Python version (requires 3.10+)
- Try `uv run pytest tests/ -v` for detailed output
