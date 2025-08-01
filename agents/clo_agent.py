import json
from typing import Dict, List, Any
from .base_agent import BaseAgent

class CLOAgent(BaseAgent):
    """Chief Legal Officer Agent - Legal compliance and risk management"""
    
    def __init__(self, name: str = "David Mitchell"):
        super().__init__("CLO", "Legal", name)
        self.max_workload = 12
        self.legal_cases = []
        self.contracts_database = {}
        self.compliance_framework = {}
        self.legal_risks = []
        self.regulatory_tracking = {}
        self.intellectual_property = {
            "patents": [],
            "trademarks": [],
            "copyrights": [],
            "trade_secrets": []
        }
        self.legal_policies = {}
        self.litigation_history = []
        
    def get_system_prompt(self) -> str:
        return """
        You are the CLO of a technology startup. Your responsibilities include:
        
        CORE RESPONSIBILITIES:
        - Legal strategy and risk management
        - Contract negotiation and management
        - Regulatory compliance and monitoring
        - Intellectual property protection and strategy
        - Corporate governance and structure
        - Privacy and data protection compliance
        - Employment law and HR legal support
        - Litigation management and dispute resolution
        
        LEGAL PHILOSOPHY:
        - Proactive risk identification and mitigation
        - Business-enabling legal solutions
        - Compliance-first approach
        - Strategic legal counsel and guidance
        - Cost-effective legal operations
        - Transparent legal communication
        
        LEADERSHIP STYLE:
        - Risk-aware and prudent
        - Business-oriented legal advice
        - Clear communication of legal implications
        - Collaborative and consultative
        - Preventive rather than reactive approach
        
        COMMUNICATION STYLE:
        - Clear and accessible legal explanations
        - Risk-focused recommendations
        - Business impact oriented
        - Precise and detailed documentation
        
        Focus on protecting the company while enabling business growth and innovation within legal boundaries.
        """
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process CLO-specific tasks"""
        task_type = task.get("type", "general")
        
        if task_type == "contract_review":
            return self._handle_contract_review(task)
        elif task_type == "compliance_assessment":
            return self._handle_compliance_assessment(task)
        elif task_type == "ip_strategy":
            return self._handle_ip_strategy(task)
        elif task_type == "regulatory_analysis":
            return self._handle_regulatory_analysis(task)
        elif task_type == "legal_risk_assessment":
            return self._handle_legal_risk_assessment(task)
        elif task_type == "policy_development":
            return self._handle_policy_development(task)
        elif task_type == "litigation_management":
            return self._handle_litigation_management(task)
        elif task_type == "data_privacy":
            return self._handle_data_privacy(task)
        else:
            return self._handle_general_legal_task(task)
    
    def _handle_contract_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle contract review and negotiation"""
        contract_details = task.get("contract_details", {})
        
        context = f"""
        Contract Review Request:
        Contract Type: {contract_details.get('type', 'General agreement')}
        Counterparty: {contract_details.get('counterparty', 'External party')}
        Contract Value: ${contract_details.get('value', 0):,}
        Key Terms: {contract_details.get('key_terms', [])}
        Risk Areas: {contract_details.get('risk_areas', [])}
        Timeline: {contract_details.get('timeline', '2 weeks')}
        
        Contracts Database: {len(self.contracts_database)} active contracts
        Legal Risks: {len(self.legal_risks)} identified
        """
        
        prompt = """
        Conduct comprehensive contract review including:
        1. Legal and regulatory compliance analysis
        2. Risk identification and assessment
        3. Terms and conditions evaluation
        4. Liability and indemnification review
        5. Intellectual property considerations
        6. Termination and dispute resolution clauses
        7. Negotiation strategy and key points
        8. Recommended modifications and redlines
        9. Approval recommendations and conditions
        
        Provide business-focused legal analysis with clear risk mitigation strategies.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add contract to database
        contract_id = len(self.contracts_database) + 1
        self.contracts_database[contract_id] = {
            "contract_details": contract_details,
            "review_analysis": response,
            "status": "under_review",
            "reviewed_at": task.get('created_at', '')
        }
        
        return {
            "status": "completed",
            "contract_analysis": response,
            "contract_id": contract_id,
            "next_actions": ["Negotiate terms", "Finalize agreement", "Execute contract"]
        }
    
    def _handle_compliance_assessment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle regulatory compliance assessment"""
        compliance_context = task.get("compliance_details", {})
        
        context = f"""
        Compliance Assessment:
        Regulatory Area: {compliance_context.get('area', 'General compliance')}
        Jurisdiction: {compliance_context.get('jurisdiction', 'US Federal')}
        Business Activity: {compliance_context.get('activity', 'Core business')}
        Compliance Requirements: {compliance_context.get('requirements', [])}
        Current Status: {compliance_context.get('current_status', 'Unknown')}
        
        Compliance Framework: {json.dumps(self.compliance_framework, indent=2)}
        Regulatory Tracking: {json.dumps(self.regulatory_tracking, indent=2)}
        """
        
        prompt = """
        Conduct compliance assessment including:
        1. Applicable regulatory requirements identification
        2. Current compliance status evaluation
        3. Gap analysis and risk assessment
        4. Compliance implementation roadmap
        5. Monitoring and reporting procedures
        6. Training and awareness requirements
        7. Compliance cost and resource analysis
        8. Enforcement and penalty risk evaluation
        9. Ongoing compliance maintenance strategy
        
        Provide actionable compliance recommendations and implementation plan.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update compliance framework
        compliance_area = compliance_context.get('area', 'general')
        self.compliance_framework[compliance_area] = {
            "assessment": response,
            "status": "assessed",
            "assessed_at": task.get('created_at', ''),
            "jurisdiction": compliance_context.get('jurisdiction', 'US Federal')
        }
        
        return {
            "status": "completed",
            "compliance_assessment": response,
            "compliance_area": compliance_area,
            "priority": "HIGH"
        }
    
    def _handle_ip_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle intellectual property strategy and protection"""
        ip_context = task.get("ip_details", {})
        
        context = f"""
        IP Strategy Request:
        IP Type: {ip_context.get('type', 'Patent')}
        Innovation/Asset: {ip_context.get('asset', 'Technology innovation')}
        Business Value: {ip_context.get('business_value', 'Competitive advantage')}
        Geographic Scope: {ip_context.get('geographic_scope', 'US')}
        Timeline: {ip_context.get('timeline', '6 months')}
        
        Current IP Portfolio: {json.dumps(self.intellectual_property, indent=2)}
        """
        
        prompt = """
        Develop IP strategy and protection plan including:
        1. IP asset identification and evaluation
        2. Patentability and protectability analysis
        3. Prior art search and freedom to operate assessment
        4. IP protection strategy and filing recommendations
        5. Geographic protection strategy
        6. IP portfolio management and optimization
        7. Competitive landscape and IP risk analysis
        8. Monetization and licensing opportunities
        9. IP enforcement and defense strategy
        
        Balance IP protection costs with business value and competitive advantages.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update IP portfolio
        ip_type = ip_context.get('type', 'patent').lower()
        if ip_type in self.intellectual_property:
            self.intellectual_property[ip_type].append({
                "asset": ip_context.get('asset', 'Unknown'),
                "strategy": response,
                "status": "strategy_developed",
                "created_at": task.get('created_at', '')
            })
        
        return {
            "status": "completed",
            "ip_strategy": response,
            "ip_type": ip_type,
            "portfolio_size": len(self.intellectual_property.get(ip_type, []))
        }
    
    def _handle_regulatory_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle regulatory analysis and monitoring"""
        regulatory_context = task.get("regulatory_details", {})
        
        context = f"""
        Regulatory Analysis:
        Regulation/Law: {regulatory_context.get('regulation', 'New regulation')}
        Impact Area: {regulatory_context.get('impact_area', 'Business operations')}
        Effective Date: {regulatory_context.get('effective_date', 'TBD')}
        Jurisdiction: {regulatory_context.get('jurisdiction', 'Federal')}
        Business Impact: {regulatory_context.get('business_impact', 'Medium')}
        
        Regulatory Tracking: {json.dumps(self.regulatory_tracking, indent=2)}
        Compliance Framework: {len(self.compliance_framework)} areas
        """
        
        prompt = """
        Analyze regulatory impact and provide guidance including:
        1. Regulatory requirements interpretation
        2. Business impact assessment and analysis
        3. Compliance obligations and deadlines
        4. Implementation requirements and costs
        5. Risk assessment and mitigation strategies
        6. Competitive implications and opportunities
        7. Stakeholder communication and training needs
        8. Monitoring and reporting requirements
        9. Strategic response recommendations
        
        Provide clear guidance on regulatory compliance and business adaptation.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update regulatory tracking
        regulation = regulatory_context.get('regulation', 'new_regulation')
        self.regulatory_tracking[regulation] = {
            "analysis": response,
            "impact_level": regulatory_context.get('business_impact', 'Medium'),
            "effective_date": regulatory_context.get('effective_date', 'TBD'),
            "analyzed_at": task.get('created_at', '')
        }
        
        return {
            "status": "completed",
            "regulatory_analysis": response,
            "regulation": regulation,
            "compliance_deadline": regulatory_context.get('effective_date', 'TBD')
        }
    
    def _handle_legal_risk_assessment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle legal risk assessment and mitigation"""
        risk_context = task.get("risk_details", {})
        
        context = f"""
        Legal Risk Assessment:
        Risk Category: {risk_context.get('category', 'General legal risk')}
        Risk Description: {risk_context.get('description', '')}
        Potential Impact: {risk_context.get('impact', 'Medium')}
        Likelihood: {risk_context.get('likelihood', 'Medium')}
        Current Controls: {risk_context.get('current_controls', [])}
        
        Existing Legal Risks: {len(self.legal_risks)} identified
        Legal Cases: {len(self.legal_cases)} active
        """
        
        prompt = """
        Conduct legal risk assessment including:
        1. Risk identification and categorization
        2. Probability and impact analysis
        3. Legal precedent and case law review
        4. Current control effectiveness evaluation
        5. Mitigation strategies and recommendations
        6. Cost-benefit analysis of risk controls
        7. Insurance and transfer opportunities
        8. Monitoring and early warning systems
        9. Contingency and response planning
        
        Provide practical risk management recommendations with implementation guidance.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add to legal risks tracking
        legal_risk = {
            "risk_details": risk_context,
            "assessment": response,
            "status": "assessed",
            "assessed_at": task.get('created_at', ''),
            "priority": risk_context.get('impact', 'Medium')
        }
        self.legal_risks.append(legal_risk)
        
        return {
            "status": "completed",
            "risk_assessment": response,
            "risk_id": len(self.legal_risks),
            "total_risks": len(self.legal_risks)
        }
    
    def _handle_policy_development(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle legal policy development and updates"""
        policy_context = task.get("policy_details", {})
        
        context = f"""
        Policy Development:
        Policy Area: {policy_context.get('area', 'General policy')}
        Policy Type: {policy_context.get('type', 'Internal policy')}
        Regulatory Driver: {policy_context.get('driver', 'Best practice')}
        Stakeholders: {policy_context.get('stakeholders', [])}
        Effective Date: {policy_context.get('effective_date', 'TBD')}
        
        Current Legal Policies: {len(self.legal_policies)} active
        Compliance Framework: {json.dumps(self.compliance_framework, indent=2)}
        """
        
        prompt = """
        Develop comprehensive legal policy including:
        1. Policy scope and applicability definition
        2. Legal and regulatory requirements integration
        3. Policy content and procedural guidelines
        4. Roles, responsibilities, and accountability
        5. Implementation and training requirements
        6. Monitoring and compliance procedures
        7. Enforcement and disciplinary measures
        8. Review and update mechanisms
        9. Communication and rollout strategy
        
        Create clear, enforceable policy that meets legal requirements and business needs.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Update legal policies
        policy_area = policy_context.get('area', 'general')
        self.legal_policies[policy_area] = {
            "policy": response,
            "type": policy_context.get('type', 'Internal policy'),
            "effective_date": policy_context.get('effective_date', 'TBD'),
            "created_at": task.get('created_at', ''),
            "status": "draft"
        }
        
        return {
            "status": "completed",
            "policy_document": response,
            "policy_area": policy_area,
            "approval_required": True
        }
    
    def _handle_litigation_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle litigation and dispute management"""
        litigation_context = task.get("litigation_details", {})
        
        context = f"""
        Litigation Management:
        Case Type: {litigation_context.get('type', 'Commercial dispute')}
        Case Status: {litigation_context.get('status', 'New')}
        Counterparty: {litigation_context.get('counterparty', 'External party')}
        Claim Amount: ${litigation_context.get('amount', 0):,}
        Legal Issues: {litigation_context.get('issues', [])}
        
        Litigation History: {len(self.litigation_history)} cases
        Legal Cases: {len(self.legal_cases)} active
        """
        
        prompt = """
        Develop litigation management strategy including:
        1. Case assessment and merit evaluation
        2. Legal strategy and approach development
        3. Discovery and evidence management plan
        4. Settlement negotiation strategy
        5. Litigation budget and cost management
        6. Risk assessment and exposure analysis
        7. Communication and PR considerations
        8. Timeline and milestone planning
        9. External counsel coordination
        
        Balance litigation costs with potential outcomes and business impact.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        # Add to legal cases
        legal_case = {
            "case_details": litigation_context,
            "strategy": response,
            "status": "active",
            "opened_at": task.get('created_at', '')
        }
        self.legal_cases.append(legal_case)
        
        return {
            "status": "completed",
            "litigation_strategy": response,
            "case_id": len(self.legal_cases),
            "estimated_cost": litigation_context.get('amount', 0)
        }
    
    def _handle_data_privacy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle data privacy and protection compliance"""
        privacy_context = task.get("privacy_details", {})
        
        context = f"""
        Data Privacy Assessment:
        Data Type: {privacy_context.get('data_type', 'Personal data')}
        Processing Activity: {privacy_context.get('activity', 'Data collection')}
        Legal Basis: {privacy_context.get('legal_basis', 'Consent')}
        Jurisdictions: {privacy_context.get('jurisdictions', ['US'])}
        Data Subjects: {privacy_context.get('data_subjects', 'Customers')}
        
        Compliance Framework: {json.dumps(self.compliance_framework, indent=2)}
        Legal Policies: {len(self.legal_policies)} active
        """
        
        prompt = """
        Develop data privacy compliance strategy including:
        1. Applicable privacy law identification (GDPR, CCPA, etc.)
        2. Data processing assessment and legal basis
        3. Privacy policy and notice requirements
        4. Consent management and user rights
        5. Data minimization and retention policies
        6. Security and breach notification procedures
        7. Cross-border transfer compliance
        8. Vendor and third-party data sharing
        9. Privacy impact assessment and monitoring
        
        Ensure comprehensive privacy compliance while enabling business operations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "privacy_strategy": response,
            "jurisdictions": privacy_context.get('jurisdictions', ['US']),
            "compliance_priority": "HIGH"
        }
    
    def _handle_general_legal_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general legal tasks"""
        context = f"Legal Task: {task.get('description', '')}"
        
        prompt = f"""
        Address this legal matter with CLO perspective:
        {task.get('description', '')}
        
        Provide legal analysis, risk assessment, and actionable recommendations.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "status": "completed",
            "legal_guidance": response
        }
    
    def review_legal_compliance(self) -> Dict[str, Any]:
        """Conduct comprehensive legal compliance review"""
        context = f"""
        Legal Compliance Review:
        Compliance Framework: {json.dumps(self.compliance_framework, indent=2)}
        Legal Risks: {len(self.legal_risks)} identified
        Active Cases: {len(self.legal_cases)}
        Legal Policies: {len(self.legal_policies)} active
        IP Portfolio: {json.dumps(self.intellectual_property, indent=2)}
        """
        
        prompt = """
        Conduct comprehensive legal compliance review including:
        1. Overall compliance status assessment
        2. High-risk area identification and prioritization
        3. Policy and procedure gap analysis
        4. Regulatory change impact assessment
        5. Legal risk mitigation effectiveness
        6. Resource allocation and training needs
        7. Technology and process improvements
        8. Compliance program optimization
        9. Strategic legal recommendations
        
        Provide executive-level compliance overview with actionable improvements.
        """
        
        response = self.communicate_with_llm(prompt, context)
        
        return {
            "compliance_review": response,
            "compliance_areas": len(self.compliance_framework),
            "risk_count": len(self.legal_risks),
            "recommendations": ["Policy updates", "Training programs", "Process improvements"]
        }
    
    def update_legal_metrics(self, metrics: Dict[str, Any]):
        """Update legal department metrics"""
        self.add_memory({
            "type": "legal_metrics_update",
            "content": f"Updated legal metrics: {json.dumps(metrics, indent=2)}",
            "metadata": {"new_metrics": metrics}
        }) 