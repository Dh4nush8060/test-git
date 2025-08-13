class SimpleAgent:
    """Simple, efficient AI agent for practical tasks"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory = []
        self.status = "ready"
    
    def think(self, task: str) -> str:
        """Process a task and return response"""
        self.memory.append(f"Task: {task}")
        
        # Simple decision logic
        if "buy" in task.lower():
            response = self._handle_buying(task)
        elif "sell" in task.lower():
            response = self._handle_selling(task)
        elif "negotiate" in task.lower():
            response = self._handle_negotiation(task)
        else:
            response = f"I'll work on: {task}"
        
        self.memory.append(f"Response: {response}")
        return response
    
    def _handle_buying(self, task: str) -> str:
        """Handle buying tasks"""
        return "Analyzing options, checking prices, ready to make offer"
    
    def _handle_selling(self, task: str) -> str:
        """Handle selling tasks"""
        return "Reviewing item value, setting competitive price"
    
    def _handle_negotiation(self, task: str) -> str:
        """Handle negotiation tasks"""
        return "Finding middle ground, preparing counter-offer"
    
    def get_status(self) -> dict:
        """Get current agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "tasks_completed": len([m for m in self.memory if "Response:" in m])
        }


# Quick usage examples
if __name__ == "__main__":
    # Create agent
    agent = SimpleAgent("Alex", "negotiator")
    
    # Test tasks
    tasks = [
        "Buy a laptop under $1000",
        "Sell my old car",
        "Negotiate better price for phone"
    ]
    
    print(f"Agent: {agent.name} ({agent.role})")
    print("-" * 40)
    
    for task in tasks:
        response = agent.think(task)
        print(f"Task: {task}")
        print(f"Response: {response}\n")
    
    print("Status:", agent.get_status())