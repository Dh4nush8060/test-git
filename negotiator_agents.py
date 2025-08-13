from abc import ABC, abstractmethod
from typing import Dict, Any, List
import random


class BaseBuyerAgent(ABC):
    """Base class for all buyer agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.personality = self.define_personality()
        self.budget = None
        self.target_price = None
        
    @abstractmethod
    def define_personality(self) -> Dict[str, Any]:
        """
        Define your agent's personality traits.
        
        Returns:
            Dict containing:
            - personality_type: str (e.g., "aggressive", "analytical", "diplomatic", "custom")
            - traits: List[str] (e.g., ["impatient", "data-driven", "friendly"])
            - negotiation_style: str (description of approach)
            - catchphrases: List[str] (typical phrases your agent uses)
        """
        pass
    
    @abstractmethod
    def make_offer(self, current_price: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Make an offer based on current price and item information"""
        pass
    
    @abstractmethod
    def respond_to_counteroffer(self, seller_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Respond to seller's counteroffer"""
        pass


class BaseSellerAgent(ABC):
    """Base class for all seller agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.personality = self.define_personality()
        self.minimum_price = None
        self.asking_price = None
        
    @abstractmethod
    def define_personality(self) -> Dict[str, Any]:
        """
        Define your agent's personality traits.
        
        Returns:
            Dict containing:
            - personality_type: str (e.g., "aggressive", "analytical", "diplomatic", "custom")
            - traits: List[str] (e.g., ["impatient", "data-driven", "friendly"])
            - negotiation_style: str (description of approach)
            - catchphrases: List[str] (typical phrases your agent uses)
        """
        pass
    
    @abstractmethod
    def respond_to_offer(self, buyer_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Respond to buyer's offer"""
        pass
    
    @abstractmethod
    def make_counteroffer(self, buyer_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Make a counteroffer to buyer's offer"""
        pass


class AggressiveBuyerAgent(BaseBuyerAgent):
    """Aggressive buyer agent that negotiates hard for lower prices"""
    
    def __init__(self, name: str, budget: float, target_discount: float = 0.3):
        super().__init__(name)
        self.budget = budget
        self.target_discount = target_discount
        self.offers_made = 0
        self.max_offers = 5
    
    def define_personality(self) -> Dict[str, Any]:
        return {
            "personality_type": "aggressive",
            "traits": ["impatient", "direct", "persistent", "cost-focused"],
            "negotiation_style": "Pushes hard for lower prices, makes bold initial offers, doesn't give up easily",
            "catchphrases": [
                "That's way too high!",
                "I can get this cheaper elsewhere",
                "My final offer is...",
                "Take it or leave it",
                "You're pricing yourself out of the market"
            ]
        }
    
    def make_offer(self, current_price: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Make an aggressive initial offer"""
        self.offers_made += 1
        
        if self.offers_made == 1:
            # Start with a very low offer
            offer_price = current_price * (1 - self.target_discount - 0.2)
        else:
            # Gradually increase but stay aggressive
            offer_price = current_price * (1 - self.target_discount + (self.offers_made * 0.05))
        
        offer_price = max(offer_price, self.budget * 0.5)  # Never go below 50% of budget
        
        catchphrase = random.choice(self.personality["catchphrases"])
        
        return {
            "offer_price": round(offer_price, 2),
            "message": f"{catchphrase}. I'll offer ${offer_price:.2f}",
            "agent_name": self.name,
            "offer_type": "initial_offer" if self.offers_made == 1 else "counteroffer"
        }
    
    def respond_to_counteroffer(self, seller_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Respond aggressively to seller's counteroffer"""
        if seller_offer <= self.budget:
            if seller_offer <= self.budget * 0.8:  # Good deal
                return {
                    "action": "accept",
                    "message": f"Fine, I'll take it for ${seller_offer:.2f}",
                    "agent_name": self.name
                }
            else:
                # Counter with slightly higher offer
                counter_offer = seller_offer * 0.9
                return {
                    "action": "counter",
                    "offer_price": round(counter_offer, 2),
                    "message": f"Still too high! How about ${counter_offer:.2f}?",
                    "agent_name": self.name
                }
        else:
            if self.offers_made >= self.max_offers:
                return {
                    "action": "walk_away",
                    "message": "This is ridiculous. I'm walking away!",
                    "agent_name": self.name
                }
            else:
                return self.make_offer(seller_offer, item_info)


class AnalyticalBuyerAgent(BaseBuyerAgent):
    """Analytical buyer agent that makes data-driven decisions"""
    
    def __init__(self, name: str, budget: float, market_research: Dict[str, float]):
        super().__init__(name)
        self.budget = budget
        self.market_research = market_research  # {"average_price": 100, "lowest_price": 80, "highest_price": 120}
        self.offers_made = 0
    
    def define_personality(self) -> Dict[str, Any]:
        return {
            "personality_type": "analytical",
            "traits": ["data-driven", "methodical", "patient", "research-oriented"],
            "negotiation_style": "Uses market data and analysis to justify offers, takes time to evaluate",
            "catchphrases": [
                "Based on my research...",
                "The market data shows...",
                "Let me analyze this offer",
                "According to comparable sales...",
                "The numbers don't add up"
            ]
        }
    
    def make_offer(self, current_price: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Make a data-driven offer based on market research"""
        self.offers_made += 1
        
        avg_price = self.market_research.get("average_price", current_price * 0.9)
        low_price = self.market_research.get("lowest_price", current_price * 0.8)
        
        # Start with offer slightly below market average
        if self.offers_made == 1:
            offer_price = min(avg_price * 0.95, self.budget)
        else:
            # Gradually increase based on market data
            offer_price = min(avg_price * (0.95 + self.offers_made * 0.02), self.budget)
        
        catchphrase = random.choice(self.personality["catchphrases"])
        
        return {
            "offer_price": round(offer_price, 2),
            "message": f"{catchphrase}, the fair market value is around ${avg_price:.2f}. I'll offer ${offer_price:.2f}",
            "agent_name": self.name,
            "offer_type": "initial_offer" if self.offers_made == 1 else "counteroffer"
        }
    
    def respond_to_counteroffer(self, seller_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Respond analytically to seller's counteroffer"""
        avg_price = self.market_research.get("average_price", seller_offer)
        
        if seller_offer <= avg_price and seller_offer <= self.budget:
            return {
                "action": "accept",
                "message": f"That's within market range. I accept ${seller_offer:.2f}",
                "agent_name": self.name
            }
        elif seller_offer <= self.budget * 1.1:  # Slightly over budget but reasonable
            counter_offer = min(avg_price, self.budget)
            return {
                "action": "counter",
                "offer_price": round(counter_offer, 2),
                "message": f"Market analysis suggests ${counter_offer:.2f} is more appropriate",
                "agent_name": self.name
            }
        else:
            return {
                "action": "walk_away",
                "message": "This price is too far above market value. I'll look elsewhere.",
                "agent_name": self.name
            }


class FlexibleSellerAgent(BaseSellerAgent):
    """Flexible seller agent that adapts to buyer behavior"""
    
    def __init__(self, name: str, asking_price: float, minimum_price: float):
        super().__init__(name)
        self.asking_price = asking_price
        self.minimum_price = minimum_price
        self.counteroffers_made = 0
        self.max_counteroffers = 4
    
    def define_personality(self) -> Dict[str, Any]:
        return {
            "personality_type": "diplomatic",
            "traits": ["flexible", "patient", "relationship-focused", "win-win oriented"],
            "negotiation_style": "Adapts to buyer's style, seeks mutually beneficial outcomes",
            "catchphrases": [
                "Let's find a middle ground",
                "I'm willing to work with you",
                "How about we meet halfway?",
                "I value our potential partnership",
                "Let's make this work for both of us"
            ]
        }
    
    def respond_to_offer(self, buyer_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Respond diplomatically to buyer's offer"""
        if buyer_offer >= self.minimum_price:
            if buyer_offer >= self.asking_price * 0.9:  # Close to asking price
                return {
                    "action": "accept",
                    "message": f"That's a fair offer. I accept ${buyer_offer:.2f}",
                    "agent_name": self.name
                }
            else:
                return self.make_counteroffer(buyer_offer, item_info)
        else:
            return self.make_counteroffer(buyer_offer, item_info)
    
    def make_counteroffer(self, buyer_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Make a flexible counteroffer"""
        self.counteroffers_made += 1
        
        if self.counteroffers_made >= self.max_counteroffers:
            # Final offer at minimum price
            counter_price = self.minimum_price
            message = f"My final offer is ${counter_price:.2f}. This is as low as I can go."
        else:
            # Meet somewhere in the middle
            gap = self.asking_price - buyer_offer
            reduction = gap * (0.3 + self.counteroffers_made * 0.2)
            counter_price = max(self.asking_price - reduction, self.minimum_price)
            
            catchphrase = random.choice(self.personality["catchphrases"])
            message = f"{catchphrase}. How about ${counter_price:.2f}?"
        
        return {
            "action": "counter",
            "offer_price": round(counter_price, 2),
            "message": message,
            "agent_name": self.name
        }


class FirmSellerAgent(BaseSellerAgent):
    """Firm seller agent that holds strong to their price"""
    
    def __init__(self, name: str, asking_price: float, minimum_price: float):
        super().__init__(name)
        self.asking_price = asking_price
        self.minimum_price = minimum_price
        self.counteroffers_made = 0
        self.max_counteroffers = 3
    
    def define_personality(self) -> Dict[str, Any]:
        return {
            "personality_type": "firm",
            "traits": ["confident", "direct", "value-focused", "no-nonsense"],
            "negotiation_style": "Maintains firm stance on pricing, minimal concessions",
            "catchphrases": [
                "This is a quality product",
                "The price reflects the value",
                "I know what it's worth",
                "Take it or leave it",
                "This is my best price"
            ]
        }
    
    def respond_to_offer(self, buyer_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Respond firmly to buyer's offer"""
        if buyer_offer >= self.asking_price * 0.95:  # Very close to asking price
            return {
                "action": "accept",
                "message": f"Alright, ${buyer_offer:.2f} it is.",
                "agent_name": self.name
            }
        elif buyer_offer >= self.minimum_price:
            return self.make_counteroffer(buyer_offer, item_info)
        else:
            return {
                "action": "reject",
                "message": f"That's far too low. My asking price is ${self.asking_price:.2f} for a reason.",
                "agent_name": self.name
            }
    
    def make_counteroffer(self, buyer_offer: float, item_info: Dict[str, Any]) -> Dict[str, Any]:
        """Make a firm counteroffer with minimal concessions"""
        self.counteroffers_made += 1
        
        if self.counteroffers_made >= self.max_counteroffers:
            return {
                "action": "final_offer",
                "offer_price": self.minimum_price,
                "message": f"Final offer: ${self.minimum_price:.2f}. This is non-negotiable.",
                "agent_name": self.name
            }
        else:
            # Small concession
            concession = (self.asking_price - self.minimum_price) * 0.2
            counter_price = max(self.asking_price - (concession * self.counteroffers_made), self.minimum_price)
            
            catchphrase = random.choice(self.personality["catchphrases"])
            
            return {
                "action": "counter",
                "offer_price": round(counter_price, 2),
                "message": f"{catchphrase}. I can do ${counter_price:.2f}",
                "agent_name": self.name
            }


class NegotiationSession:
    """Manages a negotiation session between buyer and seller agents"""
    
    def __init__(self, buyer_agent: BaseBuyerAgent, seller_agent: BaseSellerAgent, item_info: Dict[str, Any]):
        self.buyer = buyer_agent
        self.seller = seller_agent
        self.item_info = item_info
        self.negotiation_history = []
        self.max_rounds = 10
        self.current_round = 0
        self.status = "active"  # active, completed, failed
    
    def start_negotiation(self) -> Dict[str, Any]:
        """Start the negotiation process"""
        print(f"\n🤝 NEGOTIATION SESSION STARTED")
        print(f"Item: {self.item_info['name']}")
        print(f"Asking Price: ${self.item_info['asking_price']:.2f}")
        print(f"Buyer: {self.buyer.name} ({self.buyer.personality['personality_type']})")
        print(f"Seller: {self.seller.name} ({self.seller.personality['personality_type']})")
        print("="*60)
        
        # Buyer makes initial offer
        initial_offer = self.buyer.make_offer(self.item_info["asking_price"], self.item_info)
        self.negotiation_history.append({
            "round": self.current_round + 1,
            "agent": "buyer",
            "action": initial_offer
        })
        
        print(f"\n🛒 {self.buyer.name}: {initial_offer['message']}")
        
        return self.continue_negotiation(initial_offer)
    
    def continue_negotiation(self, last_action: Dict[str, Any]) -> Dict[str, Any]:
        """Continue the negotiation process"""
        while self.current_round < self.max_rounds and self.status == "active":
            self.current_round += 1
            
            if last_action.get("agent_name") == self.buyer.name:
                # Seller responds to buyer's offer
                if "offer_price" in last_action:
                    response = self.seller.respond_to_offer(last_action["offer_price"], self.item_info)
                else:
                    break
            else:
                # Buyer responds to seller's counteroffer
                if "offer_price" in last_action:
                    response = self.buyer.respond_to_counteroffer(last_action["offer_price"], self.item_info)
                else:
                    break
            
            self.negotiation_history.append({
                "round": self.current_round,
                "agent": "seller" if last_action.get("agent_name") == self.buyer.name else "buyer",
                "action": response
            })
            
            # Print response
            agent_name = self.seller.name if last_action.get("agent_name") == self.buyer.name else self.buyer.name
            emoji = "🏪" if agent_name == self.seller.name else "🛒"
            print(f"\n{emoji} {agent_name}: {response['message']}")
            
            # Check if negotiation ended
            if response["action"] in ["accept", "walk_away", "reject"]:
                if response["action"] == "accept":
                    self.status = "completed"
                    final_price = last_action.get("offer_price", response.get("offer_price"))
                    print(f"\n✅ DEAL CLOSED at ${final_price:.2f}!")
                else:
                    self.status = "failed"
                    print(f"\n❌ NEGOTIATION FAILED - {response['action']}")
                break
            
            last_action = response
        
        if self.current_round >= self.max_rounds and self.status == "active":
            self.status = "timeout"
            print(f"\n⏰ NEGOTIATION TIMEOUT after {self.max_rounds} rounds")
        
        return {
            "status": self.status,
            "rounds": self.current_round,
            "history": self.negotiation_history,
            "final_price": last_action.get("offer_price") if self.status == "completed" else None
        }