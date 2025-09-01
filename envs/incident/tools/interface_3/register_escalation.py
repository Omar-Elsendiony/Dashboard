import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RegisterEscalation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        escalated_to_id: str,
        escalation_level: str,
        escalation_reason: str,
        status: str = "open",
        acknowledged_at: str = None,
        resolved_at: str = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            escalations = data.setdefault("escalations", {})

            valid_level = {"technical","management","executive","vendor"}
            if escalation_level not in valid_level:
                return json.dumps({"success": False, "error": f"Invalid escalation_level. Must be one of {sorted(valid_level)}"})

            valid_reason = {"sla_breach","severity_increase","resource_unavailable","executive_request","client_demand"}
            if escalation_reason not in valid_reason:
                return json.dumps({"success": False, "error": f"Invalid escalation_reason. Must be one of {sorted(valid_reason)}"})

            valid_status = {"open","acknowledged","resolved"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            escalation_id = generate_id(escalations)
            timestamp = "2025-10-01T00:00:00"

            new_escalation = {
                "escalation_id": escalation_id,
                "incident_id": incident_id,
                "escalated_by_id": "system",  # No actor param supplied; defaulting to system
                "escalated_to_id": escalated_to_id,
                "escalation_reason": escalation_reason,
                "escalation_level": escalation_level,
                "escalated_at": timestamp,
                "acknowledged_at": acknowledged_at,
                "resolved_at": resolved_at,
                "status": status,
                "created_at": timestamp
            }

            escalations[escalation_id] = new_escalation
            return json.dumps({"escalation_id": escalation_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_escalation",
                "description": "Create a new escalation for an incident; sets escalated_at and created_at",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "escalated_to_id": {"type": "string"},
                        "escalation_level": {"type": "string", "description": "technical|management|executive|vendor"},
                        "escalation_reason": {"type": "string", "description": "sla_breach|severity_increase|resource_unavailable|executive_request|client_demand"},
                        "status": {"type": "string", "description": "open|acknowledged|resolved (default open)"},
                        "acknowledged_at": {"type": "string", "description": "ISO timestamp"},
                        "resolved_at": {"type": "string", "description": "ISO timestamp"}
                    },
                    "required": ["incident_id","escalated_to_id","escalation_level","escalation_reason"]
                }
            }
        }
