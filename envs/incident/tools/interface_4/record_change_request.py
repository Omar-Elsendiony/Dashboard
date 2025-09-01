import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RecordChangeRequest(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        change_type: str,
        risk_level: str,
        requested_by_id: str,
        incident_id: str = None,
        approved_by_id: str = None,
        scheduled_start: str = None,
        scheduled_end: str = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            changes = data.setdefault("change_requests", {})

            valid_types = {"emergency","standard","normal"}
            if change_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid change_type. Must be one of {sorted(valid_types)}"})

            valid_risk = {"high","medium","low"}
            if risk_level not in valid_risk:
                return json.dumps({"success": False, "error": f"Invalid risk_level. Must be one of {sorted(valid_risk)}"})

            change_id = generate_id(changes)
            timestamp = "2025-10-01T00:00:00"

            new_change = {
                "change_id": change_id,
                "incident_id": incident_id,
                "title": title,
                "change_type": change_type,
                "requested_by_id": requested_by_id,
                "approved_by_id": approved_by_id,
                "risk_level": risk_level,
                "scheduled_start": scheduled_start,
                "scheduled_end": scheduled_end,
                "actual_start": None,
                "actual_end": None,
                "status": "requested",
                "created_at": timestamp
            }

            changes[change_id] = new_change
            return json.dumps({"change_id": change_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_change_request",
                "description": "Create a change request; default status 'requested'; sets created_at",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "change_type": {"type": "string", "description": "emergency|standard|normal"},
                        "risk_level": {"type": "string", "description": "high|medium|low"},
                        "requested_by_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "approved_by_id": {"type": "string"},
                        "scheduled_start": {"type": "string", "description": "ISO timestamp"},
                        "scheduled_end": {"type": "string", "description": "ISO timestamp"}
                    },
                    "required": ["title","change_type","risk_level","requested_by_id"]
                }
            }
        }
