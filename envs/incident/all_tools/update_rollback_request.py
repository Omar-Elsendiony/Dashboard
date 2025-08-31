import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateRollbackRequest(Tool):
    @staticmethod
    def _is_iso(ts: str) -> bool:
        try:
            datetime.fromisoformat(ts.replace("Z","+00:00"))
            return True
        except Exception:
            return False

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        rollback_id: str,
        change_id: str = None,
        incident_id: str = None,
        requested_by_id: str = None,
        approved_by_id: str = None,
        executed_at: str = None,
        validation_completed: bool = None,
        status: str = None            # requested|approved|in_progress|completed|failed
    ) -> str:
        try:
            rolls = data.get("rollback_requests", {})
            if rollback_id not in rolls:
                return json.dumps({"success": False, "error": f"Rollback request {rollback_id} not found"})

            valid_status = {"requested","approved","in_progress","completed","failed"}
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if executed_at is not None and not UpdateRollbackRequest._is_iso(executed_at):
                return json.dumps({"success": False, "error": "executed_at must be ISO timestamp"})

            r = rolls[rollback_id]
            if change_id is not None: r["change_id"] = change_id
            if incident_id is not None: r["incident_id"] = incident_id
            if requested_by_id is not None: r["requested_by_id"] = requested_by_id
            if approved_by_id is not None: r["approved_by_id"] = approved_by_id
            if executed_at is not None: r["executed_at"] = executed_at
            if validation_completed is not None: r["validation_completed"] = bool(validation_completed)
            if status is not None: r["status"] = status

            return json.dumps(r)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_rollback_request",
                "description":"Update a rollback request; validates enums/boolean/timestamp",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "rollback_id":{"type":"string"},
                        "change_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "requested_by_id":{"type":"string"},
                        "approved_by_id":{"type":"string"},
                        "executed_at":{"type":"string","description":"ISO timestamp"},
                        "validation_completed":{"type":"boolean"},
                        "status":{"type":"string","description":"requested|approved|in_progress|completed|failed"}
                    },
                    "required":["rollback_id"]
                }
            }
        }
