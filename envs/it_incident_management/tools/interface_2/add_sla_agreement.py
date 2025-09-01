import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddSlaAgreement(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        subscription_id: str,
        severity_level: str,
        response_time_minutes: int,
        resolution_time_hours: int,
        availability_percentage: str = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            slas = data.setdefault("sla_agreements", {})

            valid_levels = ["P1","P2","P3","P4"]
            if severity_level not in valid_levels:
                return json.dumps({"success": False, "error": f"Invalid severity_level. Must be one of {valid_levels}"})

            if not isinstance(response_time_minutes, int):
                return json.dumps({"success": False, "error": "response_time_minutes must be an integer"})
            if not isinstance(resolution_time_hours, int):
                return json.dumps({"success": False, "error": "resolution_time_hours must be an integer"})

            sla_id = generate_id(slas)
            timestamp = "2025-09-02T23:59:59"

            new_sla = {
                "sla_id": sla_id,
                "subscription_id": subscription_id,
                "severity_level": severity_level,
                "response_time_minutes": response_time_minutes,
                "resolution_time_hours": resolution_time_hours,
                "availability_percentage": availability_percentage,
                "created_at": timestamp
            }

            slas[sla_id] = new_sla
            return json.dumps({"sla_id": sla_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_sla_agreement",
                "description": "Create a new SLA agreement for a subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string"},
                        "severity_level": {"type": "string", "description": "P1|P2|P3|P4"},
                        "response_time_minutes": {"type": "integer"},
                        "resolution_time_hours": {"type": "integer"},
                        "availability_percentage": {"type": "string", "description": "e.g., '99.90'"}
                    },
                    "required": ["subscription_id","severity_level","response_time_minutes","resolution_time_hours"]
                }
            }
        }
