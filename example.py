"""
Example demonstrating A2A protocol usage.

This script shows how to:
1. Start agents programmatically
2. Use the A2A client to communicate
3. Orchestrate multiple agents

Note: This requires agents to be running. Run agents in separate terminals first.
"""

from a2a_demo.client import A2AClient
import time


def demo_calculator():
    """Demonstrate calculator agent functionality."""
    print("\n" + "="*60)
    print("DEMO 1: Calculator Agent")
    print("="*60)
    
    client = A2AClient("http://localhost:5001")
    
    # Get agent card
    print("\n1. Getting agent card...")
    card = client.get_agent_card()
    print(f"   Agent: {card.name}")
    print(f"   Description: {card.description}")
    print(f"   Skills: {', '.join([s.name for s in card.skills])}")
    
    # Perform calculations
    print("\n2. Performing calculations...")
    
    calculations = [
        "25 + 17",
        "100 * 8",
        "(15 + 5) * 3",
        "1000 / 25"
    ]
    
    for calc in calculations:
        response = client.chat(calc)
        print(f"   {calc} = {response}")
    
    # Solve equation
    print("\n3. Solving equation...")
    response = client.chat("x + 15 = 40")
    print(f"   x + 15 = 40 -> {response}")


def demo_translator():
    """Demonstrate translator agent functionality."""
    print("\n" + "="*60)
    print("DEMO 2: Translator Agent")
    print("="*60)
    
    client = A2AClient("http://localhost:5002")
    
    # Get agent card
    print("\n1. Getting agent card...")
    card = client.get_agent_card()
    print(f"   Agent: {card.name}")
    print(f"   Description: {card.description}")
    
    # Translate phrases
    print("\n2. Translating phrases...")
    
    translations = [
        ("hello", "spanish"),
        ("thank you", "french"),
        ("good morning", "german"),
        ("goodbye", "spanish")
    ]
    
    for phrase, language in translations:
        response = client.chat(f"translate {phrase} to {language}")
        print(f"   '{phrase}' -> {language}: {response}")


def demo_orchestrator():
    """Demonstrate orchestrator agent functionality."""
    print("\n" + "="*60)
    print("DEMO 3: Orchestrator Agent")
    print("="*60)
    
    client = A2AClient("http://localhost:5000")
    
    # Get agent card
    print("\n1. Getting orchestrator card...")
    card = client.get_agent_card()
    print(f"   Agent: {card.name}")
    print(f"   Description: {card.description}")
    
    # List available agents
    print("\n2. Listing available agents...")
    response = client.chat("list agents")
    print(response)
    
    # Route calculation to calculator
    print("\n3. Orchestrating calculation (routed to CalculatorAgent)...")
    response = client.chat("calculate 50 * 20")
    print(f"   Response: {response}")
    
    # Route translation to translator
    print("\n4. Orchestrating translation (routed to TranslatorAgent)...")
    response = client.chat("translate hello to spanish")
    print(f"   Response: {response}")


def demo_task_lifecycle():
    """Demonstrate task lifecycle management."""
    print("\n" + "="*60)
    print("DEMO 4: Task Lifecycle")
    print("="*60)
    
    client = A2AClient("http://localhost:5001")
    
    print("\n1. Creating a task...")
    task = client.create_task(metadata={"demo": "task_lifecycle"})
    print(f"   Task ID: {task.task_id}")
    print(f"   Status: {task.status.value}")
    
    print("\n2. Sending first message...")
    task = client.send_message(task.task_id, "10 + 5")
    print(f"   Status: {task.status.value}")
    print(f"   Messages: {len(task.messages)}")
    
    print("\n3. Sending second message...")
    task = client.send_message(task.task_id, "20 * 3")
    print(f"   Status: {task.status.value}")
    print(f"   Messages: {len(task.messages)}")
    
    print("\n4. Retrieving task history...")
    task = client.get_task(task.task_id)
    print(f"   Task has {len(task.messages)} messages:")
    for i, msg in enumerate(task.messages, 1):
        print(f"      {i}. [{msg.role.value}]: {msg.content}")


def check_agent_health(name: str, url: str) -> bool:
    """Check if an agent is running."""
    try:
        client = A2AClient(url)
        health = client.health_check()
        return health.get("status") == "healthy"
    except:
        return False


def main():
    """Run all demos."""
    print("\n" + "#"*60)
    print("# A2A Protocol Demo")
    print("#"*60)
    
    # Check which agents are running
    print("\nChecking agent availability...")
    agents = [
        ("OrchestratorAgent", "http://localhost:5000"),
        ("CalculatorAgent", "http://localhost:5001"),
        ("TranslatorAgent", "http://localhost:5002")
    ]
    
    available = []
    for name, url in agents:
        if check_agent_health(name, url):
            print(f"   ✓ {name} is running")
            available.append((name, url))
        else:
            print(f"   ✗ {name} is NOT running")
    
    if len(available) == 0:
        print("\n⚠️  No agents are running!")
        print("\nPlease start the agents in separate terminals:")
        print("   Terminal 1: uv run python -m a2a_demo.agents.calculator_agent")
        print("   Terminal 2: uv run python -m a2a_demo.agents.translator_agent")
        print("   Terminal 3: uv run python -m a2a_demo.agents.orchestrator_agent")
        return
    
    print(f"\n{len(available)}/{len(agents)} agents are running. Proceeding with demos...\n")
    time.sleep(1)
    
    # Run demos based on available agents
    if any(name == "CalculatorAgent" for name, _ in available):
        demo_calculator()
        time.sleep(1)
        demo_task_lifecycle()
    
    if any(name == "TranslatorAgent" for name, _ in available):
        demo_translator()
    
    if any(name == "OrchestratorAgent" for name, _ in available):
        demo_orchestrator()
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
