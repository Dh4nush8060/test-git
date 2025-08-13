#!/usr/bin/env python3
"""
Demo script showcasing different negotiation scenarios between buyer and seller agents
"""

from negotiator_agents import (
    AggressiveBuyerAgent, 
    AnalyticalBuyerAgent,
    FlexibleSellerAgent,
    FirmSellerAgent,
    NegotiationSession
)


def demo_aggressive_vs_flexible():
    """Demo: Aggressive buyer vs Flexible seller"""
    print("\n" + "="*80)
    print("DEMO 1: AGGRESSIVE BUYER vs FLEXIBLE SELLER")
    print("="*80)
    
    # Create agents
    buyer = AggressiveBuyerAgent(
        name="Mike 'The Hammer' Johnson", 
        budget=800, 
        target_discount=0.4
    )
    
    seller = FlexibleSellerAgent(
        name="Sarah 'Win-Win' Davis",
        asking_price=1000,
        minimum_price=700
    )
    
    # Item being negotiated
    item_info = {
        "name": "Vintage Guitar",
        "asking_price": 1000,
        "description": "1960s Fender Stratocaster in excellent condition"
    }
    
    # Start negotiation
    session = NegotiationSession(buyer, seller, item_info)
    result = session.start_negotiation()
    
    print(f"\n📊 RESULT: {result['status'].upper()} after {result['rounds']} rounds")
    if result['final_price']:
        print(f"💰 Final Price: ${result['final_price']:.2f}")


def demo_analytical_vs_firm():
    """Demo: Analytical buyer vs Firm seller"""
    print("\n" + "="*80)
    print("DEMO 2: ANALYTICAL BUYER vs FIRM SELLER")
    print("="*80)
    
    # Create agents
    buyer = AnalyticalBuyerAgent(
        name="Dr. Emma Analytics",
        budget=1200,
        market_research={
            "average_price": 950,
            "lowest_price": 800,
            "highest_price": 1100
        }
    )
    
    seller = FirmSellerAgent(
        name="Frank 'No Nonsense' Wilson",
        asking_price=1100,
        minimum_price=950
    )
    
    # Item being negotiated
    item_info = {
        "name": "Professional Camera",
        "asking_price": 1100,
        "description": "Canon EOS R5 with 24-70mm lens"
    }
    
    # Start negotiation
    session = NegotiationSession(buyer, seller, item_info)
    result = session.start_negotiation()
    
    print(f"\n📊 RESULT: {result['status'].upper()} after {result['rounds']} rounds")
    if result['final_price']:
        print(f"💰 Final Price: ${result['final_price']:.2f}")


def demo_personality_showcase():
    """Showcase different agent personalities"""
    print("\n" + "="*80)
    print("AGENT PERSONALITY SHOWCASE")
    print("="*80)
    
    # Create different agents
    agents = [
        AggressiveBuyerAgent("Aggressive Alex", 1000),
        AnalyticalBuyerAgent("Analytical Anna", 1000, {"average_price": 800}),
        FlexibleSellerAgent("Flexible Felix", 1000, 700),
        FirmSellerAgent("Firm Fiona", 1000, 800)
    ]
    
    print("\n🎭 AGENT PERSONALITIES:")
    print("-" * 50)
    
    for agent in agents:
        personality = agent.personality
        print(f"\n👤 {agent.name}")
        print(f"   Type: {personality['personality_type'].title()}")
        print(f"   Traits: {', '.join(personality['traits'])}")
        print(f"   Style: {personality['negotiation_style']}")
        print(f"   Catchphrases: {personality['catchphrases'][:2]}")  # Show first 2


def run_multiple_scenarios():
    """Run multiple negotiation scenarios"""
    print("\n" + "="*80)
    print("MULTIPLE SCENARIO COMPARISON")
    print("="*80)
    
    scenarios = [
        {
            "name": "Scenario A: Car Purchase",
            "buyer": AggressiveBuyerAgent("Tough Tony", 15000, 0.3),
            "seller": FlexibleSellerAgent("Friendly Frank", 18000, 14000),
            "item": {"name": "Used Toyota Camry", "asking_price": 18000}
        },
        {
            "name": "Scenario B: Laptop Deal",
            "buyer": AnalyticalBuyerAgent("Research Rachel", 1500, {"average_price": 1200}),
            "seller": FirmSellerAgent("Strict Steve", 1400, 1200),
            "item": {"name": "MacBook Pro", "asking_price": 1400}
        },
        {
            "name": "Scenario C: Antique Watch",
            "buyer": AggressiveBuyerAgent("Bargain Bob", 2000, 0.4),
            "seller": FirmSellerAgent("Premium Paul", 3000, 2500),
            "item": {"name": "Vintage Rolex", "asking_price": 3000}
        }
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"\n🎯 {scenario['name']}")
        print("-" * 40)
        
        session = NegotiationSession(
            scenario['buyer'], 
            scenario['seller'], 
            scenario['item']
        )
        
        result = session.start_negotiation()
        results.append({
            "scenario": scenario['name'],
            "result": result
        })
    
    # Summary
    print("\n" + "="*80)
    print("SCENARIO SUMMARY")
    print("="*80)
    
    for i, result_data in enumerate(results, 1):
        result = result_data['result']
        print(f"\n{i}. {result_data['scenario']}")
        print(f"   Status: {result['status'].title()}")
        print(f"   Rounds: {result['rounds']}")
        if result['final_price']:
            print(f"   Final Price: ${result['final_price']:.2f}")


if __name__ == "__main__":
    print("🤖 NEGOTIATION AGENTS DEMONSTRATION")
    print("=" * 80)
    
    # Run demos
    demo_personality_showcase()
    demo_aggressive_vs_flexible()
    demo_analytical_vs_firm()
    run_multiple_scenarios()
    
    print("\n" + "="*80)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("="*80)