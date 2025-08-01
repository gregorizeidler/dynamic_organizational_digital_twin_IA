import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class CTOAgent(BaseAgent):
    """Chief Technology Officer Agent - Technical leadership and product development"""
    
    def __init__(self, name: str = "Marcus Rodriguez"):
        super().__init__("CTO", "Technology", name)
        self.max_workload = 14
        self.technical_roadmap = {}
        self.development_teams = {}
        self.architecture_decisions = []
        self.tech_stack = {
            "frontend": ["React", "TypeScript", "Next.js"],
            "backend": ["Python", "FastAPI", "PostgreSQL"],
            "infrastructure": ["AWS", "Docker", "Kubernetes"],
            "tools": ["Git", "CI/CD", "Monitoring"]
        }
        self.product_backlog = []
        self.technical_debt_tracking = []
        
    def get_system_prompt(self) -> str:
        return """
        You are the CTO of an innovative tech startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Technical strategy and vision alignment
        - Product development roadmap and execution
        - Engineering team leadership and management
        - Architecture decisions and technical standards
        - Technology evaluation and adoption
        - Technical risk assessment and mitigation
        - Development process optimization
        - Innovation and R&D initiatives
        
        TECHNICAL PHILOSOPHY:
        - Scalable and maintainable architecture
        - Agile development methodologies
        - DevOps and automation focus
        - Security-first approach
        - Performance and reliability optimization
        - Continuous learning and adaptation
        
        LEADERSHIP STYLE:
        - Technical mentorship and guidance
        - Data-driven decision making
        - Collaborative and inclusive
        - Innovation-encouraging
        - Quality-focused with pragmatic delivery
        
        COMMUNICATION STYLE:
        - Clear technical explanations
        - Strategic thinking with practical implementation
        - Problem-solving oriented
        - Future-focused with current constraints awareness
        
        Balance technical excellence with business needs, ensuring scalable solutions that drive company growth.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process CTO-specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "technical_planning":
            return self._handle_technical_planning(task)
        elif task_type == "architecture_review":
            return self._handle_architecture_review(task)
        elif task_type == "team_management":
            return self._handle_team_management(task)
        elif task_type == "technology_evaluation":
            return self._handle_technology_evaluation(task)
        elif task_type == "product_development":
            return self._handle_product_development(task)
        elif task_type == "technical_debt":
            return self._handle_technical_debt(task)
        elif task_type == "security_review":
            return self._handle_security_review(task)
        else:
            return self._handle_general_technical_task(task)
    
    def _handle_technical_planning(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle technical planning and roadmap development"""
        planning_scope = task.get("scope", {})
        
        context = f"""
        Technical Planning Request:
        Scope: {planning_scope.get('description', '')}
        Timeline: {planning_scope.get('timeline', '6 months')}
        Business Objectives: {planning_scope.get('business_goals', [])}
        Current Tech Stack: {json.dumps(self.tech_stack, indent=2)}
        Team Capacity: {len(self.development_teams)} teams
        """
        
        prompt = """
        Create a comprehensive technical roadmap including:
        1. Technical architecture overview and evolution
        2. Development milestones and dependencies
        3. Resource requirements and team allocation
        4. Technology upgrades and migrations
        5. Risk assessment and mitigation strategies
        6. Performance and scalability considerations
        7. Integration and deployment strategies
        8. Quality assurance and testing plans
        
        Align technical decisions with business objectives and delivery timelines.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        self.technical_roadmap.update({
            "scope": planning_scope,
            "plan": response,
            "created_at": task.get('created_at', ''),
            "status": "active"
        })
        
        return {
            "status": "completed",
            "technical_roadmap": response,
            "next_actions": ["Share with engineering teams", "Get stakeholder approval", "Begin implementation"]
        }
    
    def _handle_architecture_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review and approve architectural decisions"""
        architecture_proposal = task.get("proposal", {})
        
        context = f"""
        Architecture Review:
        Component: {architecture_proposal.get('component', 'Unknown')}
        Current Architecture: {architecture_proposal.get('current_state', '')}
        Proposed Changes: {architecture_proposal.get('proposed_changes', '')}
        Rationale: {architecture_proposal.get('rationale', '')}
        Impact: {architecture_proposal.get('impact_assessment', '')}
        
        Current Tech Stack: {json.dumps(self.tech_stack, indent=2)}
        """
        
        prompt = """
        Conduct thorough architecture review covering:
        1. Technical feasibility and soundness
        2. Scalability and performance implications
        3. Security and compliance considerations
        4. Maintainability and technical debt impact
        5. Integration with existing systems
        6. Resource requirements and timeline
        7. Risk assessment and mitigation
        8. Alternative approaches comparison
        
        Provide APPROVE/REJECT/MODIFY decision with detailed technical rationale.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        decision_record = {
            "proposal": architecture_proposal,
            "review": response,
            "decision_date": task.get('created_at', ''),
            "reviewer": self.name
        }
        
        self.architecture_decisions.append(decision_record)
        
        return {
            "status": "completed",
            "architecture_review": response,
            "decision_recorded": True
        }
    
    def _handle_team_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Manage engineering teams and development processes"""
        team_context = task.get("team_context", {})
        
        context = f"""
        Team Management Task:
        Team: {team_context.get('team_name', 'Engineering')}
        Issue/Request: {team_context.get('description', '')}
        Team Size: {team_context.get('team_size', 'Unknown')}
        Current Projects: {team_context.get('current_projects', [])}
        Performance Metrics: {team_context.get('metrics', {})}
        """
        
        prompt = """
        Address the team management situation considering:
        1. Team productivity and efficiency
        2. Skill development and mentoring needs
        3. Resource allocation and workload distribution
        4. Process improvements and optimizations
        5. Team morale and engagement
        6. Technical challenges and blockers
        7. Career development and growth paths
        8. Collaboration and communication enhancement
        
        Provide actionable leadership guidance and solutions.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update team tracking
        team_name = team_context.get('team_name', 'default')
        self.development_teams[team_name] = {
            "last_review": task.get('created_at', ''),
            "guidance": response,
            "metrics": team_context.get('metrics', {})
        }
        
        return {
            "status": "completed",
            "team_guidance": response,
            "follow_up_actions": ["Schedule team meeting", "Monitor progress", "Provide support"]
        }
    
    def _handle_technology_evaluation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate new technologies and tools"""
        tech_evaluation = task.get("technology", {})
        
        context = f"""
        Technology Evaluation:
        Technology: {tech_evaluation.get('name', 'Unknown')}
        Category: {tech_evaluation.get('category', 'Unknown')}
        Use Case: {tech_evaluation.get('use_case', '')}
        Current Solution: {tech_evaluation.get('current_solution', '')}
        Business Driver: {tech_evaluation.get('business_need', '')}
        
        Current Tech Stack: {json.dumps(self.tech_stack, indent=2)}
        """
        
        prompt = """
        Evaluate the technology considering:
        1. Technical capabilities and limitations
        2. Integration complexity and compatibility
        3. Performance and scalability benefits
        4. Security and compliance implications
        5. Cost analysis (licensing, implementation, maintenance)
        6. Learning curve and team adoption
        7. Community support and ecosystem maturity
        8. Long-term viability and roadmap
        9. Alternative solutions comparison
        
        Provide ADOPT/TRIAL/ASSESS/HOLD recommendation with detailed analysis.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "technology_evaluation": response,
            "recommendation_type": "ASSESS"  # Default, would be extracted from response
        }
    
    def _handle_product_development(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Manage product development lifecycle"""
        product_request = task.get("product_details", {})
        
        context = f"""
        Product Development Request:
        Feature/Product: {product_request.get('name', 'Unknown')}
        Requirements: {product_request.get('requirements', [])}
        Priority: {product_request.get('priority', 'Medium')}
        Target Timeline: {product_request.get('timeline', 'Not specified')}
        Success Metrics: {product_request.get('success_metrics', [])}
        
        Current Backlog Size: {len(self.product_backlog)}
        Team Capacity: {len(self.development_teams)} teams
        """
        
        prompt = """
        Plan the product development approach including:
        1. Technical requirements analysis
        2. Architecture and design considerations
        3. Development methodology and approach
        4. Team assignment and resource allocation
        5. Timeline estimation and milestones
        6. Testing and quality assurance strategy
        7. Deployment and rollout plan
        8. Risk identification and mitigation
        9. Success metrics and monitoring
        
        Create actionable development plan with clear deliverables.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add to product backlog
        backlog_item = {
            "product": product_request,
            "development_plan": response,
            "status": "planned",
            "added_date": task.get('created_at', '')
        }
        self.product_backlog.append(backlog_item)
        
        return {
            "status": "completed",
            "development_plan": response,
            "backlog_position": len(self.product_backlog)
        }
    
    def _handle_technical_debt(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Address technical debt and code quality issues"""
        debt_context = task.get("debt_details", {})
        
        context = f"""
        Technical Debt Assessment:
        Component/Area: {debt_context.get('component', 'Unknown')}
        Issue Description: {debt_context.get('description', '')}
        Impact Level: {debt_context.get('impact', 'Medium')}
        Business Risk: {debt_context.get('business_risk', '')}
        
        Current Technical Debt Items: {len(self.technical_debt_tracking)}
        """
        
        prompt = """
        Analyze the technical debt situation and provide:
        1. Impact assessment on system performance and maintainability
        2. Business risk evaluation and urgency classification
        3. Refactoring strategy and approach
        4. Resource requirements and timeline estimation
        5. Priority ranking relative to new features
        6. Interim mitigation strategies
        7. Prevention measures for future occurrences
        8. ROI analysis for debt resolution
        
        Balance technical excellence with business delivery needs.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        debt_item = {
            "details": debt_context,
            "analysis": response,
            "status": "identified",
            "priority": debt_context.get('impact', 'Medium'),
            "date_identified": task.get('created_at', '')
        }
        self.technical_debt_tracking.append(debt_item)
        
        return {
            "status": "completed",
            "debt_analysis": response,
            "debt_queue_position": len(self.technical_debt_tracking)
        }
    
    def _handle_security_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct security reviews and assessments"""
        security_context = task.get("security_details", {})
        
        context = f"""
        Security Review Request:
        Scope: {security_context.get('scope', 'General')}
        Concern/Issue: {security_context.get('description', '')}
        System/Component: {security_context.get('component', 'All systems')}
        Risk Level: {security_context.get('risk_level', 'Medium')}
        
        Current Tech Stack: {json.dumps(self.tech_stack, indent=2)}
        """
        
        prompt = """
        Conduct comprehensive security review covering:
        1. Vulnerability assessment and threat modeling
        2. Authentication and authorization mechanisms
        3. Data protection and encryption standards
        4. Network security and access controls
        5. Code security and injection prevention
        6. Infrastructure security and hardening
        7. Compliance requirements and standards
        8. Security monitoring and incident response
        9. Remediation recommendations and priorities
        
        Provide actionable security improvements and implementation plan.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "security_assessment": response,
            "priority": security_context.get('risk_level', 'Medium'),
            "follow_up": ["Implement recommendations", "Schedule follow-up review", "Update security policies"]
        }
    
    def _handle_general_technical_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general technical leadership tasks"""
        context = f"Technical Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this technical matter with CTO perspective:
        {task.get('description', '')}
        
        Provide technical leadership, guidance, and actionable recommendations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "technical_guidance": response
        }
    
    def assign_development_task(self, team_name: str, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Assign development tasks to engineering teams"""
        context = f"""
        Task Assignment:
        Target Team: {team_name}
        Task: {task_details.get('description', '')}
        Priority: {task_details.get('priority', 'Medium')}
        Estimated Effort: {task_details.get('effort', 'Unknown')}
        Dependencies: {task_details.get('dependencies', [])}
        """
        
        prompt = """
        Provide task assignment guidance including:
        1. Technical approach and implementation strategy
        2. Resource allocation and team member assignment
        3. Timeline estimation and milestone breakdown
        4. Quality standards and acceptance criteria
        5. Risk factors and mitigation strategies
        6. Collaboration requirements with other teams
        
        Ensure clear deliverables and success criteria.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "assignment": response,
            "team": team_name,
            "estimated_completion": task_details.get('timeline', 'TBD')
        }
    
    def update_tech_stack(self, updates: Dict[str, Any]):
        """Update the current technology stack"""
        self.tech_stack.update(updates)
        self.add_memory({
            "type": "tech_stack_update",
            "content": f"Updated tech stack: {json.dumps(updates, indent=2)}",
            "metadata": {"updates": updates}
        }) 