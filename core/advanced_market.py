import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class MarketPhase(Enum):
    GROWTH = "growth"
    RECESSION = "recession"
    RECOVERY = "recovery"
    BOOM = "boom"
    STAGNATION = "stagnation"

class CustomerSegment(Enum):
    ENTERPRISE = "enterprise"
    MID_MARKET = "mid_market"
    SMB = "smb"
    STARTUP = "startup"

@dataclass
class VirtualCustomer:
    """Represents a virtual customer with realistic behavior patterns"""
    id: str
    name: str
    segment: CustomerSegment
    industry: str
    size: int  # Number of employees
    budget: float
    satisfaction: float = 0.5
    loyalty: float = 0.3
    churn_probability: float = 0.1
    lifetime_value: float = 50000
    decision_speed: float = 0.5  # How quickly they make decisions
    price_sensitivity: float = 0.5
    feature_preferences: Dict[str, float] = None
    adoption_rate: float = 0.5
    support_tickets_per_month: int = 2
    expansion_potential: float = 0.3
    contract_length: int = 12  # months
    renewal_probability: float = 0.8
    
    def __post_init__(self):
        if self.feature_preferences is None:
            self.feature_preferences = {
                "security": random.uniform(0.3, 1.0),
                "scalability": random.uniform(0.2, 0.9),
                "usability": random.uniform(0.4, 1.0),
                "integration": random.uniform(0.3, 0.8),
                "performance": random.uniform(0.5, 1.0),
                "support": random.uniform(0.3, 0.9)
            }
    
    def react_to_product_changes(self, changes: Dict[str, Any]) -> Dict[str, float]:
        """React to product changes based on preferences"""
        reactions = {}
        
        for feature, impact in changes.items():
            if feature in self.feature_preferences:
                preference_weight = self.feature_preferences[feature]
                reaction = impact * preference_weight
                reactions[feature] = reaction
                
                # Update satisfaction based on reaction
                self.satisfaction = max(0, min(1, self.satisfaction + reaction * 0.1))
        
        return reactions
    
    def update_churn_probability(self, market_conditions: Dict[str, Any]):
        """Update churn probability based on various factors"""
        base_churn = 0.1
        
        # Satisfaction impact (most important)
        satisfaction_impact = (1 - self.satisfaction) * 0.3
        
        # Loyalty impact
        loyalty_impact = (1 - self.loyalty) * 0.2
        
        # Market conditions impact
        market_impact = 0
        if market_conditions.get('competitive_pressure', 0) > 0.7:
            market_impact += 0.1
        if market_conditions.get('economic_growth', 0) < 0.3:
            market_impact += 0.15
        
        # Price sensitivity impact
        if market_conditions.get('price_increase', 0) > 0:
            price_impact = self.price_sensitivity * market_conditions['price_increase'] * 0.2
        else:
            price_impact = 0
        
        self.churn_probability = min(0.8, base_churn + satisfaction_impact + loyalty_impact + market_impact + price_impact)
    
    def calculate_expansion_opportunity(self) -> Dict[str, Any]:
        """Calculate potential expansion opportunities"""
        if self.satisfaction < 0.6 or self.loyalty < 0.4:
            return {"potential": 0, "type": None, "value": 0}
        
        expansion_types = {
            "seat_expansion": self.size * 0.1 * self.expansion_potential,
            "feature_upgrade": self.budget * 0.2 * self.expansion_potential,
            "additional_products": self.lifetime_value * 0.3 * self.expansion_potential
        }
        
        best_opportunity = max(expansion_types.items(), key=lambda x: x[1])
        
        return {
            "potential": self.expansion_potential,
            "type": best_opportunity[0],
            "value": best_opportunity[1],
            "probability": min(0.8, self.satisfaction * self.loyalty)
        }

