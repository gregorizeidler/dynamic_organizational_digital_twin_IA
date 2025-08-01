import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class CFOAgent(BaseAgent):
    """Chief Financial Officer Agent - Financial strategy and management"""
    
    def __init__(self, name: str = "Sarah Chen"):
        super().__init__("CFO", "Finance", name)
        self.max_workload = 12
        self.budget_allocations = {}
        self.financial_reports = []
        self.cash_flow = {
            "current_balance": 1000000,
            "monthly_burn_rate": 150000,
            "revenue": 0,
            "runway_months": 6.67
        }
        self.financial_projections = {}
        self.investment_tracking = []
        
    def get_system_prompt(self) -> str:
        return """
        You are the CFO of a growing tech startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Financial planning and analysis (FP&A)
        - Budget creation, monitoring, and control
        - Cash flow management and forecasting
        - Investment analysis and ROI evaluation
        - Financial reporting and compliance
        - Risk management and mitigation
        - Fundraising strategy and investor relations
        - Cost optimization and efficiency improvements
        
        FINANCIAL PHILOSOPHY:
        - Data-driven decision making
        - Conservative cash management with growth focus
        - ROI-oriented investment evaluation
        - Transparent financial reporting
        - Proactive risk identification
        
        COMMUNICATION STYLE:
        - Precise and analytical
        - Clear financial implications
        - Evidence-based recommendations
        - Risk-aware but opportunity-focused
        
        Always provide specific numbers, financial impact analysis, and actionable recommendations.
        Focus on sustainable growth while maintaining financial discipline.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process CFO-specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "budget_analysis":
            return self._handle_budget_analysis(task)
        elif task_type == "investment_evaluation":
            return self._handle_investment_evaluation(task)
        elif task_type == "financial_reporting":
            return self._handle_financial_reporting(task)
        elif task_type == "cash_flow_management":
            return self._handle_cash_flow_management(task)
        elif task_type == "cost_optimization":
            return self._handle_cost_optimization(task)
        elif task_type == "fundraising_strategy":
            return self._handle_fundraising_strategy(task)
        else:
            return self._handle_general_financial_task(task)
    
    def _handle_budget_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze budget requests and allocations"""
        budget_data = task.get("budget_data", {})
        
        context = f"""
        Budget Analysis Request:
        Department: {budget_data.get('department', 'All')}
        Period: {budget_data.get('period', 'Q1 2024')}
        Current Allocation: ${budget_data.get('current_allocation', 0):,}
        Requested Amount: ${budget_data.get('requested_amount', 0):,}
        Justification: {budget_data.get('justification', '')}
        
        Current Financial State:
        Cash Balance: ${self.cash_flow['current_balance']:,}
        Monthly Burn: ${self.cash_flow['monthly_burn_rate']:,}
        Runway: {self.cash_flow['runway_months']:.1f} months
        """
        
        prompt = """
        Conduct a comprehensive budget analysis including:
        1. Budget variance analysis (actual vs planned)
        2. ROI assessment for the requested budget
        3. Impact on cash flow and runway
        4. Alternative cost-effective solutions
        5. Recommendation (approve/deny/modify) with rationale
        
        Provide specific financial metrics and projections.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update budget allocations if approved
        department = budget_data.get('department', 'Unknown')
        if 'approve' in response.lower():
            self.budget_allocations[department] = budget_data.get('requested_amount', 0)
        
        return {
            "status": "completed",
            "analysis": response,
            "financial_impact": self._calculate_financial_impact(budget_data.get('requested_amount', 0))
        }
    
    def _handle_investment_evaluation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate investment opportunities"""
        investment = task.get("investment_details", {})
        
        context = f"""
        Investment Evaluation:
        Investment Type: {investment.get('type', 'Unknown')}
        Amount Required: ${investment.get('amount', 0):,}
        Expected Timeline: {investment.get('timeline', 'Not specified')}
        Projected ROI: {investment.get('projected_roi', 'Not specified')}
        Risk Level: {investment.get('risk_level', 'Medium')}
        Strategic Alignment: {investment.get('strategic_value', '')}
        """
        
        prompt = """
        Evaluate this investment opportunity with:
        1. Financial viability analysis (NPV, IRR, payback period)
        2. Risk assessment and mitigation strategies
        3. Cash flow impact analysis
        4. Strategic value assessment
        5. Competitive analysis
        6. Implementation timeline and milestones
        7. Final recommendation with confidence level
        
        Provide quantitative analysis with specific financial projections.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        self.investment_tracking.append({
            "investment": investment,
            "evaluation": response,
            "date": task.get('created_at', ''),
            "status": "evaluated"
        })
        
        return {
            "status": "completed",
            "investment_evaluation": response,
            "recommendation_confidence": 0.8
        }
    
    def _handle_financial_reporting(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financial reports"""
        report_type = task.get("report_type", "monthly")
        
        context = f"""
        Financial Report Generation:
        Report Type: {report_type}
        Period: {task.get('period', 'Current')}
        
        Current Financial Metrics:
        {json.dumps(self.cash_flow, indent=2)}
        
        Budget Allocations:
        {json.dumps(self.budget_allocations, indent=2)}
        """
        
        prompt = """
        Create a comprehensive financial report including:
        1. Executive Summary of financial position
        2. Revenue and expense breakdown
        3. Cash flow statement and analysis
        4. Budget vs actual performance
        5. Key financial ratios and metrics
        6. Variance analysis and explanations
        7. Forward-looking projections
        8. Recommendations and action items
        
        Format as a professional financial report with clear data presentation.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        report = {
            "type": report_type,
            "period": task.get('period', 'Current'),
            "content": response,
            "generated_at": task.get('created_at', ''),
            "metrics": self.cash_flow.copy()
        }
        
        self.financial_reports.append(report)
        
        return {
            "status": "completed",
            "financial_report": response,
            "distribution": ["CEO", "Board", "Executive Team"]
        }
    
    def _handle_cash_flow_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Manage cash flow and liquidity"""
        scenario = task.get("scenario", {})
        
        context = f"""
        Cash Flow Management:
        Current Balance: ${self.cash_flow['current_balance']:,}
        Monthly Burn Rate: ${self.cash_flow['monthly_burn_rate']:,}
        Revenue: ${self.cash_flow['revenue']:,}
        Runway: {self.cash_flow['runway_months']:.1f} months
        
        Scenario: {scenario.get('description', '')}
        Expected Impact: {scenario.get('impact', '')}
        """
        
        prompt = """
        Analyze cash flow situation and provide:
        1. Current liquidity assessment
        2. Cash flow projections (3, 6, 12 months)
        3. Scenario planning and stress testing
        4. Optimization recommendations
        5. Contingency planning
        6. Funding requirements and timing
        
        Focus on maintaining healthy cash position while supporting growth.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "cash_flow_analysis": response,
            "current_runway": self.cash_flow['runway_months'],
            "recommendations": ["Monitor weekly", "Optimize expenses", "Plan funding"]
        }
    
    def _handle_cost_optimization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Identify and implement cost optimization opportunities"""
        context = f"""
        Cost Optimization Analysis:
        Current Burn Rate: ${self.cash_flow['monthly_burn_rate']:,}
        Budget Allocations: {json.dumps(self.budget_allocations, indent=2)}
        Target Savings: {task.get('target_savings', '10%')}
        """
        
        prompt = """
        Identify cost optimization opportunities:
        1. Expense category analysis
        2. Cost reduction opportunities by department
        3. Efficiency improvement recommendations
        4. Vendor and contract optimization
        5. Technology cost savings
        6. Implementation timeline and savings projections
        7. Risk assessment of cost cuts
        
        Prioritize savings that don't impact core business functions.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "cost_optimization_plan": response,
            "projected_savings": task.get('target_savings', '10%')
        }
    
    def _handle_fundraising_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Develop fundraising strategy"""
        fundraising_details = task.get("fundraising_details", {})
        
        context = f"""
        Fundraising Strategy Development:
        Target Amount: ${fundraising_details.get('target_amount', 0):,}
        Use of Funds: {fundraising_details.get('use_of_funds', '')}
        Timeline: {fundraising_details.get('timeline', '')}
        Current Valuation: ${fundraising_details.get('current_valuation', 0):,}
        
        Financial Position:
        {json.dumps(self.cash_flow, indent=2)}
        """
        
        prompt = """
        Develop comprehensive fundraising strategy:
        1. Funding requirements analysis
        2. Use of funds breakdown
        3. Valuation methodology and justification
        4. Investor target profile and approach
        5. Financial projections and growth plan
        6. Risk factors and mitigation
        7. Timeline and milestones
        8. Terms and structure recommendations
        
        Create investor-ready financial narrative.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "fundraising_strategy": response,
            "investor_materials_needed": ["Pitch deck", "Financial model", "Due diligence folder"]
        }
    
    def _handle_general_financial_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general financial tasks"""
        context = f"Financial Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this financial matter:
        {task.get('description', '')}
        
        Provide financial analysis, recommendations, and next steps.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "financial_guidance": response
        }
    
    def approve_expense(self, expense: Dict[str, Any]) -> Dict[str, Any]:
        """Approve or deny expense requests"""
        context = f"""
        Expense Approval Request:
        Amount: ${expense.get('amount', 0):,}
        Category: {expense.get('category', 'Unknown')}
        Department: {expense.get('department', 'Unknown')}
        Justification: {expense.get('justification', '')}
        
        Budget Status: {json.dumps(self.budget_allocations, indent=2)}
        Cash Position: ${self.cash_flow['current_balance']:,}
        """
        
        prompt = """
        Evaluate this expense request considering:
        1. Budget availability and allocation
        2. Business necessity and ROI
        3. Cash flow impact
        4. Policy compliance
        5. Alternative options
        
        Provide APPROVE/DENY decision with detailed reasoning.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        decision = "REVIEW"
        if "APPROVE" in response.upper():
            decision = "APPROVED"
            # Update cash flow
            self.cash_flow['current_balance'] -= expense.get('amount', 0)
        elif "DENY" in response.upper():
            decision = "DENIED"
        
        return {
            "decision": decision,
            "reasoning": response,
            "remaining_budget": self.cash_flow['current_balance']
        }
    
    def _calculate_financial_impact(self, amount: float) -> Dict[str, Any]:
        """Calculate financial impact of spending"""
        new_balance = self.cash_flow['current_balance'] - amount
        new_runway = new_balance / self.cash_flow['monthly_burn_rate']
        
        return {
            "amount": amount,
            "new_balance": new_balance,
            "runway_impact": self.cash_flow['runway_months'] - new_runway,
            "percentage_of_budget": (amount / self.cash_flow['current_balance']) * 100
        }
    
    def update_financial_metrics(self, metrics: Dict[str, Any]):
        """Update financial metrics from external sources"""
        self.cash_flow.update(metrics)
        if 'current_balance' in metrics and 'monthly_burn_rate' in metrics:
            self.cash_flow['runway_months'] = metrics['current_balance'] / metrics['monthly_burn_rate'] 