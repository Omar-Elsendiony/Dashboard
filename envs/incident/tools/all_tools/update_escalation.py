import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateEscalation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        escalation_id: str,
        status: str = None,
        acknowledged_at: str = None,
        resolved_at: str = None
    ) -> str:
        try:
            escalations = data.get("escalations", {})
            if escalation_id not in escalations:
                return json.dumps({"success": False, "error": f"Escalation {escalation_id} not found"})

            esc = escalations[escalation_id]
            valid_status = {"open","acknowledged","resolved"}

            if status is not None:
                if status not in valid_status:
                    return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
                esc["status"] = status

            if acknowledged_at is not None:
                esc["acknowledged_at"] = acknowledged_at

            if resolved_at is not None:
                esc["resolved_at"] = resolved_at

            # No updated_at field in schema for escalations
            return json.dumps({"success": True, "data": esc})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_escalation",
                "description": "Update escalation status and timestamps",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "escalation_id": {"type": "string"},
                        "status": {"type": "string", "description": "open|acknowledged|resolved"},
                        "acknowledged_at": {"type": "string", "description": "ISO timestamp"},
                        "resolved_at": {"type": "string", "description": "ISO timestamp"}
                    },
                    "required": ["escalation_id"]
                }
            }
        }
