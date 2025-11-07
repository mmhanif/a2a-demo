# Quick Start Guide - Gradio UI

Get started with the A2A Agent Demo web interface in 3 simple steps!

## Step 1: Install Dependencies

```bash
cd a2a-demo
uv sync
```

## Step 2: Launch the UI

```bash
uv run python gradio_ui.py
```

Or use the convenience script:
```bash
./launch_ui.sh
```

## Step 3: Open Your Browser

The UI will automatically open at: **http://localhost:7860**

If it doesn't open automatically, navigate to that URL in your browser.

---

## What You'll See

### 🟢 OrchestratorAgent (Running)
The orchestrator starts automatically and is always available.

### 🔴 CalculatorAgent (Stopped)
### 🔴 TranslatorAgent (Stopped)
These agents are stopped initially. You can start them from the UI.

---

## First Steps

### 1. Chat with the Orchestrator (No Additional Agents Needed)

Try these commands right away:

```
list agents
```

This shows which agents are available to the orchestrator.

### 2. Start the Calculator Agent

1. In the "Control Agents" section, select **CalculatorAgent** from the dropdown
2. Click **▶️ Start**
3. Wait a few seconds for the status to show 🟢

### 3. Try a Calculation

In the chat box, type:
```
calculate 100 * 50
```

The orchestrator will route this to the CalculatorAgent and return the result!

### 4. Start the Translator Agent

1. Select **TranslatorAgent** from the dropdown
2. Click **▶️ Start**
3. Wait for 🟢 status

### 5. Try a Translation

```
translate hello to spanish
```

The orchestrator will route this to the TranslatorAgent!

---

## More Examples to Try

### Calculations
```
25 + 75
(10 + 5) * 3
1000 / 25
```

### Equations
```
x + 15 = 40
2x + 5 = 15
```

### Translations
```
translate thank you to french
translate goodbye to german
translate good morning to spanish
```

### Mixed Commands
```
calculate 50 * 20
translate hello to french
list agents
x + 10 = 25
```

---

## Understanding the UI

### Left Panel
- **Agent Status**: Real-time status with 🟢/🔴 indicators
- **Control Agents**: Start/stop individual agents
- **Interaction Log**: See all communications with timestamps

### Right Panel
- **Chat Interface**: Talk to the orchestrator
- **Example Messages**: Quick reference for commands

---

## Stopping the UI

Press **Ctrl+C** in the terminal where you launched the UI.

This will:
- Stop the Gradio web server
- Stop all running agents
- Clean up all processes

---

## Troubleshooting

### Agent won't start?
- Make sure the port isn't already in use
- Check the Status Message for errors
- Try clicking "🔄 Refresh Status"

### Orchestrator not responding?
- Verify the orchestrator shows 🟢 (green)
- Try refreshing your browser
- Restart the UI with Ctrl+C and relaunch

### Chat not working?
- Ensure at least one specialized agent is running (🟢)
- Check the Interaction Log for error messages

---

## Next Steps

- Read [GRADIO_UI_README.md](GRADIO_UI_README.md) for detailed documentation
- Read [README.md](README.md) to learn about the A2A protocol
- Check [UI_IMPLEMENTATION_SUMMARY.md](UI_IMPLEMENTATION_SUMMARY.md) for technical details

## Enjoy! 🚀

You're now ready to explore the Agent-to-Agent protocol through an easy-to-use web interface!
