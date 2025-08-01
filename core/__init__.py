"""
Core Systems Package - Organizational Digital Twin Core Components

This package contains the core systems that power the organizational digital twin,
including communication, memory, market simulation, and advanced intelligence features.
"""

from .communication_system import CommunicationSystem, OrganizationalMemory, NegotiationSystem
from .organizational_simulator import OrganizationalSimulator, MarketSimulator
from .advanced_market import AdvancedMarketSimulator, VirtualCustomer, EconomicCycleSimulator
from .agent_intelligence import (
    AgentPersonality, 
    AgentLearningSystem, 
    VectorMemorySystem, 
    PredictiveAnalytics
)

__all__ = [
    "CommunicationSystem",
    "OrganizationalMemory", 
    "NegotiationSystem",
    "OrganizationalSimulator",
    "MarketSimulator",
    "AdvancedMarketSimulator",
    "VirtualCustomer",
    "EconomicCycleSimulator",
    "AgentPersonality",
    "AgentLearningSystem",
    "VectorMemorySystem",
    "PredictiveAnalytics"
]

# Core system categories
COMMUNICATION_SYSTEMS = [
    "CommunicationSystem",
    "OrganizationalMemory",
    "NegotiationSystem"
]

SIMULATION_SYSTEMS = [
    "OrganizationalSimulator",
    "MarketSimulator", 
    "AdvancedMarketSimulator"
]

INTELLIGENCE_SYSTEMS = [
    "AgentPersonality",
    "AgentLearningSystem",
    "VectorMemorySystem",
    "PredictiveAnalytics"
]

MARKET_SYSTEMS = [
    "AdvancedMarketSimulator",
    "VirtualCustomer",
    "EconomicCycleSimulator"
] 