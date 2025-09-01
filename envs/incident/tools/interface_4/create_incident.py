import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        category: str,
        impact: str,
        client_id: str,
        reporter_id: str,
        detected_at: str,              # required
        component_id: str = None,
        severity: str = None,
        p1_outage_no_workaround: bool = None,
        p1_wide_enterprise_or_5plus_customers: bool = None,
        p1_regulatory_safety_financial: bool = None,
        p1_high_priority_customer_or_recurrent: bool = None,
        p2_major_degradation_with_workaround: bool = None,
        p2_multi_dept_sites_or_critical_functions: bool = None,
        p2_risk_high_priority_sla_breach: bool = None,
        p3_localized_or_non_critical: bool = None,
        p3_moderate_deg_minimal_workaround: bool = None,
        urgency: str = None,
        assigned_manager_id: str = None
    ) -> str:
        # Local helper to avoid referencing the class name
        def compute_severity(
            severity_in: Optional[str],
            p1_a: Optional[bool], p1_b: Optional[bool], p1_c: Optional[bool], p1_d: Optional[bool],
            p2_a: Optional[bool], p2_b: Optional[bool], p2_c: Optional[bool],
            p3_a: Optional[bool], p3_b: Optional[bool]
        ) -> str:
            valid = {"P1","P2","P3","P4"}
            if severity_in:
                return severity_in if severity_in in valid else "__INVALID__"
            if any([p1_a, p1_b, p1_c, p1_d]): return "P1"
            if any([p2_a, p2_b, p2_c]):       return "P2"
            if any([p3_a, p3_b]):             return "P3"
            return "P4"

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            incidents = data.setdefault("incidents", {})

            # Validate impact & urgency
            valid_levels = {"critical","high","medium","low"}
            if impact not in valid_levels:
                return json.dumps({"success": False, "error": f"Invalid impact. Must be one of {sorted(valid_levels)}"})
            if urgency and urgency not in valid_levels:
                return json.dumps({"success": False, "error": f"Invalid urgency. Must be one of {sorted(valid_levels)}"})

            # Validate detected_at (non-empty string; caller ensures ISO format)
            if not detected_at or not isinstance(detected_at, str) or not detected_at.strip():
                return json.dumps({"success": False, "error": "detected_at is required and must be a non-empty ISO timestamp string"})

            # Compute severity if not provided
            sev = compute_severity(
                severity,
                p1_outage_no_workaround,
                p1_wide_enterprise_or_5plus_customers,
                p1_regulatory_safety_financial,
                p1_high_priority_customer_or_recurrent,
                p2_major_degradation_with_workaround,
                p2_multi_dept_sites_or_critical_functions,
                p2_risk_high_priority_sla_breach,
                p3_localized_or_non_critical,
                p3_moderate_deg_minimal_workaround
            )
            if sev == "__INVALID__":
                return json.dumps({"success": False, "error": "Invalid severity. Must be one of ['P1','P2','P3','P4']"})

            ts = "2025-10-01T00:00:00"
            incident_id = generate_id(incidents)

            new_incident = {
                "incident_id": incident_id,
                "title": title,
                "reporter_id": reporter_id,
                "assigned_manager_id": assigned_manager_id,
                "client_id": client_id,
                "component_id": component_id,
                "severity": sev,
                "status": "open",               # SOP: always start as open
                "impact": impact,
                "urgency": urgency if urgency else impact,
                "category": category,
                "detected_at": detected_at,
                "resolved_at": None,
                "closed_at": None,
                "rto_breach": False,
                "sla_breach": False,
                "is_recurring": False,
                "downtime_minutes": None,
                "created_at": ts,
                "updated_at": ts
            }

            incidents[incident_id] = new_incident
            return json.dumps({"incident_id": incident_id, "severity": sev, "status": "open", "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_incident",
                "description": "Create a new incident; initial status is set to 'open' per SOP; computes severity if not provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "category": {"type": "string"},
                        "impact": {"type": "string", "description": "critical|high|medium|low"},
                        "client_id": {"type": "string"},
                        "reporter_id": {"type": "string"},
                        "detected_at": {"type": "string", "description": "ISO timestamp; required"},
                        "component_id": {"type": "string"},
                        "severity": {"type": "string", "description": "P1|P2|P3|P4"},
                        "p1_outage_no_workaround": {"type": "boolean", "description": "Whether the incident is a P1 outage with no workaround (True/False)"},
                        "p1_wide_enterprise_or_5plus_customers": {"type": "boolean", "description": "Whether the incident affects a wide enterprise or 5+ customers (True/False)"},
                        "p1_regulatory_safety_financial": {"type": "boolean", "description": "Whether the incident is related to regulatory, safety, or financial issues (True/False)"},
                        "p1_high_priority_customer_or_recurrent": {"type": "boolean", "description": "Whether the incident is high priority for a customer or recurrent (True/False)"},
                        "p2_major_degradation_with_workaround": {"type": "boolean", "description": "Whether the incident is a P2 major degradation with a workaround (True/False)"},
                        "p2_multi_dept_sites_or_critical_functions": {"type": "boolean", "description": "Whether the incident affects multiple departments/sites or critical functions (True/False)"},
                        "p2_risk_high_priority_sla_breach": {"type": "boolean", "description": "Whether the incident poses a risk of high priority SLA breach (True/False)"},
                        "p3_localized_or_non_critical": {"type": "boolean", "description": "Whether the incident is localized or non-critical (True/False)"},
                        "p3_moderate_deg_minimal_workaround": {"type": "boolean", "description": "Whether the incident has moderate degradation with minimal workaround (True/False)"},
                        "urgency": {"type": "string", "description": "critical|high|medium|low"},
                        "assigned_manager_id": {"type": "string"}
                    },
                    "required": ["title","category","impact","client_id","reporter_id","detected_at"]
                }
            }
        }
