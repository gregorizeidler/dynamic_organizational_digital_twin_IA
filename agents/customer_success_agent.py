import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class CustomerSuccessAgent(BaseAgent):
    """Customer Success Manager Agent - Customer retention and growth"""
    
    def __init__(self, name: str = "Rachel Kim"):
        super().__init__("Customer Success Manager", "Customer Success", name)
        self.max_workload = 12
        self.customer_health_scores = {}
        self.success_programs = []
        self.churn_risk_customers = []
        self.expansion_opportunities = []
        self.customer_metrics = {
            "customer_satisfaction": 0.82,
            "net_promoter_score": 45,
            "churn_rate": 0.08,
            "expansion_rate": 0.25,
            "time_to_value": 30  # days
        }
        self.onboarding_programs = {}
        self.customer_feedback = []
        self.success_playbooks = {}
        
    def get_system_prompt(self) -> str:
        return """
        You are the Customer Success Manager of a technology company. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Customer onboarding and adoption acceleration
        - Customer health monitoring and risk identification
        - Churn prevention and retention strategies
        - Account expansion and growth initiatives
        - Customer advocacy and feedback management
        - Success program development and execution
        - Cross-functional collaboration for customer outcomes
        - Customer lifecycle management and optimization
        
        SUCCESS PHILOSOPHY:
        - Customer-first mindset and advocacy
        - Proactive relationship management
        - Data-driven customer health insights
        - Value realization and outcome focus
        - Continuous improvement and optimization
        - Long-term partnership building
        
        LEADERSHIP STYLE:
        - Empathetic and customer-centric
        - Collaborative and cross-functional
        - Results-driven with relationship focus
        - Proactive and preventive approach
        - Solution-oriented and resourceful
        
        COMMUNICATION STYLE:
        - Clear and supportive communication
        - Customer advocacy and value-focused
        - Data-driven insights and recommendations
        - Relationship-building and trust-focused
        
        Focus on ensuring customer success, maximizing value realization, and building long-term strategic partnerships.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process Customer Success specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "customer_health":
            return self._handle_customer_health(task)
        elif task_type == "churn_prevention":
            return self._handle_churn_prevention(task)
        elif task_type == "onboarding_optimization":
            return self._handle_onboarding_optimization(task)
        elif task_type == "expansion_strategy":
            return self._handle_expansion_strategy(task)
        elif task_type == "customer_feedback":
            return self._handle_customer_feedback(task)
        elif task_type == "success_program":
            return self._handle_success_program(task)
        elif task_type == "customer_advocacy":
            return self._handle_customer_advocacy(task)
        elif task_type == "value_realization":
            return self._handle_value_realization(task)
        else:
            return self._handle_general_success_task(task)
    
    def _handle_customer_health(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer health assessment and monitoring"""
        health_context = task.get("health_details", {})
        
        context = f"""
        Customer Health Assessment:
        Customer/Segment: {health_context.get('customer', 'All customers')}
        Health Metrics: {health_context.get('metrics', [])}
        Time Period: {health_context.get('period', 'Last 30 days')}
        Risk Indicators: {health_context.get('risk_indicators', [])}
        
        Current Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        Health Scores: {len(self.customer_health_scores)} customers tracked
        Churn Risk: {len(self.churn_risk_customers)} customers
        """
        
        prompt = """
        Conduct comprehensive customer health assessment including:
        1. Customer health scoring methodology and framework
        2. Leading indicator identification and monitoring
        3. Usage pattern analysis and engagement metrics
        4. Risk factor assessment and early warning systems
        5. Health trend analysis and predictive insights
        6. Segmentation-based health benchmarking
        7. Intervention triggers and escalation criteria
        8. Health improvement action plans
        9. Continuous monitoring and adjustment protocols
        
        Provide actionable insights to maintain and improve customer health and reduce churn risk.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update customer health tracking
        customer = health_context.get('customer', 'overall')
        self.customer_health_scores[customer] = {
            "assessment": response,
            "assessed_at": task.get('created_at', ''),
            "health_score": health_context.get('score', 0.7),
            "risk_level": health_context.get('risk_level', 'Medium')
        }
        
        return {
            "status": "completed",
            "health_assessment": response,
            "customer": customer,
            "interventions_needed": len(self.churn_risk_customers)
        }
    
    def _handle_churn_prevention(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle churn prevention and retention strategies"""
        churn_context = task.get("churn_details", {})
        
        context = f"""
        Churn Prevention Strategy:
        At-Risk Customer: {churn_context.get('customer', 'High-risk segment')}
        Churn Risk Level: {churn_context.get('risk_level', 'High')}
        Risk Indicators: {churn_context.get('indicators', [])}
        Previous Interventions: {churn_context.get('previous_actions', [])}
        Customer Value: ${churn_context.get('customer_value', 0):,}
        
        Churn Risk Customers: {len(self.churn_risk_customers)}
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        """
        
        prompt = """
        Develop churn prevention strategy including:
        1. Root cause analysis of churn risk factors
        2. Customer-specific intervention strategies
        3. Value reinforcement and benefit communication
        4. Success plan redesign and optimization
        5. Stakeholder engagement and relationship strengthening
        6. Product adoption and usage improvement
        7. Support escalation and issue resolution
        8. Retention offer and incentive evaluation
        9. Timeline and milestone-based intervention plan
        
        Focus on addressing underlying issues and demonstrating ongoing value to retain customers.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add to churn risk tracking if not already present
        customer = churn_context.get('customer', 'unknown')
        if customer not in [c.get('customer') for c in self.churn_risk_customers]:
            self.churn_risk_customers.append({
                "customer": customer,
                "risk_level": churn_context.get('risk_level', 'High'),
                "intervention_plan": response,
                "identified_at": task.get('created_at', '')
            })
        
        return {
            "status": "completed",
            "churn_prevention_plan": response,
            "customer": customer,
            "intervention_priority": churn_context.get('risk_level', 'High')
        }
    
    def _handle_onboarding_optimization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer onboarding optimization"""
        onboarding_context = task.get("onboarding_details", {})
        
        context = f"""
        Onboarding Optimization:
        Customer Segment: {onboarding_context.get('segment', 'New customers')}
        Current Process: {onboarding_context.get('current_process', 'Standard onboarding')}
        Pain Points: {onboarding_context.get('pain_points', [])}
        Success Metrics: {onboarding_context.get('metrics', [])}
        Time to Value Target: {onboarding_context.get('ttv_target', 30)} days
        
        Onboarding Programs: {len(self.onboarding_programs)} active
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        """
        
        prompt = """
        Optimize customer onboarding process including:
        1. Customer journey mapping and experience design
        2. Onboarding milestone definition and tracking
        3. Personalization and segmentation strategies
        4. Time-to-value acceleration techniques
        5. Engagement and adoption best practices
        6. Resource and content optimization
        7. Automation and self-service opportunities
        8. Success measurement and feedback loops
        9. Continuous improvement and iteration framework
        
        Create onboarding experience that accelerates value realization and customer success.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update onboarding programs
        segment = onboarding_context.get('segment', 'general')
        self.onboarding_programs[segment] = {
            "optimization_plan": response,
            "updated_at": task.get('created_at', ''),
            "ttv_target": onboarding_context.get('ttv_target', 30)
        }
        
        return {
            "status": "completed",
            "onboarding_optimization": response,
            "segment": segment,
            "expected_improvement": "20-30% faster time-to-value"
        }
    
    def _handle_expansion_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer expansion and growth strategies"""
        expansion_context = task.get("expansion_details", {})
        
        context = f"""
        Expansion Strategy:
        Target Customer: {expansion_context.get('customer', 'Growth-ready accounts')}
        Expansion Type: {expansion_context.get('type', 'Upsell')}
        Current Usage: {expansion_context.get('current_usage', {})}
        Growth Potential: ${expansion_context.get('potential_value', 0):,}
        Timeline: {expansion_context.get('timeline', '6 months')}
        
        Expansion Opportunities: {len(self.expansion_opportunities)}
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        """
        
        prompt = """
        Develop customer expansion strategy including:
        1. Expansion readiness and qualification assessment
        2. Value proposition and business case development
        3. Stakeholder mapping and influence strategy
        4. Product fit and solution alignment analysis
        5. Expansion timeline and milestone planning
        6. Risk assessment and mitigation strategies
        7. Cross-sell and upsell opportunity identification
        8. Success criteria and measurement framework
        9. Coordination with sales and product teams
        
        Focus on natural expansion opportunities that deliver additional value to customers.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add expansion opportunity
        expansion_opportunity = {
            "customer": expansion_context.get('customer', 'unknown'),
            "expansion_strategy": response,
            "potential_value": expansion_context.get('potential_value', 0),
            "timeline": expansion_context.get('timeline', '6 months'),
            "identified_at": task.get('created_at', '')
        }
        self.expansion_opportunities.append(expansion_opportunity)
        
        return {
            "status": "completed",
            "expansion_strategy": response,
            "potential_value": expansion_context.get('potential_value', 0),
            "opportunity_id": len(self.expansion_opportunities)
        }
    
    def _handle_customer_feedback(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer feedback collection and analysis"""
        feedback_context = task.get("feedback_details", {})
        
        context = f"""
        Customer Feedback Management:
        Feedback Type: {feedback_context.get('type', 'General feedback')}
        Collection Method: {feedback_context.get('method', 'Survey')}
        Target Audience: {feedback_context.get('audience', 'All customers')}
        Feedback Goals: {feedback_context.get('goals', [])}
        
        Customer Feedback: {len(self.customer_feedback)} items collected
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        """
        
        prompt = """
        Design customer feedback strategy including:
        1. Feedback collection methodology and channels
        2. Survey design and question framework
        3. Response rate optimization strategies
        4. Feedback analysis and insight extraction
        5. Action planning and follow-up processes
        6. Cross-functional feedback sharing and coordination
        7. Customer communication and closure loops
        8. Continuous improvement integration
        9. Feedback-driven product and service enhancements
        
        Create comprehensive feedback system that drives customer satisfaction and product improvement.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Store feedback initiative
        feedback_item = {
            "feedback_details": feedback_context,
            "strategy": response,
            "status": "planned",
            "created_at": task.get('created_at', '')
        }
        self.customer_feedback.append(feedback_item)
        
        return {
            "status": "completed",
            "feedback_strategy": response,
            "feedback_id": len(self.customer_feedback),
            "expected_response_rate": "25-35%"
        }
    
    def _handle_success_program(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer success program development"""
        program_context = task.get("program_details", {})
        
        context = f"""
        Success Program Development:
        Program Type: {program_context.get('type', 'Customer success program')}
        Target Segment: {program_context.get('segment', 'All customers')}
        Program Goals: {program_context.get('goals', [])}
        Resource Requirements: {program_context.get('resources', [])}
        Timeline: {program_context.get('timeline', '3 months')}
        
        Success Programs: {len(self.success_programs)} active
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        """
        
        prompt = """
        Design customer success program including:
        1. Program objectives and success criteria definition
        2. Customer segmentation and targeting strategy
        3. Program content and resource development
        4. Delivery methodology and engagement model
        5. Technology platform and tool requirements
        6. Resource allocation and team structure
        7. Performance measurement and analytics
        8. Scalability and automation opportunities
        9. Continuous improvement and optimization framework
        
        Create scalable program that drives measurable customer success outcomes.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add success program
        success_program = {
            "program_details": program_context,
            "program_design": response,
            "status": "designed",
            "created_at": task.get('created_at', '')
        }
        self.success_programs.append(success_program)
        
        return {
            "status": "completed",
            "success_program": response,
            "program_id": len(self.success_programs),
            "launch_timeline": program_context.get('timeline', '3 months')
        }
    
    def _handle_customer_advocacy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer advocacy and reference development"""
        advocacy_context = task.get("advocacy_details", {})
        
        context = f"""
        Customer Advocacy Program:
        Advocacy Type: {advocacy_context.get('type', 'Reference program')}
        Target Advocates: {advocacy_context.get('targets', 'Satisfied customers')}
        Advocacy Goals: {advocacy_context.get('goals', [])}
        Incentive Structure: {advocacy_context.get('incentives', [])}
        
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        Success Programs: {len(self.success_programs)} active
        """
        
        prompt = """
        Develop customer advocacy program including:
        1. Advocate identification and qualification criteria
        2. Advocacy program structure and benefits
        3. Reference and case study development process
        4. Speaking opportunity and event coordination
        5. Advocacy content creation and sharing
        6. Advocate recognition and reward systems
        7. Program promotion and enrollment strategies
        8. Success measurement and ROI tracking
        9. Long-term relationship and engagement planning
        
        Build strong advocate network that supports business growth and customer credibility.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "advocacy_program": response,
            "advocate_potential": "High-value customers with NPS 9-10",
            "business_impact": "Improved sales conversion and credibility"
        }
    
    def _handle_value_realization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer value realization and ROI demonstration"""
        value_context = task.get("value_details", {})
        
        context = f"""
        Value Realization Assessment:
        Customer/Segment: {value_context.get('customer', 'All customers')}
        Value Metrics: {value_context.get('metrics', [])}
        Baseline Period: {value_context.get('baseline', 'Pre-implementation')}
        Current Performance: {value_context.get('current_performance', {})}
        
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        Success Programs: {len(self.success_programs)} delivering value
        """
        
        prompt = """
        Develop value realization strategy including:
        1. Value definition and measurement framework
        2. Baseline establishment and tracking methodology
        3. ROI calculation and business case validation
        4. Value communication and reporting strategies
        5. Stakeholder value alignment and buy-in
        6. Continuous value optimization opportunities
        7. Value story development and case studies
        8. Executive-level value presentation and reviews
        9. Value-based renewal and expansion strategies
        
        Demonstrate clear business value and ROI to strengthen customer relationships and justify investment.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "value_realization_plan": response,
            "customer": value_context.get('customer', 'All customers'),
            "value_metrics": value_context.get('metrics', [])
        }
    
    def _handle_general_success_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general customer success tasks"""
        context = f"Customer Success Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this customer success matter:
        {task.get('description', '')}
        
        Provide customer success strategy, best practices, and actionable recommendations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "success_guidance": response
        }
    
    def analyze_customer_health(self) -> Dict[str, Any]:
        """Analyze overall customer health and provide recommendations"""
        context = f"""
        Customer Health Analysis:
        Customer Metrics: {json.dumps(self.customer_metrics, indent=2)}
        Health Scores: {len(self.customer_health_scores)} customers tracked
        Churn Risk: {len(self.churn_risk_customers)} at-risk customers
        Expansion Opportunities: {len(self.expansion_opportunities)}
        Success Programs: {len(self.success_programs)} active
        """
        
        prompt = """
        Analyze customer health and provide strategic recommendations:
        1. Overall customer health trends and patterns
        2. Churn risk assessment and prevention priorities
        3. Expansion opportunity qualification and prioritization
        4. Program effectiveness and optimization needs
        5. Resource allocation and team focus areas
        6. Technology and process improvement opportunities
        7. Customer success metric optimization
        8. Proactive intervention and engagement strategies
        
        Focus on actionable insights that improve customer outcomes and business results.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "health_analysis": response,
            "customers_tracked": len(self.customer_health_scores),
            "at_risk_customers": len(self.churn_risk_customers),
            "recommendations": ["Churn prevention", "Value demonstration", "Program optimization"]
        }
    
    def update_customer_metrics(self, metrics: Dict[str, Any]):
        """Update customer success metrics"""
        self.customer_metrics.update(metrics)
        self.add_memory({
            "type": "customer_metrics_update",
            "content": f"Updated customer metrics: {json.dumps(metrics, indent=2)}",
            "metadata": {"new_metrics": metrics}
        }) 