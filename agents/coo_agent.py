import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class COOAgent(BaseAgent):
    """Chief Operating Officer Agent - Operations and process management"""
    
    def __init__(self, name: str = "Michael Chang"):
        super().__init__("COO", "Operations", name)
        self.max_workload = 14
        self.operational_processes = {}
        self.supply_chain_metrics = {}
        self.quality_standards = {}
        self.vendor_relationships = []
        self.operational_efficiency = {
            "process_automation": 0.6,
            "quality_score": 0.8,
            "delivery_performance": 0.75,
            "cost_efficiency": 0.7
        }
        self.risk_assessments = []
        self.operational_kpis = {}
        
    def get_system_prompt(self) -> str:
        return """
        You are the COO of a fast-growing tech startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Operations strategy and execution
        - Process optimization and automation
        - Supply chain and vendor management
        - Quality assurance and standards
        - Operational risk management
        - Business continuity planning
        - Cross-functional coordination
        - Scalability and efficiency improvements
        
        OPERATIONAL PHILOSOPHY:
        - Continuous improvement mindset
        - Data-driven process optimization
        - Scalable systems and processes
        - Quality-first approach
        - Proactive risk management
        - Customer-centric operations
        
        LEADERSHIP STYLE:
        - Detail-oriented and systematic
        - Collaborative and cross-functional
        - Results-driven execution
        - Problem-solving oriented
        - Change management focused
        
        COMMUNICATION STYLE:
        - Clear and action-oriented
        - Process-focused solutions
        - Metrics and performance driven
        - Stakeholder alignment focused
        
        Focus on building scalable operations that support rapid growth while maintaining quality and efficiency.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process COO-specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "process_optimization":
            return self._handle_process_optimization(task)
        elif task_type == "vendor_management":
            return self._handle_vendor_management(task)
        elif task_type == "quality_assurance":
            return self._handle_quality_assurance(task)
        elif task_type == "operational_planning":
            return self._handle_operational_planning(task)
        elif task_type == "business_continuity":
            return self._handle_business_continuity(task)
        elif task_type == "supply_chain":
            return self._handle_supply_chain(task)
        elif task_type == "risk_assessment":
            return self._handle_risk_assessment(task)
        else:
            return self._handle_general_operational_task(task)
    
    def _handle_process_optimization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle process optimization initiatives"""
        process_details = task.get("process_details", {})
        
        context = f"""
        Process Optimization Request:
        Process Name: {process_details.get('process_name', 'Unknown')}
        Current Performance: {process_details.get('current_metrics', {})}
        Issues Identified: {process_details.get('issues', [])}
        Stakeholders: {process_details.get('stakeholders', [])}
        Target Improvements: {process_details.get('targets', {})}
        
        Current Operational Efficiency: {json.dumps(self.operational_efficiency, indent=2)}
        """
        
        prompt = """
        Analyze the process and develop optimization plan including:
        1. Current state analysis and pain points
        2. Root cause analysis of inefficiencies
        3. Proposed process improvements and automation opportunities
        4. Implementation roadmap with phases
        5. Resource requirements and timeline
        6. Success metrics and KPIs
        7. Change management strategy
        8. Risk mitigation and contingency plans
        9. Expected ROI and efficiency gains
        
        Provide actionable recommendations with clear implementation steps.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update operational processes
        process_name = process_details.get('process_name', 'general')
        self.operational_processes[process_name] = {
            "optimization_plan": response,
            "status": "planned",
            "created_at": task.get('created_at', '')
        }
        
        return {
            "status": "completed",
            "optimization_plan": response,
            "next_actions": ["Stakeholder alignment", "Resource allocation", "Implementation kickoff"]
        }
    
    def _handle_vendor_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle vendor relationship and supply chain management"""
        vendor_context = task.get("vendor_details", {})
        
        context = f"""
        Vendor Management Request:
        Vendor Type: {vendor_context.get('vendor_type', 'Service provider')}
        Service Category: {vendor_context.get('category', 'General')}
        Current Relationship: {vendor_context.get('current_status', 'New')}
        Performance Issues: {vendor_context.get('issues', [])}
        Contract Details: {vendor_context.get('contract_info', {})}
        
        Current Vendor Relationships: {len(self.vendor_relationships)} active
        Supply Chain Metrics: {json.dumps(self.supply_chain_metrics, indent=2)}
        """
        
        prompt = """
        Develop vendor management strategy including:
        1. Vendor performance evaluation and scorecards
        2. Contract terms optimization and negotiation strategy
        3. Service level agreements (SLAs) and KPIs
        4. Risk assessment and mitigation plans
        5. Alternative vendor identification and backup plans
        6. Cost optimization opportunities
        7. Relationship management and communication protocols
        8. Performance monitoring and review processes
        9. Strategic partnership development opportunities
        
        Focus on building reliable, cost-effective vendor relationships.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update vendor relationships
        vendor_record = {
            "vendor_details": vendor_context,
            "management_strategy": response,
            "status": "active",
            "last_reviewed": task.get('created_at', '')
        }
        self.vendor_relationships.append(vendor_record)
        
        return {
            "status": "completed",
            "vendor_strategy": response,
            "vendor_count": len(self.vendor_relationships)
        }
    
    def _handle_quality_assurance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle quality assurance and standards management"""
        quality_context = task.get("quality_details", {})
        
        context = f"""
        Quality Assurance Request:
        Quality Area: {quality_context.get('area', 'General')}
        Current Standards: {quality_context.get('current_standards', [])}
        Quality Issues: {quality_context.get('issues', [])}
        Compliance Requirements: {quality_context.get('compliance', [])}
        
        Current Quality Standards: {json.dumps(self.quality_standards, indent=2)}
        Operational Efficiency: {json.dumps(self.operational_efficiency, indent=2)}
        """
        
        prompt = """
        Develop quality assurance framework including:
        1. Quality standards definition and documentation
        2. Quality control processes and checkpoints
        3. Testing and validation procedures
        4. Compliance monitoring and reporting
        5. Continuous improvement processes
        6. Quality metrics and measurement systems
        7. Training and certification requirements
        8. Incident response and corrective actions
        9. Audit and review schedules
        
        Ensure quality standards support business objectives and customer satisfaction.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update quality standards
        quality_area = quality_context.get('area', 'general')
        self.quality_standards[quality_area] = {
            "standards": response,
            "implemented_at": task.get('created_at', ''),
            "status": "active"
        }
        
        return {
            "status": "completed",
            "quality_framework": response,
            "standards_updated": True
        }
    
    def _handle_operational_planning(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle operational planning and capacity management"""
        planning_context = task.get("planning_details", {})
        
        context = f"""
        Operational Planning Request:
        Planning Horizon: {planning_context.get('horizon', '12 months')}
        Growth Projections: {planning_context.get('growth_targets', {})}
        Resource Constraints: {planning_context.get('constraints', [])}
        Strategic Objectives: {planning_context.get('objectives', [])}
        
        Current Operational KPIs: {json.dumps(self.operational_kpis, indent=2)}
        Operational Efficiency: {json.dumps(self.operational_efficiency, indent=2)}
        """
        
        prompt = """
        Create comprehensive operational plan including:
        1. Capacity planning and resource requirements
        2. Operational scalability roadmap
        3. Technology and infrastructure needs
        4. Process standardization and documentation
        5. Team structure and role definitions
        6. Performance metrics and monitoring systems
        7. Budget requirements and cost projections
        8. Risk factors and mitigation strategies
        9. Implementation timeline and milestones
        
        Align operational capabilities with business growth objectives.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "operational_plan": response,
            "planning_horizon": planning_context.get('horizon', '12 months')
        }
    
    def _handle_business_continuity(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle business continuity and disaster recovery planning"""
        continuity_context = task.get("continuity_details", {})
        
        context = f"""
        Business Continuity Planning:
        Risk Scenario: {continuity_context.get('scenario', 'General preparedness')}
        Critical Systems: {continuity_context.get('critical_systems', [])}
        Recovery Objectives: {continuity_context.get('objectives', {})}
        Stakeholders: {continuity_context.get('stakeholders', [])}
        
        Current Risk Assessments: {len(self.risk_assessments)} completed
        Operational Processes: {len(self.operational_processes)} documented
        """
        
        prompt = """
        Develop business continuity plan including:
        1. Business impact analysis and critical function identification
        2. Risk assessment and threat scenarios
        3. Recovery strategies and procedures
        4. Communication plans and stakeholder notifications
        5. Resource requirements and backup systems
        6. Testing and validation procedures
        7. Training and awareness programs
        8. Plan maintenance and update schedules
        9. Coordination with external partners and vendors
        
        Ensure business resilience and rapid recovery capabilities.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "continuity_plan": response,
            "risk_coverage": "comprehensive"
        }
    
    def _handle_supply_chain(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle supply chain optimization and management"""
        supply_context = task.get("supply_details", {})
        
        context = f"""
        Supply Chain Management:
        Supply Category: {supply_context.get('category', 'General')}
        Current Performance: {supply_context.get('performance', {})}
        Issues: {supply_context.get('issues', [])}
        Cost Targets: {supply_context.get('cost_targets', {})}
        
        Supply Chain Metrics: {json.dumps(self.supply_chain_metrics, indent=2)}
        Vendor Relationships: {len(self.vendor_relationships)} active
        """
        
        prompt = """
        Optimize supply chain strategy including:
        1. Supply chain mapping and analysis
        2. Vendor diversification and risk management
        3. Cost optimization and negotiation strategies
        4. Inventory management and demand forecasting
        5. Logistics and distribution optimization
        6. Quality control and compliance monitoring
        7. Technology integration and automation
        8. Performance metrics and dashboards
        9. Sustainability and ESG considerations
        
        Build resilient and cost-effective supply chain operations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update supply chain metrics
        category = supply_context.get('category', 'general')
        self.supply_chain_metrics[category] = {
            "optimization_plan": response,
            "last_updated": task.get('created_at', ''),
            "status": "optimized"
        }
        
        return {
            "status": "completed",
            "supply_chain_strategy": response,
            "optimization_areas": category
        }
    
    def _handle_risk_assessment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle operational risk assessment and mitigation"""
        risk_context = task.get("risk_details", {})
        
        context = f"""
        Risk Assessment Request:
        Risk Category: {risk_context.get('category', 'Operational')}
        Risk Level: {risk_context.get('level', 'Medium')}
        Impact Areas: {risk_context.get('impact_areas', [])}
        Current Controls: {risk_context.get('current_controls', [])}
        
        Previous Risk Assessments: {len(self.risk_assessments)}
        Operational Efficiency: {json.dumps(self.operational_efficiency, indent=2)}
        """
        
        prompt = """
        Conduct comprehensive risk assessment including:
        1. Risk identification and categorization
        2. Probability and impact analysis
        3. Current control effectiveness evaluation
        4. Risk appetite and tolerance assessment
        5. Mitigation strategies and action plans
        6. Monitoring and reporting procedures
        7. Escalation and response protocols
        8. Cost-benefit analysis of risk controls
        9. Regular review and update schedules
        
        Provide actionable risk management recommendations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Store risk assessment
        risk_assessment = {
            "risk_details": risk_context,
            "assessment": response,
            "assessment_date": task.get('created_at', ''),
            "status": "completed"
        }
        self.risk_assessments.append(risk_assessment)
        
        return {
            "status": "completed",
            "risk_assessment": response,
            "total_assessments": len(self.risk_assessments)
        }
    
    def _handle_general_operational_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general operational tasks"""
        context = f"Operational Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this operational matter with COO perspective:
        {task.get('description', '')}
        
        Provide operational guidance, process improvements, and actionable solutions.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "operational_guidance": response
        }
    
    def optimize_operations(self, target_areas: List[str]) -> Dict[str, Any]:
        """Optimize specific operational areas"""
        context = f"""
        Operations Optimization:
        Target Areas: {target_areas}
        Current Efficiency: {json.dumps(self.operational_efficiency, indent=2)}
        Active Processes: {len(self.operational_processes)}
        """
        
        prompt = """
        Analyze current operations and provide optimization recommendations:
        1. Performance gap analysis
        2. Automation opportunities
        3. Resource optimization
        4. Process streamlining
        5. Technology leverage
        6. Cost reduction strategies
        7. Quality improvements
        8. Scalability enhancements
        
        Focus on measurable efficiency gains and ROI.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "optimization_recommendations": response,
            "target_areas": target_areas,
            "current_efficiency": self.operational_efficiency
        }
    
    def update_operational_metrics(self, metrics: Dict[str, Any]):
        """Update operational efficiency metrics"""
        self.operational_efficiency.update(metrics)
        self.add_memory({
            "type": "metrics_update",
            "content": f"Updated operational metrics: {json.dumps(metrics, indent=2)}",
            "metadata": {"new_metrics": metrics}
        }) 