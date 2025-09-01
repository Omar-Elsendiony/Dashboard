import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ModifySlaAgreement(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sla_id: str,
        subscription_id: str = None,
        severity_level: str = None,     # P1|P2|P3|P4
        response_time_minutes: int = None,
        resolution_time_hours: int = None,
        availability_percentage: float = None
    ) -> str:
        try:
            slas = data.get("sla_agreements", {})
            if sla_id not in slas:
                return json.dumps({"success": False, "error": f"SLA {sla_id} not found"})

            valid_sev = {"P1","P2","P3","P4"}
            if severity_level and severity_level not in valid_sev:
                return json.dumps({"success": False, "error": f"Invalid severity_level. Must be one of {sorted(valid_sev)}"})

            if response_time_minutes is not None and response_time_minutes < 0:
                return json.dumps({"success": False, "error": "response_time_minutes must be non-negative"})
            if resolution_time_hours is not None and resolution_time_hours < 0:
                return json.dumps({"success": False, "error": "resolution_time_hours must be non-negative"})
            if availability_percentage is not None:
                try:
                    float(availability_percentage)
                except Exception:
                    return json.dumps({"success": False, "error": "availability_percentage must be a number"})

            s = slas[sla_id]
            if subscription_id is not None: s["subscription_id"] = subscription_id
            if severity_level is not None: s["severity_level"] = severity_level
            if response_time_minutes is not None: s["response_time_minutes"] = response_time_minutes
            if resolution_time_hours is not None: s["resolution_time_hours"] = resolution_time_hours
            if availability_percentage is not None: s["availability_percentage"] = availability_percentage

            # Table has no updated_at
            return json.dumps(s)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
    
    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"modify_sla_agreement",
                "description":"Update an SLA agreement; validates enums and numbers",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "sla_id":{"type":"string"},
                        "subscription_id":{"type":"string"},
                        "severity_level":{"type":"string","description":"P1|P2|P3|P4"},
                        "response_time_minutes":{"type":"integer"},
                        "resolution_time_hours":{"type":"integer"},
                        "availability_percentage":{"type":"number"}
                    },
                    "required":["sla_id"]
                }
            }
        }
