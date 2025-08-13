import json
import urllib.request
import urllib.parse


class OllamaAgent:
    """Simple AI agent using Ollama 7B local model"""
    
    def __init__(self, name: str, role: str, ollama_url: str = "http://localhost:11434"):
        self.name = name
        self.role = role
        self.ollama_url = ollama_url
        self.model = "llama2:7b"  # Default 7B model
        self.memory = []
        self.status = "ready"
    
    def think(self, task: str) -> str:
        """Process task using Ollama 7B model"""
        try:
            # Create prompt based on role
            prompt = self._create_prompt(task)
            
            # Get AI response from Ollama
            response = self._call_ollama(prompt)
            
            # Store in memory
            self.memory.append({"task": task, "response": response})
            
            return response
            
        except Exception as e:
            fallback = f"Error connecting to Ollama: {e}. Working on: {task}"
            self.memory.append({"task": task, "response": fallback})
            return fallback
    
    def _create_prompt(self, task: str) -> str:
        """Create role-specific prompt"""
        base_prompt = f"You are {self.name}, a {self.role}. "
        
        if "buy" in task.lower():
            prompt = base_prompt + f"Help with this buying task: {task}. Give a brief, practical response."
        elif "sell" in task.lower():
            prompt = base_prompt + f"Help with this selling task: {task}. Give a brief, practical response."
        elif "negotiate" in task.lower():
            prompt = base_prompt + f"Help with this negotiation: {task}. Give a brief, practical response."
        else:
            prompt = base_prompt + f"Help with this task: {task}. Give a brief, practical response."
        
        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
        url = f"{self.ollama_url}/api/generate"
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 150
            }
        }
        
        # Prepare request
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data)
        req.add_header('Content-Type', 'application/json')
        
        # Make request
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('response', 'No response from model').strip()
    
    def set_model(self, model_name: str):
        """Change Ollama model (e.g., 'llama2:7b', 'mistral:7b')"""
        self.model = model_name
        print(f"Switched to model: {model_name}")
    
    def get_status(self) -> dict:
        """Get agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "model": self.model,
            "ollama_url": self.ollama_url,
            "status": self.status,
            "tasks_completed": len(self.memory)
        }
    
    def get_memory(self) -> list:
        """Get conversation history"""
        return self.memory[-5:]  # Last 5 interactions


# Simple usage example
if __name__ == "__main__":
    # Create agent
    agent = OllamaAgent("Sam", "business_assistant")
    
    print(f"🤖 {agent.name} ({agent.role}) - Using {agent.model}")
    print("=" * 50)
    
    # Test tasks
    tasks = [
        "Buy a good laptop for programming under $1200",
        "Sell my 2020 Honda Civic, what price should I ask?",
        "Negotiate with supplier for bulk discount on office supplies"
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n{i}. Task: {task}")
        print("   Thinking...")
        
        response = agent.think(task)
        print(f"   Response: {response}")
    
    print(f"\n📊 Status: {agent.get_status()}")


# Quick setup instructions
def setup_instructions():
    """Print Ollama setup instructions"""
    print("""
    🚀 OLLAMA SETUP INSTRUCTIONS:
    
    1. Install Ollama:
       curl -fsSL https://ollama.ai/install.sh | sh
    
    2. Start Ollama service:
       ollama serve
    
    3. Pull 7B model:
       ollama pull llama2:7b
       # or
       ollama pull mistral:7b
    
    4. Run this agent:
       python3 ollama_agent.py
    
    Available models:
    - llama2:7b (default)
    - mistral:7b
    - codellama:7b
    """)


if __name__ == "__main__" and len(__import__('sys').argv) > 1:
    if __import__('sys').argv[1] == "--setup":
        setup_instructions()