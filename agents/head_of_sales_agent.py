import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class HeadOfSalesAgent(BaseAgent):
    """Head of Sales Agent - Sales strategy and revenue generation"""
    
    def __init__(self, name: str = "James Carter"):
        super().__init__("Head of Sales", "Sales", name)
        self.max_workload = 13
        self.sales_pipeline = []
        self.sales_targets = {}
        self.sales_team_performance = {}
        self.customer_accounts = {}
        self.sales_metrics = {
            "conversion_rate": 0.15,
            "average_deal_size": 25000,
            "sales_cycle_days": 45,
            "pipeline_velocity": 0.7,
            "quota_attainment": 0.85
        }
        self.sales_strategies = {}
        self.competitive_intel = {}
        self.sales_training_programs = []
        
    def get_system_prompt(self) -> str:
        return """
        You are the Head of Sales of a growing tech startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Sales strategy development and execution
        - Revenue generation and growth acceleration
        - Sales team leadership and performance management
        - Customer relationship management and expansion
        - Sales process optimization and automation
        - Market penetration and territory development
        - Partnership and channel strategy
        - Sales forecasting and pipeline management
        
        SALES PHILOSOPHY:
        - Customer-centric value selling approach
        - Data-driven sales decisions and optimization
        - Consultative and solution-oriented selling
        - Long-term relationship building focus
        - Continuous improvement and adaptation
        - Team collaboration and knowledge sharing
        
        LEADERSHIP STYLE:
        - Results-driven and performance focused
        - Motivational and team-building oriented
        - Coaching and development minded
        - Strategic and tactical balance
        - Customer advocacy and market intelligence
        
        COMMUNICATION STYLE:
        - Persuasive and compelling messaging
        - Clear value proposition articulation
        - Relationship-building focused
        - Results and metrics oriented
        
        Focus on building a high-performing sales organization that drives sustainable revenue growth and customer success.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process Head of Sales specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "sales_strategy":
            return self._handle_sales_strategy(task)
        elif task_type == "pipeline_management":
            return self._handle_pipeline_management(task)
        elif task_type == "team_performance":
            return self._handle_team_performance(task)
        elif task_type == "account_management":
            return self._handle_account_management(task)
        elif task_type == "sales_forecasting":
            return self._handle_sales_forecasting(task)
        elif task_type == "competitive_analysis":
            return self._handle_competitive_analysis(task)
        elif task_type == "sales_training":
            return self._handle_sales_training(task)
        elif task_type == "pricing_strategy":
            return self._handle_pricing_strategy(task)
        else:
            return self._handle_general_sales_task(task)
    
    def _handle_sales_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sales strategy development and optimization"""
        strategy_context = task.get("strategy_details", {})
        
        context = f"""
        Sales Strategy Development:
        Strategic Focus: {strategy_context.get('focus_area', 'Revenue growth')}
        Target Market: {strategy_context.get('target_market', 'Enterprise')}
        Sales Channels: {strategy_context.get('channels', ['Direct sales'])}
        Revenue Goals: ${strategy_context.get('revenue_target', 0):,}
        Timeline: {strategy_context.get('timeline', '12 months')}
        
        Current Sales Metrics: {json.dumps(self.sales_metrics, indent=2)}
        Sales Strategies: {len(self.sales_strategies)} active
        """
        
        prompt = """
        Develop comprehensive sales strategy including:
        1. Market segmentation and target customer analysis
        2. Value proposition and messaging framework
        3. Sales channel strategy and optimization
        4. Territory planning and coverage model
        5. Sales process and methodology definition
        6. Pricing strategy and discount guidelines
        7. Partner and channel development strategy
        8. Sales technology and tool requirements
        9. Performance metrics and success criteria
        
        Create strategy that maximizes revenue growth while building sustainable customer relationships.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update sales strategies
        strategy_focus = strategy_context.get('focus_area', 'general')
        self.sales_strategies[strategy_focus] = {
            "strategy": response,
            "created_at": task.get('created_at', ''),
            "target_revenue": strategy_context.get('revenue_target', 0),
            "status": "active"
        }
        
        return {
            "status": "completed",
            "sales_strategy": response,
            "revenue_target": strategy_context.get('revenue_target', 0),
            "next_actions": ["Team training", "Process implementation", "Performance tracking"]
        }
    
    def _handle_pipeline_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sales pipeline management and optimization"""
        pipeline_context = task.get("pipeline_details", {})
        
        context = f"""
        Pipeline Management:
        Pipeline Analysis: {pipeline_context.get('analysis_type', 'Quarterly review')}
        Focus Stage: {pipeline_context.get('focus_stage', 'All stages')}
        Deal Size Range: ${pipeline_context.get('min_deal', 0):,} - ${pipeline_context.get('max_deal', 0):,}
        Time Period: {pipeline_context.get('period', 'Current quarter')}
        
        Current Pipeline: {len(self.sales_pipeline)} opportunities
        Sales Metrics: {json.dumps(self.sales_metrics, indent=2)}
        """
        
        prompt = """
        Analyze and optimize sales pipeline including:
        1. Pipeline health and velocity analysis
        2. Stage-by-stage conversion rate optimization
        3. Deal qualification and scoring framework
        4. Bottleneck identification and resolution
        5. Forecast accuracy and predictability
        6. Sales cycle time reduction strategies
        7. Lead quality and source effectiveness
        8. Pipeline coverage and capacity planning
        9. CRM optimization and data quality
        
        Provide actionable insights to accelerate pipeline progression and improve win rates.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "pipeline_analysis": response,
            "pipeline_size": len(self.sales_pipeline),
            "optimization_areas": ["Conversion rates", "Sales cycle", "Lead quality"]
        }
    
    def _handle_team_performance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sales team performance management"""
        performance_context = task.get("performance_details", {})
        
        context = f"""
        Sales Team Performance:
        Performance Period: {performance_context.get('period', 'Last quarter')}
        Team/Individual: {performance_context.get('scope', 'Full team')}
        Performance Metrics: {performance_context.get('metrics', [])}
        Performance Issues: {performance_context.get('issues', [])}
        
        Team Performance: {json.dumps(self.sales_team_performance, indent=2)}
        Sales Metrics: {json.dumps(self.sales_metrics, indent=2)}
        """
        
        prompt = """
        Analyze sales team performance and provide development plan including:
        1. Individual and team performance assessment
        2. Quota attainment and goal achievement analysis
        3. Activity metrics and productivity evaluation
        4. Skill gap identification and training needs
        5. Coaching and development recommendations
        6. Performance improvement action plans
        7. Recognition and incentive strategies
        8. Territory and account optimization
        9. Career development and progression planning
        
        Focus on building high-performing sales professionals and sustainable results.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update team performance tracking
        performance_scope = performance_context.get('scope', 'team')
        self.sales_team_performance[performance_scope] = {
            "assessment": response,
            "period": performance_context.get('period', 'Last quarter'),
            "assessed_at": task.get('created_at', '')
        }
        
        return {
            "status": "completed",
            "performance_assessment": response,
            "development_actions": ["Coaching sessions", "Skills training", "Process optimization"]
        }
    
    def _handle_account_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle strategic account management and expansion"""
        account_context = task.get("account_details", {})
        
        context = f"""
        Account Management:
        Account Type: {account_context.get('type', 'Strategic account')}
        Account Size: ${account_context.get('value', 0):,}
        Relationship Status: {account_context.get('status', 'Active')}
        Expansion Opportunities: {account_context.get('opportunities', [])}
        Risk Factors: {account_context.get('risks', [])}
        
        Customer Accounts: {len(self.customer_accounts)} managed
        Sales Metrics: {json.dumps(self.sales_metrics, indent=2)}
        """
        
        prompt = """
        Develop account management strategy including:
        1. Account portfolio analysis and segmentation
        2. Customer health and satisfaction assessment
        3. Expansion and upselling opportunity identification
        4. Relationship mapping and stakeholder analysis
        5. Account-specific value proposition development
        6. Competitive positioning and differentiation
        7. Risk mitigation and retention strategies
        8. Account team coordination and planning
        9. Success metrics and milestone tracking
        
        Focus on maximizing customer lifetime value and building strategic partnerships.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update customer accounts
        account_id = account_context.get('account_id', len(self.customer_accounts) + 1)
        self.customer_accounts[account_id] = {
            "account_details": account_context,
            "strategy": response,
            "last_updated": task.get('created_at', ''),
            "status": "active"
        }
        
        return {
            "status": "completed",
            "account_strategy": response,
            "account_id": account_id,
            "expansion_potential": account_context.get('value', 0)
        }
    
    def _handle_sales_forecasting(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sales forecasting and revenue prediction"""
        forecast_context = task.get("forecast_details", {})
        
        context = f"""
        Sales Forecasting:
        Forecast Period: {forecast_context.get('period', 'Next quarter')}
        Forecast Type: {forecast_context.get('type', 'Revenue forecast')}
        Historical Data: {forecast_context.get('historical_periods', 4)} periods
        Market Conditions: {forecast_context.get('market_conditions', 'Stable')}
        
        Sales Pipeline: {len(self.sales_pipeline)} opportunities
        Sales Metrics: {json.dumps(self.sales_metrics, indent=2)}
        """
        
        prompt = """
        Create accurate sales forecast including:
        1. Historical performance analysis and trends
        2. Pipeline analysis and probability weighting
        3. Seasonal and market factor adjustments
        4. Territory and segment-specific forecasts
        5. Best case, most likely, and worst case scenarios
        6. Forecast accuracy and confidence intervals
        7. Risk factors and contingency planning
        8. Resource requirements and capacity planning
        9. Monthly progression and milestone tracking
        
        Provide reliable forecast to support business planning and resource allocation.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "sales_forecast": response,
            "forecast_period": forecast_context.get('period', 'Next quarter'),
            "confidence_level": "Medium"
        }
    
    def _handle_competitive_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle competitive intelligence and positioning"""
        competitive_context = task.get("competitive_details", {})
        
        context = f"""
        Competitive Analysis:
        Competitors: {competitive_context.get('competitors', [])}
        Analysis Focus: {competitive_context.get('focus_areas', [])}
        Market Segment: {competitive_context.get('segment', 'Enterprise')}
        Competitive Pressure: {competitive_context.get('pressure_level', 'Medium')}
        
        Competitive Intelligence: {json.dumps(self.competitive_intel, indent=2)}
        Sales Metrics: {json.dumps(self.sales_metrics, indent=2)}
        """
        
        prompt = """
        Conduct sales-focused competitive analysis including:
        1. Competitor sales strategy and approach analysis
        2. Pricing and packaging comparison
        3. Sales messaging and positioning assessment
        4. Win/loss analysis and pattern identification
        5. Competitive differentiation and advantages
        6. Sales objection handling and responses
        7. Market positioning and perception analysis
        8. Competitive threat assessment and response
        9. Sales enablement and battle card development
        
        Provide actionable intelligence to improve competitive win rates and positioning.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update competitive intelligence
        for competitor in competitive_context.get('competitors', ['market']):
            self.competitive_intel[competitor] = {
                "analysis": response,
                "analyzed_at": task.get('created_at', ''),
                "focus_areas": competitive_context.get('focus_areas', [])
            }
        
        return {
            "status": "completed",
            "competitive_analysis": response,
            "competitors_analyzed": len(competitive_context.get('competitors', [])),
            "battle_cards_needed": True
        }
    
    def _handle_sales_training(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sales training and development programs"""
        training_context = task.get("training_details", {})
        
        context = f"""
        Sales Training:
        Training Focus: {training_context.get('focus', 'General sales skills')}
        Target Audience: {training_context.get('audience', 'All sales team')}
        Skill Gaps: {training_context.get('skill_gaps', [])}
        Training Format: {training_context.get('format', 'Workshop')}
        Timeline: {training_context.get('timeline', '4 weeks')}
        
        Training Programs: {len(self.sales_training_programs)} active
        Team Performance: {json.dumps(self.sales_team_performance, indent=2)}
        """
        
        prompt = """
        Design sales training program including:
        1. Training needs assessment and gap analysis
        2. Learning objectives and competency framework
        3. Curriculum design and content development
        4. Training methodology and delivery approach
        5. Practical exercises and role-playing scenarios
        6. Assessment and certification criteria
        7. Ongoing coaching and reinforcement plan
        8. Performance measurement and ROI tracking
        9. Continuous improvement and iteration
        
        Create practical training that improves sales performance and results.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add training program
        training_program = {
            "training_details": training_context,
            "program_design": response,
            "status": "designed",
            "created_at": task.get('created_at', '')
        }
        self.sales_training_programs.append(training_program)
        
        return {
            "status": "completed",
            "training_program": response,
            "program_id": len(self.sales_training_programs),
            "training_timeline": training_context.get('timeline', '4 weeks')
        }
    
    def _handle_pricing_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pricing strategy and optimization"""
        pricing_context = task.get("pricing_details", {})
        
        context = f"""
        Pricing Strategy:
        Product/Service: {pricing_context.get('product', 'Core offering')}
        Market Segment: {pricing_context.get('segment', 'Enterprise')}
        Competitive Position: {pricing_context.get('position', 'Premium')}
        Current Pricing: ${pricing_context.get('current_price', 0):,}
        Price Sensitivity: {pricing_context.get('sensitivity', 'Medium')}
        
        Sales Metrics: {json.dumps(self.sales_metrics, indent=2)}
        Competitive Intelligence: {len(self.competitive_intel)} competitors tracked
        """
        
        prompt = """
        Develop pricing strategy including:
        1. Market-based pricing analysis and benchmarking
        2. Value-based pricing framework and justification
        3. Competitive pricing positioning and differentiation
        4. Price elasticity and demand analysis
        5. Discount structure and approval guidelines
        6. Bundle and package pricing optimization
        7. Pricing for different customer segments
        8. Price testing and optimization methodology
        9. Sales team pricing training and enablement
        
        Balance revenue optimization with market competitiveness and customer value perception.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "pricing_strategy": response,
            "current_price": pricing_context.get('current_price', 0),
            "optimization_potential": "Medium"
        }
    
    def _handle_general_sales_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general sales tasks"""
        context = f"Sales Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this sales matter with Head of Sales perspective:
        {task.get('description', '')}
        
        Provide sales strategy, process optimization, and actionable recommendations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "sales_guidance": response
        }
    
    def analyze_sales_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall sales performance and provide recommendations"""
        context = f"""
        Sales Performance Analysis:
        Current Metrics: {json.dumps(metrics, indent=2)}
        Historical Performance: {json.dumps(self.sales_metrics, indent=2)}
        Pipeline Health: {len(self.sales_pipeline)} opportunities
        Team Performance: {json.dumps(self.sales_team_performance, indent=2)}
        """
        
        prompt = """
        Analyze sales performance and provide strategic recommendations:
        1. Revenue growth trends and pattern analysis
        2. Sales efficiency and productivity assessment
        3. Pipeline health and conversion optimization
        4. Market opportunity and expansion analysis
        5. Team performance and capability evaluation
        6. Process improvement and automation opportunities
        7. Technology and tool optimization needs
        8. Competitive positioning and response strategies
        
        Focus on actionable insights that drive revenue growth and team performance.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update sales metrics
        self.sales_metrics.update(metrics)
        
        return {
            "performance_analysis": response,
            "updated_metrics": self.sales_metrics,
            "recommendations": ["Process optimization", "Team training", "Technology upgrades"]
        }
    
    def update_sales_metrics(self, metrics: Dict[str, Any]):
        """Update sales performance metrics"""
        self.sales_metrics.update(metrics)
        self.add_memory({
            "type": "sales_metrics_update",
            "content": f"Updated sales metrics: {json.dumps(metrics, indent=2)}",
            "metadata": {"new_metrics": metrics}
        }) 