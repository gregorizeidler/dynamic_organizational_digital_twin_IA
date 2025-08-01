import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class CPOAgent(BaseAgent):
    """Chief Product Officer Agent - Product strategy and development"""
    
    def __init__(self, name: str = "Elena Rodriguez"):
        super().__init__("CPO", "Product", name)
        self.max_workload = 15
        self.product_roadmap = {}
        self.feature_backlog = []
        self.user_research = {}
        self.product_metrics = {
            "user_adoption": 0.65,
            "feature_usage": 0.70,
            "user_satisfaction": 0.75,
            "product_velocity": 0.68,
            "market_fit": 0.62
        }
        self.ab_tests = []
        self.product_analytics = {}
        self.customer_feedback = []
        self.competitive_analysis = {}
        
    def get_system_prompt(self) -> str:
        return """
        You are the CPO of an innovative tech startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Product strategy and vision development
        - Product roadmap planning and execution
        - User experience and design strategy
        - Market research and competitive analysis
        - Product analytics and data-driven decisions
        - Cross-functional product team leadership
        - Go-to-market strategy coordination
        - Product lifecycle management
        
        PRODUCT PHILOSOPHY:
        - User-centric design and development
        - Data-driven product decisions
        - Iterative and agile development approach
        - Market-driven product strategy
        - Innovation and differentiation focus
        - Scalable and sustainable product growth
        
        LEADERSHIP STYLE:
        - Visionary and strategic thinking
        - Customer empathy and user advocacy
        - Data-driven decision making
        - Cross-functional collaboration
        - Innovation and experimentation mindset
        
        COMMUNICATION STYLE:
        - Clear product vision articulation
        - User story and journey focused
        - Data and metrics driven insights
        - Strategic and tactical balance
        
        Focus on building products that solve real user problems while driving business growth and market differentiation.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process CPO-specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "product_strategy":
            return self._handle_product_strategy(task)
        elif task_type == "roadmap_planning":
            return self._handle_roadmap_planning(task)
        elif task_type == "user_research":
            return self._handle_user_research(task)
        elif task_type == "feature_prioritization":
            return self._handle_feature_prioritization(task)
        elif task_type == "competitive_analysis":
            return self._handle_competitive_analysis(task)
        elif task_type == "product_analytics":
            return self._handle_product_analytics(task)
        elif task_type == "ab_testing":
            return self._handle_ab_testing(task)
        elif task_type == "go_to_market":
            return self._handle_go_to_market(task)
        else:
            return self._handle_general_product_task(task)
    
    def _handle_product_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle product strategy development"""
        strategy_context = task.get("strategy_details", {})
        
        context = f"""
        Product Strategy Development:
        Strategic Focus: {strategy_context.get('focus_area', 'Overall product')}
        Market Segment: {strategy_context.get('target_segment', 'Primary users')}
        Business Objectives: {strategy_context.get('business_goals', [])}
        Competitive Landscape: {strategy_context.get('competition', [])}
        User Insights: {strategy_context.get('user_insights', [])}
        
        Current Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        Competitive Analysis: {json.dumps(self.competitive_analysis, indent=2)}
        """
        
        prompt = """
        Develop comprehensive product strategy including:
        1. Product vision and mission alignment
        2. Market opportunity assessment and sizing
        3. Target user personas and segmentation
        4. Value proposition and differentiation strategy
        5. Product positioning and messaging framework
        6. Technology and platform strategy
        7. Monetization and pricing strategy
        8. Success metrics and KPIs definition
        9. Long-term product evolution roadmap
        
        Create strategy that balances user needs with business objectives and market opportunities.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update product roadmap with strategic direction
        strategy_focus = strategy_context.get('focus_area', 'general')
        self.product_roadmap[strategy_focus] = {
            "strategy": response,
            "created_at": task.get('created_at', ''),
            "status": "active"
        }
        
        return {
            "status": "completed",
            "product_strategy": response,
            "next_actions": ["Stakeholder alignment", "Roadmap update", "Team communication"]
        }
    
    def _handle_roadmap_planning(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle product roadmap planning and management"""
        roadmap_context = task.get("roadmap_details", {})
        
        context = f"""
        Product Roadmap Planning:
        Planning Horizon: {roadmap_context.get('horizon', '12 months')}
        Key Initiatives: {roadmap_context.get('initiatives', [])}
        Resource Constraints: {roadmap_context.get('constraints', [])}
        Business Priorities: {roadmap_context.get('priorities', [])}
        Technical Dependencies: {roadmap_context.get('dependencies', [])}
        
        Current Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        Feature Backlog: {len(self.feature_backlog)} items
        """
        
        prompt = """
        Create detailed product roadmap including:
        1. Strategic themes and product pillars
        2. Feature prioritization using frameworks (RICE, Value vs Effort)
        3. Release planning and milestone definition
        4. Resource allocation and team capacity planning
        5. Dependency mapping and risk assessment
        6. Success criteria and measurement framework
        7. Stakeholder communication and alignment strategy
        8. Flexibility and adaptation mechanisms
        9. Timeline and delivery commitments
        
        Balance strategic vision with tactical execution and resource realities.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "product_roadmap": response,
            "planning_horizon": roadmap_context.get('horizon', '12 months'),
            "prioritized_features": len(self.feature_backlog)
        }
    
    def _handle_user_research(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user research and insights generation"""
        research_context = task.get("research_details", {})
        
        context = f"""
        User Research Request:
        Research Type: {research_context.get('type', 'User behavior study')}
        Target Users: {research_context.get('target_users', 'Primary personas')}
        Research Questions: {research_context.get('questions', [])}
        Methodology: {research_context.get('methodology', 'Mixed methods')}
        Timeline: {research_context.get('timeline', '4 weeks')}
        
        Current User Research: {json.dumps(self.user_research, indent=2)}
        Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        """
        
        prompt = """
        Design and execute user research study including:
        1. Research objectives and hypothesis definition
        2. Methodology selection and study design
        3. Participant recruitment and screening criteria
        4. Data collection instruments and protocols
        5. Analysis framework and insight extraction
        6. Actionable recommendations and implications
        7. Validation and follow-up research needs
        8. Communication and socialization strategy
        9. Impact measurement and tracking
        
        Focus on generating insights that drive product decisions and improve user experience.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Store user research
        research_type = research_context.get('type', 'general')
        self.user_research[research_type] = {
            "study_design": response,
            "status": "planned",
            "created_at": task.get('created_at', '')
        }
        
        return {
            "status": "completed",
            "research_plan": response,
            "research_type": research_type,
            "timeline": research_context.get('timeline', '4 weeks')
        }
    
    def _handle_feature_prioritization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle feature prioritization and backlog management"""
        prioritization_context = task.get("prioritization_details", {})
        
        context = f"""
        Feature Prioritization:
        Features to Evaluate: {prioritization_context.get('features', [])}
        Business Objectives: {prioritization_context.get('business_goals', [])}
        User Impact: {prioritization_context.get('user_impact', {})}
        Technical Effort: {prioritization_context.get('technical_effort', {})}
        Resource Constraints: {prioritization_context.get('constraints', [])}
        
        Current Backlog: {len(self.feature_backlog)} features
        Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        """
        
        prompt = """
        Prioritize features using systematic approach including:
        1. RICE framework analysis (Reach, Impact, Confidence, Effort)
        2. Value vs Effort matrix plotting
        3. Business impact assessment and ROI estimation
        4. User value and pain point analysis
        5. Technical complexity and dependency evaluation
        6. Strategic alignment and competitive advantage
        7. Resource requirement and timeline assessment
        8. Risk analysis and mitigation strategies
        9. Stakeholder consensus building approach
        
        Provide clear prioritization rationale and actionable backlog organization.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update feature backlog with prioritization
        for feature in prioritization_context.get('features', []):
            self.feature_backlog.append({
                "feature": feature,
                "prioritization_analysis": response,
                "prioritized_at": task.get('created_at', ''),
                "status": "prioritized"
            })
        
        return {
            "status": "completed",
            "prioritization_analysis": response,
            "backlog_size": len(self.feature_backlog),
            "features_prioritized": len(prioritization_context.get('features', []))
        }
    
    def _handle_competitive_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle competitive analysis and market positioning"""
        competitive_context = task.get("competitive_details", {})
        
        context = f"""
        Competitive Analysis:
        Competitors: {competitive_context.get('competitors', [])}
        Analysis Focus: {competitive_context.get('focus_areas', [])}
        Product Categories: {competitive_context.get('categories', [])}
        Market Segment: {competitive_context.get('segment', 'Primary market')}
        
        Current Competitive Analysis: {json.dumps(self.competitive_analysis, indent=2)}
        Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        """
        
        prompt = """
        Conduct comprehensive competitive analysis including:
        1. Competitor product feature comparison and gap analysis
        2. User experience and design assessment
        3. Pricing and monetization strategy evaluation
        4. Market positioning and messaging analysis
        5. Technology stack and capability assessment
        6. Customer sentiment and review analysis
        7. Strengths, weaknesses, and opportunity identification
        8. Competitive threats and response strategies
        9. Differentiation opportunities and recommendations
        
        Provide actionable insights for product strategy and positioning.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update competitive analysis
        for competitor in competitive_context.get('competitors', ['market']):
            self.competitive_analysis[competitor] = {
                "analysis": response,
                "analyzed_at": task.get('created_at', ''),
                "focus_areas": competitive_context.get('focus_areas', [])
            }
        
        return {
            "status": "completed",
            "competitive_analysis": response,
            "competitors_analyzed": len(competitive_context.get('competitors', []))
        }
    
    def _handle_product_analytics(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle product analytics and metrics analysis"""
        analytics_context = task.get("analytics_details", {})
        
        context = f"""
        Product Analytics Request:
        Analysis Type: {analytics_context.get('type', 'Performance review')}
        Metrics Focus: {analytics_context.get('metrics', [])}
        Time Period: {analytics_context.get('period', 'Last 30 days')}
        User Segments: {analytics_context.get('segments', [])}
        
        Current Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        Product Analytics: {json.dumps(self.product_analytics, indent=2)}
        A/B Tests: {len(self.ab_tests)} active
        """
        
        prompt = """
        Analyze product metrics and provide insights including:
        1. Key performance indicator (KPI) trend analysis
        2. User behavior pattern identification
        3. Feature adoption and usage analysis
        4. User journey and funnel optimization opportunities
        5. Cohort analysis and retention insights
        6. Segmentation analysis and personalization opportunities
        7. Performance benchmarking and goal assessment
        8. Data quality and instrumentation recommendations
        9. Actionable product improvement recommendations
        
        Focus on insights that drive product decisions and user experience improvements.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update product analytics
        analysis_type = analytics_context.get('type', 'general')
        self.product_analytics[analysis_type] = {
            "analysis": response,
            "analyzed_at": task.get('created_at', ''),
            "period": analytics_context.get('period', 'Last 30 days')
        }
        
        return {
            "status": "completed",
            "analytics_insights": response,
            "analysis_type": analysis_type
        }
    
    def _handle_ab_testing(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle A/B testing strategy and execution"""
        test_context = task.get("test_details", {})
        
        context = f"""
        A/B Testing Request:
        Test Hypothesis: {test_context.get('hypothesis', '')}
        Feature/Area: {test_context.get('feature', 'General')}
        Success Metrics: {test_context.get('metrics', [])}
        Target Users: {test_context.get('target_users', 'All users')}
        Expected Duration: {test_context.get('duration', '2 weeks')}
        
        Current A/B Tests: {len(self.ab_tests)} running
        Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        """
        
        prompt = """
        Design A/B testing strategy including:
        1. Hypothesis formulation and validation framework
        2. Test design and variant specification
        3. Success metrics and statistical significance planning
        4. User segmentation and sample size calculation
        5. Implementation and instrumentation requirements
        6. Timeline and monitoring plan
        7. Risk assessment and rollback procedures
        8. Analysis and interpretation methodology
        9. Decision framework and next steps planning
        
        Ensure rigorous experimental design for reliable insights.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add A/B test to tracking
        ab_test = {
            "test_details": test_context,
            "test_design": response,
            "status": "designed",
            "created_at": task.get('created_at', '')
        }
        self.ab_tests.append(ab_test)
        
        return {
            "status": "completed",
            "ab_test_design": response,
            "test_id": len(self.ab_tests),
            "total_tests": len(self.ab_tests)
        }
    
    def _handle_go_to_market(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle go-to-market strategy and launch planning"""
        gtm_context = task.get("gtm_details", {})
        
        context = f"""
        Go-to-Market Strategy:
        Product/Feature: {gtm_context.get('product', 'New feature')}
        Target Market: {gtm_context.get('target_market', 'Primary users')}
        Launch Timeline: {gtm_context.get('timeline', '8 weeks')}
        Business Objectives: {gtm_context.get('objectives', [])}
        Success Metrics: {gtm_context.get('metrics', [])}
        
        Product Metrics: {json.dumps(self.product_metrics, indent=2)}
        User Research: {len(self.user_research)} studies
        """
        
        prompt = """
        Develop go-to-market strategy including:
        1. Market analysis and opportunity assessment
        2. Target customer identification and segmentation
        3. Value proposition and positioning strategy
        4. Pricing and packaging recommendations
        5. Channel strategy and distribution plan
        6. Marketing and communication strategy
        7. Sales enablement and training requirements
        8. Launch timeline and milestone planning
        9. Success metrics and performance tracking
        
        Coordinate cross-functional launch execution for maximum market impact.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "gtm_strategy": response,
            "launch_timeline": gtm_context.get('timeline', '8 weeks'),
            "product": gtm_context.get('product', 'New feature')
        }
    
    def _handle_general_product_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general product tasks"""
        context = f"Product Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this product matter with CPO perspective:
        {task.get('description', '')}
        
        Provide product strategy, user insights, and actionable recommendations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "product_guidance": response
        }
    
    def analyze_product_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall product performance"""
        context = f"""
        Product Performance Analysis:
        Current Metrics: {json.dumps(metrics, indent=2)}
        Historical Performance: {json.dumps(self.product_metrics, indent=2)}
        User Research Insights: {len(self.user_research)} studies
        A/B Test Results: {len(self.ab_tests)} experiments
        """
        
        prompt = """
        Analyze product performance and provide strategic recommendations:
        1. Performance trend analysis and pattern identification
        2. User satisfaction and engagement assessment
        3. Feature adoption and value realization analysis
        4. Market fit and competitive position evaluation
        5. Growth opportunities and optimization areas
        6. Risk factors and mitigation strategies
        7. Resource allocation and priority recommendations
        8. Product strategy adjustments and refinements
        
        Focus on actionable insights that drive product success and user value.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update product metrics
        self.product_metrics.update(metrics)
        
        return {
            "performance_analysis": response,
            "updated_metrics": self.product_metrics,
            "recommendations": ["Strategy review", "Feature prioritization", "User research"]
        }
    
    def update_product_metrics(self, metrics: Dict[str, Any]):
        """Update product performance metrics"""
        self.product_metrics.update(metrics)
        self.add_memory({
            "type": "metrics_update",
            "content": f"Updated product metrics: {json.dumps(metrics, indent=2)}",
            "metadata": {"new_metrics": metrics}
        }) 