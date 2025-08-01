import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration for the organizational digital twin"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")
    
    # Organization Configuration
    ORGANIZATION_NAME = os.getenv("ORGANIZATION_NAME", "TechCorp AI Startup")
    INITIAL_BUDGET = 1000000  # Initial budget in simulated USD
    
    # Simulation Configuration
    SIMULATION_SPEED = os.getenv("SIMULATION_SPEED", "normal")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Agent Configuration
    MAX_TOKENS_PER_RESPONSE = 1000
    TEMPERATURE = 0.7
    
    # Market Configuration
    MARKET_SIZE = 10000000  # Total simulated market size
    COMPETITORS_COUNT = 3   # Number of competitors in the market
    
    # Performance Metrics
    PERFORMANCE_METRICS = {
        "market_share": 0.0,
        "revenue": 0.0,
        "profit_margin": 0.0,
        "customer_satisfaction": 0.5,
        "innovation_index": 0.5,
        "employee_satisfaction": 0.5
    }
    
    # Time Configuration
    SIMULATION_CYCLE_DAYS = 30  # Each cycle represents 30 days
    
    @classmethod
    def validate(cls):
        """Validates that all necessary configurations are present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured. Set in .env or environment variable.")
        return True 