class EconomicCycleSimulator:
    """Simulates realistic economic cycles and market conditions"""
    
    def __init__(self):
        self.current_phase = MarketPhase.GROWTH
        self.phase_duration = 0
        self.interest_rates = 0.05
        self.inflation_rate = 0.03
        self.unemployment_rate = 0.04
        self.gdp_growth = 0.025
        self.market_volatility = 0.1
        self.tech_sector_performance = 0.8
        
    def advance_cycle(self):
        """Advance the economic cycle by one period"""
        self.phase_duration += 1
        
        # Phase transition logic
        if self.current_phase == MarketPhase.GROWTH and self.phase_duration > 24:
            if random.random() < 0.3:
                self.current_phase = MarketPhase.BOOM
                self.phase_duration = 0
        elif self.current_phase == MarketPhase.BOOM and self.phase_duration > 12:
            if random.random() < 0.4:
                self.current_phase = MarketPhase.RECESSION
                self.phase_duration = 0
        elif self.current_phase == MarketPhase.RECESSION and self.phase_duration > 18:
            if random.random() < 0.5:
                self.current_phase = MarketPhase.RECOVERY
                self.phase_duration = 0
        elif self.current_phase == MarketPhase.RECOVERY and self.phase_duration > 15:
            if random.random() < 0.6:
                self.current_phase = MarketPhase.GROWTH
                self.phase_duration = 0
        
        # Update economic indicators based on phase
        self._update_economic_indicators()
    
    def _update_economic_indicators(self):
        """Update economic indicators based on current phase"""
        if self.current_phase == MarketPhase.GROWTH:
            self.gdp_growth = random.uniform(0.02, 0.04)
            self.unemployment_rate = random.uniform(0.03, 0.06)
            self.interest_rates = random.uniform(0.02, 0.06)
            self.tech_sector_performance = random.uniform(0.7, 0.9)
            
        elif self.current_phase == MarketPhase.BOOM:
            self.gdp_growth = random.uniform(0.04, 0.07)
            self.unemployment_rate = random.uniform(0.02, 0.04)
            self.interest_rates = random.uniform(0.01, 0.04)
            self.tech_sector_performance = random.uniform(0.8, 1.0)
            
        elif self.current_phase == MarketPhase.RECESSION:
            self.gdp_growth = random.uniform(-0.03, 0.01)
            self.unemployment_rate = random.uniform(0.06, 0.12)
            self.interest_rates = random.uniform(0.00, 0.02)
            self.tech_sector_performance = random.uniform(0.3, 0.6)
            
        elif self.current_phase == MarketPhase.RECOVERY:
            self.gdp_growth = random.uniform(0.01, 0.03)
            self.unemployment_rate = random.uniform(0.05, 0.08)
            self.interest_rates = random.uniform(0.01, 0.03)
            self.tech_sector_performance = random.uniform(0.6, 0.8)
            
        elif self.current_phase == MarketPhase.STAGNATION:
            self.gdp_growth = random.uniform(-0.01, 0.01)
            self.unemployment_rate = random.uniform(0.05, 0.07)
            self.interest_rates = random.uniform(0.02, 0.04)
            self.tech_sector_performance = random.uniform(0.5, 0.7)
    
    def get_market_conditions(self) -> Dict[str, Any]:
        """Get current market conditions"""
        return {
            "phase": self.current_phase.value,
            "gdp_growth": self.gdp_growth,
            "unemployment_rate": self.unemployment_rate,
            "interest_rates": self.interest_rates,
            "inflation_rate": self.inflation_rate,
            "market_volatility": self.market_volatility,
            "tech_sector_performance": self.tech_sector_performance,
            "phase_duration": self.phase_duration
        }

