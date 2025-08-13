#!/usr/bin/env python3
"""Quick start script for Ollama Agent"""

from ollama_agent import OllamaAgent


def test_without_ollama():
    """Test agent functionality without Ollama running"""
    print("🧪 TESTING AGENT (without Ollama)")
    print("=" * 40)
    
    agent = OllamaAgent("TestBot", "assistant")
    
    # This will show fallback responses
    tasks = [
        "Help me buy a laptop",
        "Price my used car",
        "Negotiate a deal"
    ]
    
    for task in tasks:
        response = agent.think(task)
        print(f"Task: {task}")
        print(f"Response: {response}\n")


def run_with_ollama():
    """Run agent with Ollama (requires Ollama running)"""
    print("🤖 RUNNING WITH OLLAMA")
    print("=" * 40)
    
    agent = OllamaAgent("AI_Assistant", "helpful_agent")
    
    # Interactive mode
    print("Type 'quit' to exit")
    while True:
        task = input("\nEnter task: ").strip()
        if task.lower() in ['quit', 'exit', 'q']:
            break
        
        if task:
            print("Thinking...")
            response = agent.think(task)
            print(f"Response: {response}")


def main():
    """Main function"""
    print("🚀 OLLAMA AGENT QUICK START")
    print("=" * 50)
    
    choice = input("""
Choose mode:
1. Test without Ollama (shows fallback)
2. Run with Ollama (requires Ollama running)
3. Show setup instructions

Enter choice (1-3): """).strip()
    
    if choice == "1":
        test_without_ollama()
    elif choice == "2":
        run_with_ollama()
    elif choice == "3":
        print("""
🔧 OLLAMA SETUP:

1. Install Ollama:
   curl -fsSL https://ollama.ai/install.sh | sh

2. Start Ollama:
   ollama serve

3. Download model:
   ollama pull llama2:7b

4. Test connection:
   curl http://localhost:11434/api/tags

5. Run agent:
   python3 ollama_agent.py
        """)
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()