#!/bin/bash
# Launch script for the Gradio UI

echo "=========================================="
echo "   A2A Agent Demo - Gradio UI Launcher"
echo "=========================================="
echo ""
echo "Starting the web interface..."
echo "The UI will be available at: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
uv run python gradio_ui.py
