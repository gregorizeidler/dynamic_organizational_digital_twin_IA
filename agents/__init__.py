"""
Agents Package - Organizational Digital Twin Agents

This package contains all the specialized AI agents that form the core
of the organizational digital twin simulation.
"""

from .base_agent import BaseAgent
from .ceo_agent import CEOAgent
from .cfo_agent import CFOAgent
from .cto_agent import CTOAgent
from .cmo_agent import CMOAgent
from .hr_agent import HRAgent
from .coo_agent import COOAgent
from .cpo_agent import CPOAgent
from .clo_agent import CLOAgent
from .head_of_sales_agent import HeadOfSalesAgent
from .customer_success_agent import CustomerSuccessAgent
from .cdo_agent import CDOAgent

__all__ = [
    "BaseAgent",
    "CEOAgent", 
    "CFOAgent",
    "CTOAgent",
    "CMOAgent", 
    "HRAgent",
    "COOAgent",
    "CPOAgent",
    "CLOAgent",
    "HeadOfSalesAgent",
    "CustomerSuccessAgent",
    "CDOAgent"
]

# Agent Categories for Easy Organization
EXECUTIVE_AGENTS = [
    "CEOAgent",
    "CFOAgent", 
    "CTOAgent",
    "CMOAgent",
    "COOAgent",
    "CPOAgent",
    "CLOAgent",
    "CDOAgent"
]

SPECIALIZED_AGENTS = [
    "HRAgent",
    "HeadOfSalesAgent", 
    "CustomerSuccessAgent"
]

def get_all_agent_classes():
    """Return all available agent classes"""
    return {
        "CEO": CEOAgent,
        "CFO": CFOAgent,
        "CTO": CTOAgent,
        "CMO": CMOAgent,
        "HR": HRAgent,
        "COO": COOAgent,
        "CPO": CPOAgent,
        "CLO": CLOAgent,
        "Head of Sales": HeadOfSalesAgent,
        "Customer Success Manager": CustomerSuccessAgent,
        "CDO": CDOAgent
    }

def create_agent(agent_type: str, name: str = None):
    """Factory function to create agents by type"""
    agent_classes = get_all_agent_classes()
    
    if agent_type not in agent_classes:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    agent_class = agent_classes[agent_type]
    
    if name:
        return agent_class(name=name)
    else:
        return agent_class() 