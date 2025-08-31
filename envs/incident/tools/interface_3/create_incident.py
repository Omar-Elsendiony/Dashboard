import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateIncident(Tool):
    @staticmethod
    def _compute_severity(
        severity: Optional[str],
        p1_outage_no_workaround: Optional[bool],
        p1_wide_enterprise_or_5plus_customers: Optional[bool],
        p1_regulatory_safety_financial: Optional[bool],
        p1_high_priority_customer_or_recurrent: Optional[bool],
        p2_major_degradation_with_workaround: Optional[bool],
        p2_multi_dept_sites_or_critical_functions: Optional[bool],
        p2_risk_high_priority_sla_breach: Optional[bool],
        p3_localized_or_non_critical: Optional[bool],
        p3_moderate_deg_minimal_workaround: Optional[bool]
    ) -> str:
        valid = {"P1","P2","P3","P4"}
        if severity:
            if severity not in valid:
                return "__INVALID__"
            return severity

        p1_flags = any([
            p1_outage_no_workaround, 
            p1_wide_enterprise_or_5plus_customers,
            p1_regulatory_safety_financial,
            p1_high_priority_customer_or_recurrent
        ])
        p2_flags = any([
            p2_major_degradation_with_workaround,
            p2_multi_dept_sites_or_critical_functions,
            p2_risk_high_priority_sla_breach
        ])
        p3_flags = any([
            p3_localized_or_non_critical,
            p3_moderate_deg_minimal_workaround
        ])

        if p1_flags: return "P1"
        if p2_flags: return "P2"
        if p3_flags: return "P3"
        return "P4"

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        category: str,
        impact: str,
        client_id: str,
        reporter_id: str,
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
        assigned_manager_id: str = None,
        detected_at: Optional[str] = None,  # NEW: optional override
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            incidents = data.setdefault("incidents", {})

            valid_impact = {"critical","high","medium","low"}
            if impact not in valid_impact:
                return json.dumps({"success": False, "error": f"Invalid impact. Must be one of {sorted(valid_impact)}"})
            valid_urg = {"critical","high","medium","low"}
            if urgency and urgency not in valid_urg:
                return json.dumps({"success": False, "error": f"Invalid urgency. Must be one of {sorted(valid_urg)}"})

            sev = CreateIncident._compute_severity(
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

            ts = "2025-10-01T00:00:00"  # standard timestamp for created_at/updated_at; default for detected_at
            incident_id = generate_id(incidents)
            detected_ts = (detected_at.strip() if isinstance(detected_at, str) and detected_at.strip() else ts)

            new_incident = {
                "incident_id": incident_id,
                "title": title,
                "reporter_id": reporter_id,
                "assigned_manager_id": assigned_manager_id,
                "client_id": client_id,
                "component_id": component_id,
                "severity": sev,
                "status": "open",
                "impact": impact,
                "urgency": urgency if urgency else impact,  # default urgency to impact
                "category": category,
                "detected_at": detected_ts,  # uses provided value or default ts
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
        # Omitting full flag docs in description to keep concise
        return {
            "type": "function",
            "function": {
                "name": "create_incident",
                "description": "Create a new incident; sets status=open; computes severity if not provided. detected_at can be provided; otherwise defaults.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "category": {"type": "string"},
                        "impact": {"type": "string", "description": "critical|high|medium|low"},
                        "client_id": {"type": "string"},
                        "reporter_id": {"type": "string"},
                        "component_id": {"type": "string"},
                        "severity": {"type": "string", "description": "P1|P2|P3|P4"},
                        "p1_outage_no_workaround": {"type": "boolean"},
                        "p1_wide_enterprise_or_5plus_customers": {"type": "boolean"},
                        "p1_regulatory_safety_financial": {"type": "boolean"},
                        "p1_high_priority_customer_or_recurrent": {"type": "boolean"},
                        "p2_major_degradation_with_workaround": {"type": "boolean"},
                        "p2_multi_dept_sites_or_critical_functions": {"type": "boolean"},
                        "p2_risk_high_priority_sla_breach": {"type": "boolean"},
                        "p3_localized_or_non_critical": {"type": "boolean"},
                        "p3_moderate_deg_minimal_workaround": {"type": "boolean"},
                        "urgency": {"type": "string", "description": "critical|high|medium|low"},
                        "assigned_manager_id": {"type": "string"},
                        "detected_at": {"type": "string", "description": "ISO timestamp; default is 2025-10-01T00:00:00"}
                    },
                    "required": ["title","category","impact","client_id","reporter_id"]
                }
            }
        }
