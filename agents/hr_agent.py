import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class HRAgent(BaseAgent):
    """Human Resources Agent - People management and organizational development"""
    
    def __init__(self, name: str = "Rebecca Johnson"):
        super().__init__("HR Director", "Human Resources", name)
        self.max_workload = 12
        self.employee_database = {}
        self.performance_reviews = []
        self.hiring_pipeline = []
        self.training_programs = []
        self.organizational_health = {
            "employee_satisfaction": 0.75,
            "retention_rate": 0.85,
            "engagement_score": 0.72,
            "diversity_index": 0.68
        }
        self.policy_framework = {}
        self.compensation_structure = {}
        
    def get_system_prompt(self) -> str:
        return """
        You are the HR Director of a dynamic tech startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Talent acquisition and retention strategies
        - Performance management and employee development
        - Organizational culture and engagement
        - Compensation and benefits administration
        - Policy development and compliance
        - Diversity, equity, and inclusion initiatives
        - Employee relations and conflict resolution
        - Learning and development programs
        
        HR PHILOSOPHY:
        - Employee-centric approach
        - Data-driven people analytics
        - Continuous learning and growth mindset
        - Inclusive and diverse workplace culture
        - Performance-based recognition and development
        - Work-life balance and well-being focus
        
        LEADERSHIP STYLE:
        - Empathetic and supportive
        - Fair and transparent
        - Strategic and business-aligned
        - Collaborative and cross-functional
        - Change-adaptive and innovative
        
        COMMUNICATION STYLE:
        - Clear and compassionate
        - Confidential and trustworthy
        - Solution-oriented
        - Professional and approachable
        
        Focus on building a high-performance culture while ensuring employee satisfaction and organizational health.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process HR-specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "talent_acquisition":
            return self._handle_talent_acquisition(task)
        elif task_type == "performance_management":
            return self._handle_performance_management(task)
        elif task_type == "employee_development":
            return self._handle_employee_development(task)
        elif task_type == "culture_assessment":
            return self._handle_culture_assessment(task)
        elif task_type == "compensation_review":
            return self._handle_compensation_review(task)
        elif task_type == "policy_development":
            return self._handle_policy_development(task)
        elif task_type == "employee_relations":
            return self._handle_employee_relations(task)
        else:
            return self._handle_general_hr_task(task)
    
    def _handle_talent_acquisition(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle talent acquisition and hiring processes"""
        hiring_request = task.get("hiring_request", {})
        
        context = f"""
        Talent Acquisition Request:
        Position: {hiring_request.get('position', 'Unknown')}
        Department: {hiring_request.get('department', 'Unknown')}
        Level: {hiring_request.get('level', 'Mid-level')}
        Required Skills: {hiring_request.get('skills', [])}
        Timeline: {hiring_request.get('timeline', '30 days')}
        Budget Range: ${hiring_request.get('budget_min', 0):,} - ${hiring_request.get('budget_max', 0):,}
        
        Current Team Size: {len(self.employee_database)}
        Active Hiring Pipeline: {len(self.hiring_pipeline)} positions
        Organizational Health: {json.dumps(self.organizational_health, indent=2)}
        """
        
        prompt = """
        Develop comprehensive talent acquisition strategy including:
        1. Job description and requirements definition
        2. Sourcing strategy and recruitment channels
        3. Candidate evaluation criteria and process
        4. Interview structure and assessment methods
        5. Compensation package and benefits offering
        6. Onboarding and integration plan
        7. Timeline and milestone tracking
        8. Diversity and inclusion considerations
        9. Success metrics and evaluation criteria
        
        Create hiring plan that attracts top talent while maintaining culture fit.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add to hiring pipeline
        hiring_item = {
            "position": hiring_request,
            "strategy": response,
            "status": "active",
            "created_at": task.get('created_at', ''),
            "candidates": []
        }
        self.hiring_pipeline.append(hiring_item)
        
        return {
            "status": "completed",
            "hiring_strategy": response,
            "pipeline_position": len(self.hiring_pipeline),
            "next_actions": ["Post job description", "Begin sourcing", "Set up interview process"]
        }
    
    def _handle_performance_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle performance reviews and management"""
        performance_context = task.get("performance_context", {})
        
        context = f"""
        Performance Management Request:
        Review Type: {performance_context.get('review_type', 'Annual')}
        Employee/Team: {performance_context.get('subject', 'Team-wide')}
        Performance Period: {performance_context.get('period', 'Last 12 months')}
        Focus Areas: {performance_context.get('focus_areas', [])}
        Current Metrics: {performance_context.get('current_metrics', {})}
        
        Performance Review History: {len(self.performance_reviews)} completed
        Organizational Performance: {json.dumps(self.organizational_health, indent=2)}
        """
        
        prompt = """
        Design performance management approach including:
        1. Performance criteria and evaluation framework
        2. Goal setting and OKR alignment
        3. Feedback mechanisms and coaching strategies
        4. Performance improvement plans where needed
        5. Recognition and reward recommendations
        6. Career development and growth planning
        7. Skills gap analysis and training needs
        8. Retention and engagement strategies
        9. Performance tracking and follow-up schedule
        
        Create performance management plan that drives individual and organizational success.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add to performance reviews
        review_record = {
            "context": performance_context,
            "management_plan": response,
            "review_date": task.get('created_at', ''),
            "status": "planned"
        }
        self.performance_reviews.append(review_record)
        
        return {
            "status": "completed",
            "performance_plan": response,
            "follow_up_schedule": "Monthly check-ins",
            "development_opportunities": "To be identified based on assessment"
        }
    
    def _handle_employee_development(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle employee development and training programs"""
        development_request = task.get("development_details", {})
        
        context = f"""
        Employee Development Request:
        Development Focus: {development_request.get('focus', 'General skills')}
        Target Audience: {development_request.get('audience', 'All employees')}
        Skill Gaps: {development_request.get('skill_gaps', [])}
        Business Objectives: {development_request.get('business_goals', [])}
        Timeline: {development_request.get('timeline', '3 months')}
        Budget: ${development_request.get('budget', 0):,}
        
        Current Training Programs: {len(self.training_programs)}
        Employee Database Size: {len(self.employee_database)}
        """
        
        prompt = """
        Design employee development program including:
        1. Learning objectives and competency framework
        2. Training curriculum and content strategy
        3. Delivery methods and learning platforms
        4. Mentorship and coaching components
        5. Assessment and certification processes
        6. Career pathway and progression planning
        7. Resource requirements and budget allocation
        8. Success metrics and program evaluation
        9. Continuous improvement and iteration plan
        
        Create development program that enhances capabilities and engagement.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add to training programs
        program = {
            "details": development_request,
            "program_design": response,
            "status": "designed",
            "created_at": task.get('created_at', ''),
            "participants": []
        }
        self.training_programs.append(program)
        
        return {
            "status": "completed",
            "development_program": response,
            "program_id": len(self.training_programs),
            "implementation_timeline": development_request.get('timeline', '3 months')
        }
    
    def _handle_culture_assessment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assess and improve organizational culture"""
        culture_context = task.get("culture_details", {})
        
        context = f"""
        Culture Assessment Request:
        Assessment Scope: {culture_context.get('scope', 'Organization-wide')}
        Focus Areas: {culture_context.get('focus_areas', [])}
        Current Concerns: {culture_context.get('concerns', [])}
        
        Current Organizational Health Metrics:
        {json.dumps(self.organizational_health, indent=2)}
        
        Employee Count: {len(self.employee_database)}
        Recent Changes: {culture_context.get('recent_changes', [])}
        """
        
        prompt = """
        Conduct comprehensive culture assessment including:
        1. Current culture analysis and health metrics
        2. Employee engagement and satisfaction evaluation
        3. Values alignment and behavioral assessment
        4. Communication and collaboration patterns
        5. Diversity, equity, and inclusion analysis
        6. Work environment and culture drivers
        7. Culture gaps and improvement opportunities
        8. Culture transformation roadmap
        9. Measurement and monitoring framework
        
        Provide actionable insights to strengthen organizational culture.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "culture_assessment": response,
            "current_health_score": self.organizational_health,
            "improvement_priorities": ["Communication", "Engagement", "Development"]
        }
    
    def _handle_compensation_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review and optimize compensation structure"""
        compensation_context = task.get("compensation_details", {})
        
        context = f"""
        Compensation Review Request:
        Review Scope: {compensation_context.get('scope', 'Organization-wide')}
        Market Analysis: {compensation_context.get('market_data', 'Required')}
        Budget Constraints: ${compensation_context.get('budget_limit', 0):,}
        Equity Considerations: {compensation_context.get('equity_focus', [])}
        
        Current Compensation Structure: {json.dumps(self.compensation_structure, indent=2) if self.compensation_structure else 'Under development'}
        Employee Count: {len(self.employee_database)}
        """
        
        prompt = """
        Develop compensation strategy including:
        1. Market competitiveness analysis
        2. Pay equity and fairness assessment
        3. Performance-based compensation alignment
        4. Benefits package optimization
        5. Equity and long-term incentive design
        6. Career progression and salary bands
        7. Total rewards communication strategy
        8. Budget impact and implementation plan
        9. Compliance and legal considerations
        
        Create fair and competitive compensation framework.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update compensation structure
        self.compensation_structure.update({
            "review_date": task.get('created_at', ''),
            "strategy": response,
            "status": "under_review"
        })
        
        return {
            "status": "completed",
            "compensation_strategy": response,
            "implementation_priority": "HIGH",
            "approval_required": ["CEO", "CFO", "Board"]
        }
    
    def _handle_policy_development(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Develop and update HR policies"""
        policy_request = task.get("policy_details", {})
        
        context = f"""
        Policy Development Request:
        Policy Area: {policy_request.get('area', 'General')}
        Policy Type: {policy_request.get('type', 'New policy')}
        Business Driver: {policy_request.get('driver', '')}
        Compliance Requirements: {policy_request.get('compliance', [])}
        Stakeholders: {policy_request.get('stakeholders', [])}
        
        Current Policy Framework: {json.dumps(self.policy_framework, indent=2) if self.policy_framework else 'Basic policies in place'}
        Organization Size: {len(self.employee_database)} employees
        """
        
        prompt = """
        Develop comprehensive HR policy including:
        1. Policy objectives and scope definition
        2. Legal and compliance requirements analysis
        3. Policy content and procedural guidelines
        4. Implementation and communication strategy
        5. Training and awareness requirements
        6. Monitoring and enforcement mechanisms
        7. Review and update schedule
        8. Stakeholder impact assessment
        9. Risk mitigation and contingency planning
        
        Create clear, enforceable policy that supports business objectives.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update policy framework
        policy_area = policy_request.get('area', 'general')
        self.policy_framework[policy_area] = {
            "policy": response,
            "created_at": task.get('created_at', ''),
            "status": "draft",
            "type": policy_request.get('type', 'New policy')
        }
        
        return {
            "status": "completed",
            "policy_document": response,
            "approval_process": ["Legal review", "Management approval", "Implementation"],
            "effective_date": "TBD pending approvals"
        }
    
    def _handle_employee_relations(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle employee relations and conflict resolution"""
        relations_context = task.get("relations_details", {})
        
        context = f"""
        Employee Relations Matter:
        Issue Type: {relations_context.get('issue_type', 'General inquiry')}
        Parties Involved: {relations_context.get('parties', 'Not specified')}
        Severity Level: {relations_context.get('severity', 'Medium')}
        Description: {relations_context.get('description', '')}
        Previous Actions: {relations_context.get('previous_actions', [])}
        
        Organizational Health: {json.dumps(self.organizational_health, indent=2)}
        """
        
        prompt = """
        Address employee relations matter including:
        1. Situation analysis and fact gathering
        2. Stakeholder impact assessment
        3. Policy and legal compliance review
        4. Resolution strategy and options
        5. Communication and mediation approach
        6. Documentation and record keeping
        7. Follow-up and monitoring plan
        8. Prevention and improvement recommendations
        9. Organizational learning opportunities
        
        Provide fair, confidential, and effective resolution approach.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "resolution_plan": response,
            "confidentiality": "HIGH",
            "follow_up_required": True,
            "documentation": "Maintained per policy"
        }
    
    def _handle_general_hr_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general HR tasks"""
        context = f"HR Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this HR matter with director-level perspective:
        {task.get('description', '')}
        
        Provide HR guidance, policy recommendations, and actionable solutions.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "hr_guidance": response
        }
    
    def assess_team_performance(self, team_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess team performance and organizational health"""
        context = f"""
        Team Performance Assessment:
        Metrics: {json.dumps(team_metrics, indent=2)}
        Current Organizational Health: {json.dumps(self.organizational_health, indent=2)}
        Team Size: {len(self.employee_database)}
        """
        
        prompt = """
        Analyze team performance and provide:
        1. Performance trends and patterns analysis
        2. Productivity and efficiency assessment
        3. Engagement and satisfaction indicators
        4. Skills and capability gaps identification
        5. Team dynamics and collaboration evaluation
        6. Workload distribution and balance analysis
        7. Development and training recommendations
        8. Retention risk assessment
        9. Action plan for performance improvement
        
        Provide comprehensive people analytics insights.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "performance_analysis": response,
            "health_indicators": self.organizational_health,
            "recommendations": ["Team development", "Process optimization", "Recognition programs"]
        }
    
    def recommend_hiring(self, department: str, justification: str) -> Dict[str, Any]:
        """Recommend new hiring based on organizational needs"""
        context = f"""
        Hiring Recommendation Request:
        Department: {department}
        Justification: {justification}
        Current Team Size: {len(self.employee_database)}
        Active Hiring: {len(self.hiring_pipeline)} positions
        Organizational Health: {json.dumps(self.organizational_health, indent=2)}
        """
        
        prompt = """
        Evaluate hiring need and provide recommendation including:
        1. Business case and ROI analysis
        2. Organizational capacity and readiness
        3. Skills requirements and job definition
        4. Budget impact and resource allocation
        5. Timeline and hiring strategy
        6. Team integration and cultural fit
        7. Alternative solutions consideration
        8. Risk assessment and mitigation
        
        Provide strategic hiring recommendation with supporting rationale.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "hiring_recommendation": response,
            "priority_level": "To be determined",
            "approval_required": ["Department Head", "CFO", "CEO"]
        }
    
    def update_organizational_health(self, metrics: Dict[str, Any]):
        """Update organizational health metrics"""
        self.organizational_health.update(metrics)
        self.add_memory({
            "type": "health_update",
            "content": f"Updated organizational health metrics: {json.dumps(metrics, indent=2)}",
            "metadata": {"new_metrics": metrics}
        }) 