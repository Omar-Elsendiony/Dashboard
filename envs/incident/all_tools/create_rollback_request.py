import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateRollbackRequest(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        change_id: str,
        requested_by_id: str,
        incident_id: str = None,
        status: str = "requested"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            rollbacks = data.setdefault("rollback_requests", {})

            valid_status = {"requested","approved","in_progress","completed","failed"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            rollback_id = generate_id(rollbacks)
            timestamp = "2025-10-01T00:00:00"

            new_rb = {
                "rollback_id": rollback_id,
                "change_id": change_id,
                "incident_id": incident_id,
                "requested_by_id": requested_by_id,
                "approved_by_id": None,
                "executed_at": None,
                "validation_completed": False,
                "status": status,
                "created_at": timestamp
            }

            rollbacks[rollback_id] = new_rb
            return json.dumps({"rollback_id": rollback_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_rollback_request",
                "description": "Create a rollback request; default status 'requested'; sets created_at",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "change_id": {"type": "string"},
                        "requested_by_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "status": {"type": "string", "description": "requested|approved|in_progress|completed|failed (default requested)"}
                    },
                    "required": ["change_id","requested_by_id"]
                }
            }
        }
