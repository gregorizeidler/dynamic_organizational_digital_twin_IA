import json
import random
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from config import Config
from .communication_system import CommunicationSystem, OrganizationalMemory, NegotiationSystem
from .advanced_market import AdvancedMarketSimulator

# Import all agent types
from agents import (
    CEOAgent, CFOAgent, CTOAgent, CMOAgent, HRAgent,
    COOAgent, CPOAgent, CLOAgent, HeadOfSalesAgent,
    CustomerSuccessAgent, CDOAgent
)

class OrganizationalSimulator:
    """Enhanced organizational simulator with advanced AI agents and market dynamics"""
    
    def __init__(self):
        # Core simulation state
        self.simulation_day = 0
        self.is_running = False
        self.simulation_speed = Config.SIMULATION_SPEED
        
        # Advanced systems
        self.communication_system = CommunicationSystem()
        self.organizational_memory = OrganizationalMemory()
        self.negotiation_system = NegotiationSystem()
        self.market_simulator = AdvancedMarketSimulator()
        
        # Performance metrics
        self.performance_metrics = Config.PERFORMANCE_METRICS.copy()
        self.financial_metrics = {
            "revenue": 0,
            "expenses": 0,
            "profit": 0,
            "budget": Config.INITIAL_BUDGET,
            "monthly_burn_rate": 150000,
            "runway_months": 12
        }
        
        # Organization state
        self.organizational_health = {
            "morale": 0.75,
            "productivity": 0.70,
            "innovation_index": 0.65,
            "communication_quality": 0.80,
            "decision_velocity": 0.60,
            "market_responsiveness": 0.55
        }
        
        # Events and crises
        self.active_events = []
        self.event_history = []
        
        # Initialize all agents
        self.agents = self._initialize_agents()
        
        # Simulation history
        self.daily_snapshots = []
        
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all organizational agents with realistic team composition"""
        agents = {
            # C-Suite
            "CEO": CEOAgent("Sarah Johnson"),
            "CFO": CFOAgent("Marcus Chen"),
            "CTO": CTOAgent("Alex Rivera"),
            "CMO": CMOAgent("Jessica Williams"),
            "COO": COOAgent("Michael Chang"),
            "CPO": CPOAgent("Elena Rodriguez"),
            "CLO": CLOAgent("David Mitchell"),
            "CDO": CDOAgent("Dr. Priya Sharma"),
            
            # Department heads and specialists
            "HR": HRAgent("Lisa Park"),
            "Head_of_Sales": HeadOfSalesAgent("James Carter"),
            "Customer_Success": CustomerSuccessAgent("Rachel Kim")
        }
        
        # Register agents with communication system
        for role, agent in agents.items():
            self.communication_system.register_agent(agent.id, role)
        
        return agents
    
    def start_simulation(self):
        """Start the organizational simulation"""
        self.is_running = True
        self.organizational_memory.add_decision(
            decision="Simulation Started",
            context="Organizational Digital Twin simulation initiated",
            decision_maker="System",
            impact=0.5
        )
        
        # Initialize agents with startup context
        startup_context = {
            "company_stage": "Series A startup",
            "team_size": len(self.agents),
            "market_conditions": self.market_simulator.economic_cycle.get_market_conditions(),
            "initial_budget": self.financial_metrics["budget"]
        }
        
        for agent in self.agents.values():
            agent.add_memory({
                "content": f"Company started simulation. Stage: {startup_context['company_stage']}",
                "type": "company_milestone",
                "metadata": startup_context
            }, importance=0.8)
    
    def stop_simulation(self):
        """Stop the organizational simulation"""
        self.is_running = False
        self.organizational_memory.add_decision(
            decision="Simulation Stopped",
            context="Organizational Digital Twin simulation paused",
            decision_maker="System",
            impact=0.3
        )
    
    def advance_day(self) -> Dict[str, Any]:
        """Advance the simulation by one day with comprehensive updates"""
        if not self.is_running:
            return {"status": "simulation_not_running"}
        
        self.simulation_day += 1
        current_date = datetime.now() + timedelta(days=self.simulation_day)
        
        # Market dynamics update
        market_results = self.market_simulator.simulate_market_dynamics()
        
        # Daily agent activities
        agent_activities = self._process_daily_agent_activities(market_results)
        
        # Cross-agent collaborations
        collaborations = self._process_collaborations()
        
        # Handle pending negotiations
        negotiations = self._process_negotiations()
        
        # Update organizational metrics
        self._update_organizational_metrics(market_results, agent_activities)
        
        # Generate and handle events
        events = self._generate_daily_events(market_results)
        
        # Update financial metrics
        self._update_financial_metrics(market_results)
        
        # Capture daily snapshot
        daily_snapshot = self._capture_daily_snapshot(
            market_results, agent_activities, collaborations, negotiations, events
        )
        self.daily_snapshots.append(daily_snapshot)
        
        # Keep history manageable
        if len(self.daily_snapshots) > 365:  # Keep 1 year of daily data
            self.daily_snapshots = self.daily_snapshots[-365:]
        
        return daily_snapshot
    
    def _process_daily_agent_activities(self, market_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process daily activities for all agents"""
        activities = {}
        
        for role, agent in self.agents.items():
            # Update agent with market context
            market_context = market_results.get("market_conditions", {})
            agent.personality.adjust_for_workload(agent.current_workload / agent.max_workload)
            
            # Generate role-specific tasks based on market conditions and company needs
            daily_tasks = self._generate_daily_tasks_for_agent(role, market_context)
            
            # Process tasks
            completed_tasks = []
            for task in daily_tasks:
                if agent.assign_task(task):
                    result = agent.process_task(task)
                    completion = agent.complete_task(
                        task["id"], 
                        result.get("status") == "completed",
                        result.get("response", "")
                    )
                    completed_tasks.append(completion)
            
            activities[role] = {
                "agent_status": agent.get_status(),
                "daily_tasks": daily_tasks,
                "completed_tasks": completed_tasks,
                "personality_state": {
                    "mood": agent.personality.current_mood,
                    "confidence": agent.personality.confidence_level,
                    "stress": agent.personality.stress_level
                }
            }
        
        return activities
    
    def _generate_daily_tasks_for_agent(self, role: str, market_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate realistic daily tasks for each agent role"""
        tasks = []
        task_templates = {
            "CEO": [
                {"type": "strategic_review", "description": "Review company strategic priorities and market position"},
                {"type": "stakeholder_meeting", "description": "Meet with key stakeholders and investors"},
                {"type": "team_alignment", "description": "Ensure leadership team alignment on key decisions"}
            ],
            "CFO": [
                {"type": "financial_analysis", "description": "Analyze financial performance and budget allocation"},
                {"type": "cash_flow_management", "description": "Monitor cash flow and funding requirements"},
                {"type": "investor_relations", "description": "Prepare investor updates and financial reports"}
            ],
            "CTO": [
                {"type": "technical_planning", "description": "Review technical roadmap and development priorities"},
                {"type": "team_management", "description": "Support engineering team and remove blockers"},
                {"type": "architecture_review", "description": "Review system architecture and technical decisions"}
            ],
            "CMO": [
                {"type": "campaign_optimization", "description": "Optimize marketing campaigns and messaging"},
                {"type": "market_research", "description": "Analyze market trends and competitive landscape"},
                {"type": "brand_management", "description": "Manage brand positioning and customer perception"}
            ],
            "COO": [
                {"type": "operations_review", "description": "Review operational efficiency and process improvements"},
                {"type": "vendor_management", "description": "Manage vendor relationships and supply chain"},
                {"type": "quality_assurance", "description": "Ensure quality standards and operational excellence"}
            ],
            "CPO": [
                {"type": "product_strategy", "description": "Review product roadmap and feature prioritization"},
                {"type": "user_research", "description": "Analyze user feedback and market research"},
                {"type": "competitive_analysis", "description": "Monitor competitive landscape and positioning"}
            ],
            "CLO": [
                {"type": "legal_review", "description": "Review contracts and legal compliance matters"},
                {"type": "risk_assessment", "description": "Assess legal risks and compliance requirements"},
                {"type": "policy_development", "description": "Develop and update company policies"}
            ],
            "CDO": [
                {"type": "data_strategy", "description": "Review data strategy and analytics priorities"},
                {"type": "analytics_project", "description": "Oversee analytics projects and insights generation"},
                {"type": "data_governance", "description": "Ensure data quality and governance compliance"}
            ],
            "HR": [
                {"type": "talent_management", "description": "Review talent pipeline and employee development"},
                {"type": "culture_assessment", "description": "Assess company culture and employee satisfaction"},
                {"type": "performance_review", "description": "Conduct performance reviews and feedback sessions"}
            ],
            "Head_of_Sales": [
                {"type": "pipeline_review", "description": "Review sales pipeline and forecasting"},
                {"type": "team_performance", "description": "Analyze sales team performance and coaching needs"},
                {"type": "customer_meetings", "description": "Meet with key prospects and customers"}
            ],
            "Customer_Success": [
                {"type": "customer_health", "description": "Review customer health scores and satisfaction"},
                {"type": "churn_prevention", "description": "Identify and address at-risk customers"},
                {"type": "expansion_opportunities", "description": "Identify upsell and expansion opportunities"}
            ]
        }
        
        # Generate 1-3 tasks per day based on role and market conditions
        if role in task_templates:
            num_tasks = random.randint(1, 3)
            selected_tasks = random.sample(task_templates[role], min(num_tasks, len(task_templates[role])))
            
            for i, task_template in enumerate(selected_tasks):
                task = {
                    "id": f"{role}_{self.simulation_day}_{i}",
                    "type": task_template["type"],
                    "description": task_template["description"],
                    "complexity": random.randint(1, 3),
                    "importance": random.uniform(0.3, 0.9),
                    "risk_level": random.choice(["low", "medium", "high"]),
                    "created_at": datetime.now().isoformat(),
                    "market_context": market_context
                }
                tasks.append(task)
        
        return tasks
    
    def _process_collaborations(self) -> List[Dict[str, Any]]:
        """Process inter-agent collaborations"""
        collaborations = []
        
        # Define common collaboration patterns
        collaboration_patterns = [
            ("CEO", "CFO", "strategic_budget_review"),
            ("CEO", "CTO", "technology_strategy"),
            ("CMO", "Head_of_Sales", "go_to_market_alignment"),
            ("CPO", "CTO", "product_development"),
            ("HR", "CEO", "organizational_development"),
            ("CLO", "CFO", "compliance_and_risk"),
            ("CDO", "CPO", "data_driven_product_decisions"),
            ("Customer_Success", "Head_of_Sales", "customer_lifecycle_management"),
            ("COO", "CTO", "operational_efficiency")
        ]
        
        # Randomly trigger some collaborations
        for agent1_role, agent2_role, collaboration_type in collaboration_patterns:
            if random.random() < 0.3:  # 30% chance of collaboration per day
                collaboration_context = f"Daily collaboration on {collaboration_type}"
                
                agent1 = self.agents[agent1_role]
                agent2 = self.agents[agent2_role]
                
                result1 = agent1.collaborate(agent2_role, collaboration_context)
                result2 = agent2.collaborate(agent1_role, collaboration_context)
                
                collaboration = {
                    "participants": [agent1_role, agent2_role],
                    "type": collaboration_type,
                    "context": collaboration_context,
                    "results": [result1, result2],
                    "success": (result1["collaboration_quality"] + result2["collaboration_quality"]) / 2 > 0.6
                }
                
                collaborations.append(collaboration)
                
                # Add to organizational memory
                self.organizational_memory.add_lesson_learned(
                    lesson=f"Collaboration between {agent1_role} and {agent2_role} on {collaboration_type}",
                    context=collaboration_context,
                    effectiveness=(result1["collaboration_quality"] + result2["collaboration_quality"]) / 2
                )
        
        return collaborations
    
    def _process_negotiations(self) -> List[Dict[str, Any]]:
        """Process any pending negotiations between agents"""
        negotiations = []
        
        # Check for resource conflicts or decision disagreements
        if random.random() < 0.15:  # 15% chance of negotiation needed
            # Simulate a resource allocation negotiation
            participants = random.sample(list(self.agents.keys()), 2)
            
            negotiation_context = {
                "type": "resource_allocation",
                "participants": participants,
                "resource": random.choice(["budget", "engineering_time", "marketing_budget", "data_resources"]),
                "amount": random.randint(10000, 100000)
            }
            
            result = self.negotiation_system.mediate_negotiation(
                participants=participants,
                issue=negotiation_context["resource"],
                stakes=negotiation_context["amount"],
                agent_preferences={p: random.uniform(0.3, 0.9) for p in participants}
            )
            
            negotiations.append({
                "context": negotiation_context,
                "result": result,
                "resolved": result["success"]
            })
        
        return negotiations
    
    def _update_organizational_metrics(self, market_results: Dict[str, Any], agent_activities: Dict[str, Any]):
        """Update organizational health and performance metrics"""
        # Calculate organizational health based on agent states
        total_confidence = sum(activities["personality_state"]["confidence"] 
                             for activities in agent_activities.values())
        avg_confidence = total_confidence / len(agent_activities)
        
        total_stress = sum(activities["personality_state"]["stress"] 
                          for activities in agent_activities.values())
        avg_stress = total_stress / len(agent_activities)
        
        # Update organizational health
        self.organizational_health["morale"] = 0.7 * self.organizational_health["morale"] + 0.3 * avg_confidence
        self.organizational_health["productivity"] = 0.8 * self.organizational_health["productivity"] + 0.2 * (1 - avg_stress)
        
        # Update performance metrics based on market and agent performance
        customer_metrics = market_results.get("customer_metrics", {})
        if customer_metrics:
            self.performance_metrics["customer_satisfaction"] = customer_metrics.get("avg_satisfaction", 0.5)
            self.performance_metrics["market_share"] = min(0.1, self.performance_metrics["market_share"] + 0.001)
        
        # Innovation index based on agent innovation appetite
        innovation_scores = []
        for activities in agent_activities.values():
            agent_status = activities["agent_status"]
            if "personality" in agent_status:
                innovation_scores.append(agent_status["personality"].get("innovation_appetite", 0.5))
        
        if innovation_scores:
            self.organizational_health["innovation_index"] = sum(innovation_scores) / len(innovation_scores)
    
    def _update_financial_metrics(self, market_results: Dict[str, Any]):
        """Update financial metrics based on simulation results"""
        # Simulate daily revenue based on market performance
        market_conditions = market_results.get("market_conditions", {})
        daily_revenue = random.uniform(5000, 25000)  # Base daily revenue
        
        # Adjust based on market conditions
        if market_conditions.get("phase") == "recession":
            daily_revenue *= 0.7
        elif market_conditions.get("phase") == "boom":
            daily_revenue *= 1.3
        
        # Daily expenses
        daily_expenses = self.financial_metrics["monthly_burn_rate"] / 30
        
        # Update metrics
        self.financial_metrics["revenue"] += daily_revenue
        self.financial_metrics["expenses"] += daily_expenses
        self.financial_metrics["profit"] = self.financial_metrics["revenue"] - self.financial_metrics["expenses"]
        self.financial_metrics["budget"] = Config.INITIAL_BUDGET + self.financial_metrics["profit"]
        
        # Update runway
        if self.financial_metrics["monthly_burn_rate"] > 0:
            self.financial_metrics["runway_months"] = max(0, 
                self.financial_metrics["budget"] / self.financial_metrics["monthly_burn_rate"]
            )
    
    def _generate_daily_events(self, market_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate daily organizational events"""
        events = []
        
        # Market events from market simulator
        market_events = market_results.get("market_events", [])
        for event in market_events:
            events.append({
                "type": "market_event",
                "event": event,
                "impact": event.get("severity", 0.5),
                "source": "market"
            })
        
        # Internal organizational events
        if random.random() < 0.1:  # 10% chance of internal event
            internal_events = [
                {"type": "team_milestone", "description": "Team achieved important milestone", "impact": 0.3},
                {"type": "process_improvement", "description": "Process improvement implemented", "impact": 0.2},
                {"type": "new_partnership", "description": "New strategic partnership formed", "impact": 0.4},
                {"type": "technical_issue", "description": "Technical issue requiring attention", "impact": -0.2},
                {"type": "team_conflict", "description": "Team conflict needs resolution", "impact": -0.3}
            ]
            
            event = random.choice(internal_events)
            events.append({
                "type": "internal_event",
                "event": event,
                "impact": event["impact"],
                "source": "internal"
            })
        
        # Update active events
        self.active_events.extend(events)
        self.event_history.extend(events)
        
        # Keep history manageable
        if len(self.event_history) > 500:
            self.event_history = self.event_history[-500:]
        
        return events
    
    def _capture_daily_snapshot(self, market_results: Dict[str, Any], agent_activities: Dict[str, Any], 
                               collaborations: List[Dict[str, Any]], negotiations: List[Dict[str, Any]], 
                               events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Capture comprehensive daily snapshot"""
        return {
            "simulation_day": self.simulation_day,
            "timestamp": datetime.now().isoformat(),
            
            # Market state
            "market_results": market_results,
            
            # Agent states
            "agent_activities": agent_activities,
            "agent_summary": {
                role: activities["agent_status"] for role, activities in agent_activities.items()
            },
            
            # Organizational metrics
            "performance_metrics": self.performance_metrics.copy(),
            "financial_metrics": self.financial_metrics.copy(),
            "organizational_health": self.organizational_health.copy(),
            
            # Daily interactions
            "collaborations": collaborations,
            "negotiations": negotiations,
            "events": events,
            
            # System metrics
            "communication_stats": {
                "total_messages": len(self.communication_system.message_history),
                "active_negotiations": len(negotiations)
            }
        }
    
    def inject_crisis(self, crisis_type: str, severity: float = 0.7):
        """Inject a crisis scenario for testing organizational response"""
        crisis_scenarios = {
            "market_downturn": {
                "description": "Major market downturn affecting customer demand",
                "impact": {"revenue": -0.3, "morale": -0.2, "market_share": -0.1}
            },
            "competitor_threat": {
                "description": "Major competitor launches disruptive product",
                "impact": {"market_share": -0.2, "innovation_pressure": 0.3}
            },
            "key_talent_loss": {
                "description": "Key team members leaving the company",
                "impact": {"productivity": -0.3, "morale": -0.4}
            },
            "funding_challenge": {
                "description": "Difficulty raising next funding round",
                "impact": {"budget": -0.5, "runway": -0.3, "stress": 0.4}
            },
            "regulatory_change": {
                "description": "New regulations affecting business operations",
                "impact": {"compliance_cost": 0.2, "operational_complexity": 0.3}
            }
        }
        
        if crisis_type in crisis_scenarios:
            crisis = crisis_scenarios[crisis_type]
            
            # Apply crisis impacts
            for metric, impact in crisis["impact"].items():
                if metric in self.performance_metrics:
                    self.performance_metrics[metric] = max(0, min(1, 
                        self.performance_metrics[metric] + impact * severity
                    ))
                elif metric in self.organizational_health:
                    self.organizational_health[metric] = max(0, min(1,
                        self.organizational_health[metric] + impact * severity
                    ))
            
            # Notify all agents
            crisis_message = {
                "type": "crisis_alert",
                "content": crisis["description"],
                "severity": severity,
                "requires_response": True
            }
            
            for agent in self.agents.values():
                agent.add_memory({
                    "content": f"Crisis injected: {crisis['description']}",
                    "type": "crisis",
                    "metadata": {"severity": severity, "crisis_type": crisis_type}
                }, importance=0.9)
            
            # Record in organizational memory
            self.organizational_memory.add_decision(
                decision=f"Crisis Response: {crisis_type}",
                context=crisis["description"],
                decision_maker="Organization",
                impact=severity
            )
            
            return {"status": "crisis_injected", "crisis": crisis, "severity": severity}
        
        return {"status": "unknown_crisis_type", "available_types": list(crisis_scenarios.keys())}
    
    def get_simulation_state(self) -> Dict[str, Any]:
        """Get comprehensive simulation state"""
        return {
            "simulation_day": self.simulation_day,
            "is_running": self.is_running,
            "performance_metrics": self.performance_metrics,
            "financial_metrics": self.financial_metrics,
            "organizational_health": self.organizational_health,
            "agent_count": len(self.agents),
            "active_events": len(self.active_events),
            "total_memories": sum(len(agent.memory) for agent in self.agents.values()),
            "market_conditions": self.market_simulator.economic_cycle.get_market_conditions(),
            "recent_activity": self.daily_snapshots[-7:] if len(self.daily_snapshots) >= 7 else self.daily_snapshots
        }

# Legacy MarketSimulator for backward compatibility
class MarketSimulator:
    """Legacy market simulator - use AdvancedMarketSimulator for new features"""
    
    def __init__(self):
        self.advanced_simulator = AdvancedMarketSimulator()
        self.market_share = 0.05
        self.competitor_actions = []
        
    def simulate_day(self) -> Dict[str, Any]:
        """Simulate one day of market activity"""
        results = self.advanced_simulator.simulate_market_dynamics()
        
        # Extract legacy format data
        market_conditions = results.get("market_conditions", {})
        customer_metrics = results.get("customer_metrics", {})
        
        return {
            "market_growth": market_conditions.get("gdp_growth", 0.02),
            "competitive_pressure": random.uniform(0.3, 0.8),
            "customer_acquisition": customer_metrics.get("total_customers", 0),
            "market_events": results.get("market_events", []),
            "market_share": self.market_share,
            "revenue_impact": random.uniform(-0.1, 0.1)
        } 