class AdvancedMarketSimulator:
    """Advanced market simulator with virtual customers and economic cycles"""
    
    def __init__(self):
        self.virtual_customers: List[VirtualCustomer] = []
        self.economic_cycle = EconomicCycleSimulator()
        self.competitors = {}
        self.market_events = []
        self.total_market_size = 10000000  # $10M total addressable market
        self.market_growth_rate = 0.15
        self.competitive_landscape = {
            "market_leader": {"share": 0.35, "strength": 0.9},
            "challenger_1": {"share": 0.25, "strength": 0.8},
            "challenger_2": {"share": 0.20, "strength": 0.7},
            "our_company": {"share": 0.05, "strength": 0.6},
            "others": {"share": 0.15, "strength": 0.5}
        }
        
        # Initialize virtual customers
        self._generate_virtual_customers()
    
    def _generate_virtual_customers(self, count: int = 100):
        """Generate a diverse set of virtual customers"""
        industries = ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Education"]
        
        for i in range(count):
            segment = random.choice(list(CustomerSegment))
            industry = random.choice(industries)
            
            # Size and budget based on segment
            if segment == CustomerSegment.ENTERPRISE:
                size = random.randint(1000, 10000)
                budget = random.uniform(100000, 1000000)
            elif segment == CustomerSegment.MID_MARKET:
                size = random.randint(100, 1000)
                budget = random.uniform(25000, 200000)
            elif segment == CustomerSegment.SMB:
                size = random.randint(10, 100)
                budget = random.uniform(5000, 50000)
            else:  # STARTUP
                size = random.randint(5, 50)
                budget = random.uniform(1000, 25000)
            
            customer = VirtualCustomer(
                id=f"customer_{i:03d}",
                name=f"{industry} Corp {i:03d}",
                segment=segment,
                industry=industry,
                size=size,
                budget=budget,
                satisfaction=random.uniform(0.4, 0.8),
                loyalty=random.uniform(0.2, 0.7),
                churn_probability=random.uniform(0.05, 0.15),
                lifetime_value=budget * random.uniform(1.5, 3.0),
                decision_speed=random.uniform(0.2, 0.8),
                price_sensitivity=random.uniform(0.2, 0.8),
                adoption_rate=random.uniform(0.3, 0.9),
                expansion_potential=random.uniform(0.1, 0.6)
            )
            
            self.virtual_customers.append(customer)
    
    def simulate_market_dynamics(self) -> Dict[str, Any]:
        """Simulate one period of market dynamics"""
        # Advance economic cycle
        self.economic_cycle.advance_cycle()
        market_conditions = self.economic_cycle.get_market_conditions()
        
        # Update customer behaviors
        churned_customers = []
        expansion_opportunities = []
        
        for customer in self.virtual_customers:
            # Update churn probability
            customer.update_churn_probability(market_conditions)
            
            # Check for churn
            if random.random() < customer.churn_probability:
                churned_customers.append(customer)
            else:
                # Check for expansion opportunities
                expansion = customer.calculate_expansion_opportunity()
                if expansion["potential"] > 0.5:
                    expansion_opportunities.append({
                        "customer": customer,
                        "opportunity": expansion
                    })
        
        # Remove churned customers
        for customer in churned_customers:
            self.virtual_customers.remove(customer)
        
        # Generate market events
        market_events = self._generate_market_events(market_conditions)
        
        # Update competitive landscape
        self._update_competitive_landscape(market_conditions)
        
        return {
            "market_conditions": market_conditions,
            "customer_metrics": {
                "total_customers": len(self.virtual_customers),
                "churned_customers": len(churned_customers),
                "churn_rate": len(churned_customers) / max(1, len(self.virtual_customers) + len(churned_customers)),
                "expansion_opportunities": len(expansion_opportunities),
                "avg_satisfaction": np.mean([c.satisfaction for c in self.virtual_customers]),
                "avg_loyalty": np.mean([c.loyalty for c in self.virtual_customers])
            },
            "expansion_opportunities": expansion_opportunities,
            "market_events": market_events,
            "competitive_landscape": self.competitive_landscape,
            "market_size": self.total_market_size
        }
    
    def _generate_market_events(self, market_conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate realistic market events"""
        events = []
        
        # Economic events
        if market_conditions["gdp_growth"] < 0:
            events.append({
                "type": "economic",
                "event": "Economic downturn affecting customer budgets",
                "impact": "negative",
                "severity": abs(market_conditions["gdp_growth"]) * 10
            })
        
        if market_conditions["tech_sector_performance"] > 0.9:
            events.append({
                "type": "sector",
                "event": "Tech sector boom - increased investment",
                "impact": "positive",
                "severity": (market_conditions["tech_sector_performance"] - 0.5) * 2
            })
        
        # Competitive events
        if random.random() < 0.1:
            events.append({
                "type": "competitive",
                "event": "Major competitor launches new product",
                "impact": "negative",
                "severity": random.uniform(0.2, 0.7)
            })
        
        # Technology events
        if random.random() < 0.05:
            events.append({
                "type": "technology", 
                "event": "New technology disruption in market",
                "impact": "mixed",
                "severity": random.uniform(0.3, 0.8)
            })
        
        # Regulatory events
        if random.random() < 0.03:
            events.append({
                "type": "regulatory",
                "event": "New data privacy regulations announced",
                "impact": "negative",
                "severity": random.uniform(0.1, 0.5)
            })
        
        return events
    
    def _update_competitive_landscape(self, market_conditions: Dict[str, Any]):
        """Update competitive market shares based on conditions"""
        # Market growth affects all players
        growth_factor = 1 + market_conditions["gdp_growth"]
        
        # Update market shares with some randomness
        for competitor, data in self.competitive_landscape.items():
            # Add some randomness to market share changes
            change = random.uniform(-0.02, 0.02)
            
            # Economic conditions affect share changes
            if market_conditions["gdp_growth"] < 0:
                # In recession, stronger players gain share
                if data["strength"] > 0.7:
                    change += 0.01
                else:
                    change -= 0.01
            
            new_share = max(0.01, min(0.8, data["share"] + change))
            self.competitive_landscape[competitor]["share"] = new_share
        
        # Normalize shares to sum to 1.0
        total_share = sum(data["share"] for data in self.competitive_landscape.values())
        for competitor, data in self.competitive_landscape.items():
            self.competitive_landscape[competitor]["share"] = data["share"] / total_share
    
    def get_customer_segments_analysis(self) -> Dict[str, Any]:
        """Analyze customer segments"""
        segments = {}
        
        for segment in CustomerSegment:
            segment_customers = [c for c in self.virtual_customers if c.segment == segment]
            
            if segment_customers:
                segments[segment.value] = {
                    "count": len(segment_customers),
                    "avg_satisfaction": np.mean([c.satisfaction for c in segment_customers]),
                    "avg_loyalty": np.mean([c.loyalty for c in segment_customers]),
                    "avg_ltv": np.mean([c.lifetime_value for c in segment_customers]),
                    "churn_risk": np.mean([c.churn_probability for c in segment_customers]),
                    "expansion_potential": np.mean([c.expansion_potential for c in segment_customers])
                }
        
        return segments
    
    def simulate_campaign_impact(self, campaign_type: str, target_segment: str = None) -> Dict[str, Any]:
        """Simulate the impact of a marketing campaign"""
        impact_results = {
            "customers_affected": 0,
            "satisfaction_improvement": 0,
            "loyalty_improvement": 0,
            "acquisition_potential": 0
        }
        
        # Define campaign effects
        campaign_effects = {
            "brand_awareness": {"satisfaction": 0.05, "loyalty": 0.03, "acquisition": 0.1},
            "product_demo": {"satisfaction": 0.1, "loyalty": 0.05, "acquisition": 0.15},
            "customer_success": {"satisfaction": 0.15, "loyalty": 0.1, "acquisition": 0.05},
            "pricing_promotion": {"satisfaction": 0.08, "loyalty": 0.02, "acquisition": 0.2}
        }
        
        if campaign_type not in campaign_effects:
            return impact_results
        
        effects = campaign_effects[campaign_type]
        target_customers = self.virtual_customers
        
        # Filter by segment if specified
        if target_segment:
            target_customers = [c for c in self.virtual_customers 
                             if c.segment.value == target_segment]
        
        # Apply effects
        for customer in target_customers:
            customer.satisfaction = min(1.0, customer.satisfaction + effects["satisfaction"])
            customer.loyalty = min(1.0, customer.loyalty + effects["loyalty"])
            impact_results["customers_affected"] += 1
        
        impact_results["satisfaction_improvement"] = effects["satisfaction"]
        impact_results["loyalty_improvement"] = effects["loyalty"]
        impact_results["acquisition_potential"] = effects["acquisition"]
        
        return impact_results 