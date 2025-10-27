import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AssessIncidentSeverity(Tool):
    """
    Assesses incident severity based on impact, scope, and business criticality.
    Determines severity level (P1-P4) through systematic evaluation criteria.
    """
    
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        complete_outage: Optional[bool] = None,
        no_workaround: Optional[bool] = None,
        enterprise_impact: Optional[bool] = None,
        affected_parties_count: Optional[int] = None,
        regulatory_implications: Optional[bool] = None,
        high_priority_customer: Optional[bool] = None,
        recurrent_incident: Optional[bool] = None,
        major_degradation: Optional[bool] = None,
        workaround_available: Optional[bool] = None,
        multiple_departments: Optional[bool] = None,
        sla_breach_risk: Optional[bool] = None,
        single_department: Optional[bool] = None,
        moderate_degradation: Optional[bool] = None,
        minimal_workaround: Optional[bool] = None
    ) -> str:
        """
        Evaluates incident severity based on structured criteria and returns P1-P4 classification.
        
        Severity Levels:
        - P1: Critical - Complete outage, enterprise-wide impact, or regulatory implications
        - P2: High - Major degradation, multi-department impact, or SLA breach risk
        - P3: Medium - Single department impact or moderate degradation with workaround
        - P4: Low - Minor impact, localized issue
        """
        
        severity = None
        justification = []
        evaluation_path = []
        
        # P1 Evaluation
        evaluation_path.append("Starting P1 evaluation")
        
        # P1 Criterion 1: Complete outage of business-critical service
        if complete_outage is True and no_workaround is True:
            severity = "P1"
            justification.append("Complete outage of business-critical service with no workaround available")
            evaluation_path.append("P1 Criterion 1: Met - Complete outage without workaround")
        elif complete_outage is not None or no_workaround is not None:
            evaluation_path.append("P1 Criterion 1: Not met - Continuing evaluation")
        
        # P1 Criterion 2: Enterprise or multiple customer impact
        if severity is None and (enterprise_impact is True or (affected_parties_count is not None and affected_parties_count >= 5)):
            severity = "P1"
            if enterprise_impact:
                justification.append("Impacts entire enterprise or multiple customers")
            if affected_parties_count and affected_parties_count >= 5:
                justification.append(f"Affects {affected_parties_count} parties (threshold: 5+)")
            evaluation_path.append("P1 Criterion 2: Met - Enterprise-wide or multi-customer impact")
        elif enterprise_impact is not None or affected_parties_count is not None:
            evaluation_path.append("P1 Criterion 2: Not met - Continuing evaluation")
        
        # P1 Criterion 3: Regulatory, safety, or financial implications
        if severity is None and regulatory_implications is True:
            severity = "P1"
            justification.append("Significant regulatory, safety, or financial implications")
            evaluation_path.append("P1 Criterion 3: Met - Regulatory/safety/financial implications")
        elif regulatory_implications is not None:
            evaluation_path.append("P1 Criterion 3: Not met - Continuing evaluation")
        
        # P1 Criterion 4: High-priority customer or recurrent incident
        if severity is None and (high_priority_customer is True or recurrent_incident is True):
            severity = "P1"
            if high_priority_customer:
                justification.append("Involves high-priority customer with contractual P1 requirements")
            if recurrent_incident:
                justification.append("Recurrent incident with escalated priority")
            evaluation_path.append("P1 Criterion 4: Met - High-priority customer or recurrent incident")
        elif high_priority_customer is not None or recurrent_incident is not None:
            evaluation_path.append("P1 Criterion 4: Not met - Proceeding to P2 evaluation")
        
        # P2 Evaluation
        if severity is None:
            evaluation_path.append("Starting P2 evaluation")
            
            # P2 Criterion 1: Major degradation with workaround
            if major_degradation is True and workaround_available is True:
                severity = "P2"
                justification.append("Major degradation of business-critical services with workaround available")
                evaluation_path.append("P2 Criterion 1: Met - Major degradation with workaround")
            elif major_degradation is not None or workaround_available is not None:
                evaluation_path.append("P2 Criterion 1: Not met - Continuing evaluation")
            
            # P2 Criterion 2: Multiple departments or critical functions
            if severity is None and multiple_departments is True:
                severity = "P2"
                justification.append("Impacts multiple departments, sites, or critical business functions")
                evaluation_path.append("P2 Criterion 2: Met - Multi-department impact")
            elif multiple_departments is not None:
                evaluation_path.append("P2 Criterion 2: Not met - Continuing evaluation")
            
            # P2 Criterion 3: SLA breach risk
            if severity is None and sla_breach_risk is True:
                severity = "P2"
                justification.append("Risks breaching high-priority SLA with significant impact")
                evaluation_path.append("P2 Criterion 3: Met - SLA breach risk")
            elif sla_breach_risk is not None:
                evaluation_path.append("P2 Criterion 3: Not met - Proceeding to P3 evaluation")
        
        # P3 Evaluation
        if severity is None:
            evaluation_path.append("Starting P3 evaluation")
            
            # P3 Criterion 1: Single department or localized impact
            if single_department is True:
                severity = "P3"
                justification.append("Impacts single department, localized users, or non-critical function")
                evaluation_path.append("P3 Criterion 1: Met - Single department impact")
            elif single_department is not None:
                evaluation_path.append("P3 Criterion 1: Not met - Continuing evaluation")
            
            # P3 Criterion 2: Moderate degradation with minimal workaround
            if severity is None and moderate_degradation is True and minimal_workaround is True:
                severity = "P3"
                justification.append("Moderate degradation with operations continuing using minimal workaround")
                evaluation_path.append("P3 Criterion 2: Met - Moderate degradation with minimal workaround")
            elif moderate_degradation is not None or minimal_workaround is not None:
                evaluation_path.append("P3 Criterion 2: Not met - Defaulting to P4")
        
        # P4 Default
        if severity is None:
            severity = "P4"
            justification.append("Low impact incident not meeting higher severity criteria")
            evaluation_path.append("Defaulting to P4 - Minor/localized issue")
        
        result = {
            "severity": severity,
            # "justification": justification,
            # "evaluation_path": evaluation_path,
            # "timestamp": "2025-10-07T12:00:00"
        }
        
        return json.dumps(result)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the AssessIncidentSeverity tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "assess_incident_severity",
                "description": "Assesses and determines incident severity level (P1-P4) through systematic evaluation of impact, scope, and business criticality. Evaluates incidents against structured criteria: P1 for critical outages, enterprise-wide impact, or regulatory implications; P2 for major degradation or multi-department impact; P3 for single department or moderate degradation; P4 for minor issues. Returns severity classification with justification and evaluation path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "complete_outage": {
                            "type": "boolean",
                            "description": "Whether incident causes complete outage of business-critical service (P1 criterion)"
                        },
                        "no_workaround": {
                            "type": "boolean",
                            "description": "Whether no workaround is available for the outage (P1 criterion, evaluated with complete_outage)"
                        },
                        "enterprise_impact": {
                            "type": "boolean",
                            "description": "Whether incident impacts entire enterprise or multiple customers (P1 criterion)"
                        },
                        "affected_parties_count": {
                            "type": "integer",
                            "description": "Number of affected parties/customers (P1 if 5 or more)"
                        },
                        "regulatory_implications": {
                            "type": "boolean",
                            "description": "Whether incident has significant regulatory, safety, or financial implications (P1 criterion)"
                        },
                        "high_priority_customer": {
                            "type": "boolean",
                            "description": "Whether incident involves high-priority customer with contractual P1 requirements (P1 criterion)"
                        },
                        "recurrent_incident": {
                            "type": "boolean",
                            "description": "Whether this is a recurrent incident requiring escalated priority (P1 criterion)"
                        },
                        "major_degradation": {
                            "type": "boolean",
                            "description": "Whether incident causes major degradation of business-critical services (P2 criterion)"
                        },
                        "workaround_available": {
                            "type": "boolean",
                            "description": "Whether a workaround is available for major degradation (P2 criterion, evaluated with major_degradation)"
                        },
                        "multiple_departments": {
                            "type": "boolean",
                            "description": "Whether incident impacts multiple departments, sites, or critical business functions (P2 criterion)"
                        },
                        "sla_breach_risk": {
                            "type": "boolean",
                            "description": "Whether incident risks breaching high-priority SLA with significant impact (P2 criterion)"
                        },
                        "single_department": {
                            "type": "boolean",
                            "description": "Whether incident impacts single department, localized users, or non-critical function (P3 criterion)"
                        },
                        "moderate_degradation": {
                            "type": "boolean",
                            "description": "Whether incident causes moderate degradation (P3 criterion)"
                        },
                        "minimal_workaround": {
                            "type": "boolean",
                            "description": "Whether operations continue using minimal workaround (P3 criterion, evaluated with moderate_degradation)"
                        }
                    },
                    "required": [
                        "complete_outage",
                        "no_workaround",
                        "enterprise_impact",
                        "affected_parties_count",
                        "regulatory_implications",
                        "high_priority_customer",
                        "recurrent_incident",
                        "major_degradation",
                        "workaround_available",
                        "multiple_departments",
                        "sla_breach_risk",
                        "single_department",
                        "moderate_degradation",
                        "minimal_workaround"
                    ]
                }
            }
        }