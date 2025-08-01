import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class CEOAgent(BaseAgent):
    """Chief Executive Officer Agent - Strategic leadership and vision"""
    
    def __init__(self, name: str = "Alex Thompson"):
        super().__init__("CEO", "Executive", name)
        self.max_workload = 15  # CEOs handle more complex, strategic tasks
        self.strategic_vision = ""
        self.okrs = []  # Objectives and Key Results
        self.board_reports = []
        self.market_analysis = {}
        
    def get_system_prompt(self) -> str:
        return """
        You are the CEO of a dynamic tech startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Setting long-term strategic vision and direction
        - Making high-level executive decisions
        - Managing relationships with board, investors, and key stakeholders
        - Overseeing all departments and ensuring alignment
        - Resource allocation and budget approval
        - Crisis management and organizational adaptation
        - Market positioning and competitive strategy
        
        DECISION-MAKING STYLE:
        - Data-driven but decisive
        - Long-term focused while addressing immediate needs
        - Collaborative but willing to make tough calls
        - Risk-aware but not risk-averse
        - Innovation-oriented
        
        COMMUNICATION STYLE:
        - Clear, inspiring, and authoritative
        - Strategic thinking with practical implementation
        - Transparent about challenges and opportunities
        - Empowering to team members
        
        Always consider the broader organizational impact of decisions and maintain a balance between 
        growth ambitions and operational stability. Focus on creating sustainable competitive advantages.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process CEO-specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "strategic_planning":
            return self._handle_strategic_planning(task)
        elif task_type == "budget_approval":
            return self._handle_budget_approval(task)
        elif task_type == "crisis_management":
            return self._handle_crisis_management(task)
        elif task_type == "board_report":
            return self._handle_board_report(task)
        elif task_type == "vision_setting":
            return self._handle_vision_setting(task)
        else:
            return self._handle_general_executive_task(task)
    
    def _handle_strategic_planning(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle strategic planning tasks"""
        context = f"""
        Strategic Planning Task: {task.get('description', '')}
        Current Company State: {self._get_company_status()}
        Market Conditions: {self.market_analysis}
        """
        
        prompt = """
        Create a comprehensive strategic plan addressing the following:
        1. Current situation analysis (SWOT)
        2. Strategic objectives for next 12 months
        3. Key initiatives and resource requirements
        4. Success metrics and KPIs
        5. Risk assessment and mitigation strategies
        
        Format your response as a structured strategic plan.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "strategic_plan": response,
            "next_actions": ["Share with executive team", "Get department input", "Finalize and communicate"]
        }
    
    def _handle_budget_approval(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle budget approval decisions"""
        budget_request = task.get("budget_request", {})
        
        context = f"""
        Budget Approval Request:
        Department: {budget_request.get('department', 'Unknown')}
        Amount: ${budget_request.get('amount', 0):,}
        Purpose: {budget_request.get('purpose', '')}
        Justification: {budget_request.get('justification', '')}
        Expected ROI: {budget_request.get('expected_roi', 'Not specified')}
        """
        
        prompt = """
        Evaluate this budget request and make a decision. Consider:
        1. Strategic alignment with company goals
        2. Financial impact and ROI potential
        3. Current budget constraints
        4. Priority relative to other initiatives
        5. Risk factors
        
        Provide your decision (APPROVE/DENY/MODIFY) with detailed reasoning.
        If modifying, specify the approved amount and conditions.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Extract decision from response
        decision = "REVIEW" # Default
        if "APPROVE" in response.upper():
            decision = "APPROVED"
        elif "DENY" in response.upper():
            decision = "DENIED"
        elif "MODIFY" in response.upper():
            decision = "MODIFIED"
        
        return {
            "status": "completed",
            "decision": decision,
            "reasoning": response,
            "approved_amount": budget_request.get('amount', 0) if decision == "APPROVED" else 0
        }
    
    def _handle_crisis_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle crisis management situations"""
        crisis_details = task.get("crisis_details", {})
        
        context = f"""
        Crisis Situation:
        Type: {crisis_details.get('type', 'Unknown')}
        Severity: {crisis_details.get('severity', 'Medium')}
        Impact: {crisis_details.get('impact', '')}
        Timeline: {crisis_details.get('timeline', 'Immediate')}
        Stakeholders Affected: {crisis_details.get('stakeholders', [])}
        """
        
        prompt = """
        Develop a crisis management response plan including:
        1. Immediate actions to contain the situation
        2. Communication strategy (internal and external)
        3. Resource mobilization plan
        4. Recovery and business continuity measures
        5. Long-term prevention strategies
        
        Prioritize stakeholder safety, business continuity, and reputation management.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "crisis_response_plan": response,
            "immediate_actions": ["Assemble crisis team", "Implement containment measures", "Begin stakeholder communication"],
            "urgency": "HIGH"
        }
    
    def _handle_board_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate board reports"""
        context = f"""
        Board Report Period: {task.get('period', 'Q1 2024')}
        Company Performance: {self._get_company_status()}
        Key Achievements: {task.get('achievements', [])}
        Challenges: {task.get('challenges', [])}
        """
        
        prompt = """
        Create a comprehensive board report including:
        1. Executive Summary
        2. Financial Performance and Key Metrics
        3. Strategic Progress and Milestones
        4. Market Position and Competitive Analysis
        5. Operational Highlights
        6. Risk Assessment
        7. Forward-Looking Strategy
        8. Resource Requirements and Recommendations
        
        Make it data-driven, transparent, and strategic.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        self.board_reports.append({
            "period": task.get('period', 'Current'),
            "content": response,
            "created_at": task.get('created_at', '')
        })
        
        return {
            "status": "completed",
            "board_report": response,
            "distribution_list": ["Board Members", "Investors", "Executive Team"]
        }
    
    def _handle_vision_setting(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Set or update company vision and mission"""
        context = f"""
        Vision Setting Context:
        Current Vision: {self.strategic_vision}
        Market Changes: {task.get('market_changes', '')}
        Company Evolution: {task.get('company_changes', '')}
        Stakeholder Feedback: {task.get('feedback', '')}
        """
        
        prompt = """
        Develop or refine the company vision considering:
        1. Market opportunities and trends
        2. Company strengths and capabilities
        3. Stakeholder expectations
        4. Long-term sustainability
        5. Competitive differentiation
        
        Create a compelling, achievable vision that inspires and guides the organization.
        Include both vision statement and strategic pillars.
        """
        
        response = self.communicate_with_llm(prompt, context)
        self.strategic_vision = response
        
        return {
            "status": "completed",
            "updated_vision": response,
            "communication_plan": ["All-hands meeting", "Internal communications", "Website update"]
        }
    
    def _handle_general_executive_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general executive tasks"""
        context = f"Executive Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this executive matter with your CEO perspective:
        {task.get('description', '')}
        
        Provide strategic guidance, decisions, or actions as appropriate.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "executive_guidance": response
        }
    
    def set_okrs(self, objectives: List[Dict[str, Any]]):
        """Set Objectives and Key Results for the organization"""
        self.okrs = objectives
        self.add_memory({
            "type": "okr_setting",
            "content": f"Set {len(objectives)} OKRs for the organization",
            "metadata": {"okrs": objectives}
        })
    
    def evaluate_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate organizational performance against goals"""
        context = f"""
        Performance Metrics: {json.dumps(metrics, indent=2)}
        Current OKRs: {json.dumps(self.okrs, indent=2)}
        """
        
        prompt = """
        Analyze the current performance metrics against our OKRs and strategic goals.
        Provide:
        1. Performance assessment (achieving/underperforming/exceeding)
        2. Key insights and trends
        3. Areas requiring attention
        4. Strategic adjustments recommended
        5. Next quarter focus areas
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "performance_assessment": response,
            "recommended_actions": ["Review with exec team", "Adjust strategies as needed", "Communicate to organization"]
        }
    
    def _get_company_status(self) -> str:
        """Get current company status summary"""
        return f"""
        Role: {self.role}
        Active Tasks: {len(self.tasks)}
        Decisions Made: {self.performance_metrics['decisions_made']}
        Current Vision: {self.strategic_vision[:100]}...
        OKRs Count: {len(self.okrs)}
        """ 