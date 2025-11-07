"""Gradio UI for A2A Agent Demo.

This provides a web interface to:
- View and manage available agents
- Start/stop agents (except orchestrator which always runs)
- Chat with the orchestrator agent
- Monitor agent interactions
"""

import gradio as gr
import threading
import time
import subprocess
import sys
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from a2a_demo.client import A2AClient
from a2a_demo.agents import OrchestratorAgent


class AgentManager:
    """Manages agent lifecycle and monitoring."""
    
    def __init__(self):
        self.agents = {
            "OrchestratorAgent": {
                "port": 5003,
                "module": "a2a_demo.agents.orchestrator_agent",
                "description": "Coordinates tasks across multiple specialized agents",
                "process": None,
                "status": "stopped",
                "always_running": True
            },
            "CalculatorAgent": {
                "port": 5001,
                "module": "a2a_demo.agents.calculator_agent",
                "description": "Performs mathematical calculations and solves equations",
                "process": None,
                "status": "stopped",
                "always_running": False
            },
            "TranslatorAgent": {
                "port": 5002,
                "module": "a2a_demo.agents.translator_agent",
                "description": "Translates text between English and Spanish/French/German",
                "process": None,
                "status": "stopped",
                "always_running": False
            }
        }
        self.orchestrator = None
        self.orchestrator_thread = None
        self.interaction_log: List[Dict] = []
    
    def start_orchestrator_embedded(self):
        """Start the orchestrator agent in a separate thread."""
        if self.orchestrator is None:
            self.orchestrator = OrchestratorAgent(port=5003)
            
            def run_orchestrator():
                self.orchestrator.run(debug=False)
            
            self.orchestrator_thread = threading.Thread(target=run_orchestrator, daemon=True)
            self.orchestrator_thread.start()
            time.sleep(2)  # Wait for server to start
            
            # Try to register other agents
            self._try_register_agents()
            
            self.agents["OrchestratorAgent"]["status"] = "running"
    
    def _try_register_agents(self):
        """Try to register running agents with the orchestrator."""
        if self.orchestrator:
            for name, info in self.agents.items():
                if name != "OrchestratorAgent" and self.is_agent_running(name):
                    url = f"http://localhost:{info['port']}"
                    self.orchestrator.register_agent(url)
    
    def start_agent(self, agent_name: str) -> Tuple[bool, str]:
        """Start an agent process."""
        if agent_name not in self.agents:
            return False, f"Unknown agent: {agent_name}"
        
        agent_info = self.agents[agent_name]
        
        if agent_name == "OrchestratorAgent":
            if agent_info["status"] != "running":
                self.start_orchestrator_embedded()
            return True, f"{agent_name} is running"
        
        if agent_info["process"] is not None and agent_info["process"].poll() is None:
            return False, f"{agent_name} is already running"
        
        try:
            # Start agent as subprocess
            process = subprocess.Popen(
                [sys.executable, "-m", agent_info["module"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            agent_info["process"] = process
            agent_info["status"] = "starting"
            
            # Wait a bit and check if it's running
            time.sleep(2)
            if self.is_agent_running(agent_name):
                agent_info["status"] = "running"
                
                # Register with orchestrator if it's running
                if self.orchestrator:
                    url = f"http://localhost:{agent_info['port']}"
                    self.orchestrator.register_agent(url)
                
                self._log_interaction("system", f"{agent_name} started successfully")
                return True, f"{agent_name} started successfully"
            else:
                agent_info["status"] = "failed"
                return False, f"Failed to start {agent_name}"
        
        except Exception as e:
            agent_info["status"] = "error"
            return False, f"Error starting {agent_name}: {str(e)}"
    
    def stop_agent(self, agent_name: str) -> Tuple[bool, str]:
        """Stop an agent process."""
        if agent_name not in self.agents:
            return False, f"Unknown agent: {agent_name}"
        
        agent_info = self.agents[agent_name]
        
        if agent_info["always_running"]:
            return False, f"{agent_name} must always be running"
        
        if agent_info["process"] is None or agent_info["process"].poll() is not None:
            agent_info["status"] = "stopped"
            return False, f"{agent_name} is not running"
        
        try:
            agent_info["process"].terminate()
            agent_info["process"].wait(timeout=5)
            agent_info["process"] = None
            agent_info["status"] = "stopped"
            self._log_interaction("system", f"{agent_name} stopped")
            return True, f"{agent_name} stopped successfully"
        except Exception as e:
            return False, f"Error stopping {agent_name}: {str(e)}"
    
    def is_agent_running(self, agent_name: str) -> bool:
        """Check if an agent is running by trying to connect to it."""
        if agent_name not in self.agents:
            return False
        
        agent_info = self.agents[agent_name]
        try:
            client = A2AClient(f"http://localhost:{agent_info['port']}", timeout=2)
            health = client.health_check()
            is_healthy = health.get("status") == "healthy"
            if is_healthy:
                agent_info["status"] = "running"
            return is_healthy
        except:
            if agent_info["status"] == "running":
                agent_info["status"] = "stopped"
            return False
    
    def get_agent_status(self) -> List[Dict]:
        """Get status of all agents."""
        status_list = []
        for name, info in self.agents.items():
            # Update status by checking if actually running
            is_running = self.is_agent_running(name)
            status_list.append({
                "name": name,
                "port": info["port"],
                "description": info["description"],
                "status": info["status"],
                "running": is_running,
                "always_running": info["always_running"]
            })
        return status_list
    
    def chat_with_orchestrator(self, message: str) -> str:
        """Send a message to the orchestrator and get a response."""
        try:
            client = A2AClient("http://localhost:5003", timeout=10)
            self._log_interaction("user", message)
            
            response = client.chat(message)
            self._log_interaction("orchestrator", response)
            
            return response
        except Exception as e:
            error_msg = f"Error communicating with orchestrator: {str(e)}"
            self._log_interaction("error", error_msg)
            return error_msg
    
    def _log_interaction(self, role: str, message: str):
        """Log an interaction for display."""
        self.interaction_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "role": role,
            "message": message
        })
    
    def get_interaction_log(self) -> str:
        """Get formatted interaction log."""
        if not self.interaction_log:
            return "No interactions yet."
        
        log_text = ""
        for entry in self.interaction_log[-20:]:  # Show last 20 interactions
            timestamp = entry["timestamp"]
            role = entry["role"].upper()
            message = entry["message"]
            log_text += f"[{timestamp}] {role}:\n{message}\n\n"
        
        return log_text
    
    def clear_log(self):
        """Clear the interaction log."""
        self.interaction_log = []


# Global agent manager instance
agent_manager = AgentManager()


def create_agent_status_display() -> str:
    """Create a formatted display of agent statuses."""
    status_list = agent_manager.get_agent_status()
    
    display = "# Agent Status\n\n"
    for agent in status_list:
        status_emoji = "🟢" if agent["running"] else "🔴"
        lock_emoji = "🔒" if agent["always_running"] else ""
        
        display += f"{status_emoji} **{agent['name']}** {lock_emoji}\n"
        display += f"   Port: {agent['port']}\n"
        display += f"   Status: {agent['status']}\n"
        display += f"   {agent['description']}\n\n"
    
    return display


def start_agent_handler(agent_name: str) -> Tuple[str, str]:
    """Handle agent start request."""
    success, message = agent_manager.start_agent(agent_name)
    return create_agent_status_display(), message


def stop_agent_handler(agent_name: str) -> Tuple[str, str]:
    """Handle agent stop request."""
    success, message = agent_manager.stop_agent(agent_name)
    return create_agent_status_display(), message


def chat_handler(message: str, history: List) -> Tuple[List, str]:
    """Handle chat messages."""
    if not message.strip():
        return history, ""
    
    # Add user message to history
    history.append((message, None))
    
    # Get response from orchestrator
    response = agent_manager.chat_with_orchestrator(message)
    
    # Update history with response
    history[-1] = (message, response)
    
    return history, ""


def refresh_status() -> str:
    """Refresh the agent status display."""
    return create_agent_status_display()


def refresh_log() -> str:
    """Refresh the interaction log."""
    return agent_manager.get_interaction_log()


def clear_log_handler() -> str:
    """Clear the interaction log."""
    agent_manager.clear_log()
    return agent_manager.get_interaction_log()


def create_ui():
    """Create the Gradio UI."""
    
    with gr.Blocks(title="A2A Agent Demo", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🤖 Agent-to-Agent (A2A) Protocol Demo")
        gr.Markdown("Manage agents and interact with the orchestrator to coordinate tasks across specialized agents.")
        
        with gr.Row():
            # Left column: Agent management
            with gr.Column(scale=1):
                gr.Markdown("## Agent Management")
                
                agent_status = gr.Markdown(create_agent_status_display())
                
                refresh_btn = gr.Button("🔄 Refresh Status", size="sm")
                
                gr.Markdown("### Control Agents")
                
                with gr.Row():
                    agent_selector = gr.Dropdown(
                        choices=["CalculatorAgent", "TranslatorAgent"],
                        label="Select Agent",
                        value="CalculatorAgent"
                    )
                
                with gr.Row():
                    start_btn = gr.Button("▶️ Start", variant="primary")
                    stop_btn = gr.Button("⏹️ Stop", variant="stop")
                
                control_msg = gr.Textbox(label="Status Message", interactive=False)
                
                gr.Markdown("---")
                gr.Markdown("### Interaction Log")
                
                interaction_log = gr.Textbox(
                    label="Recent Interactions",
                    lines=10,
                    max_lines=15,
                    interactive=False
                )
                
                with gr.Row():
                    refresh_log_btn = gr.Button("🔄 Refresh Log", size="sm")
                    clear_log_btn = gr.Button("🗑️ Clear Log", size="sm")
            
            # Right column: Chat interface
            with gr.Column(scale=2):
                gr.Markdown("## 💬 Chat with Orchestrator")
                gr.Markdown("The orchestrator will route your requests to the appropriate specialized agents.")
                
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=400
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="Message",
                        placeholder="Try: 'list agents', 'calculate 50 * 20', or 'translate hello to spanish'",
                        scale=4
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)
                
                gr.Markdown("### Example Messages")
                gr.Markdown("""
                - `list agents` - See available agents
                - `calculate 100 + 50` - Perform calculation (routed to CalculatorAgent)
                - `x + 15 = 40` - Solve equation (routed to CalculatorAgent)
                - `translate hello to spanish` - Translate text (routed to TranslatorAgent)
                """)
        
        # Event handlers
        start_btn.click(
            start_agent_handler,
            inputs=[agent_selector],
            outputs=[agent_status, control_msg]
        )
        
        stop_btn.click(
            stop_agent_handler,
            inputs=[agent_selector],
            outputs=[agent_status, control_msg]
        )
        
        refresh_btn.click(
            refresh_status,
            outputs=[agent_status]
        )
        
        send_btn.click(
            chat_handler,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        msg_input.submit(
            chat_handler,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        refresh_log_btn.click(
            refresh_log,
            outputs=[interaction_log]
        )
        
        clear_log_btn.click(
            clear_log_handler,
            outputs=[interaction_log]
        )
        
        # Auto-refresh status and log periodically
        demo.load(
            lambda: (create_agent_status_display(), agent_manager.get_interaction_log()),
            outputs=[agent_status, interaction_log],
        )
    
    return demo


if __name__ == "__main__":
    # Start the orchestrator automatically
    print("Starting Orchestrator Agent...")
    agent_manager.start_orchestrator_embedded()
    print("Orchestrator started on port 5003")
    
    # Launch Gradio UI
    print("\nLaunching Gradio UI...")
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
