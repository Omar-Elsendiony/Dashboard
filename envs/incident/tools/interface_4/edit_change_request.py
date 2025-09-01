import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class EditChangeRequest(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        change_id: str,
        incident_id: str = None,
        title: str = None,
        change_type: str = None,     # emergency|standard|normal
        requested_by_id: str = None,
        approved_by_id: str = None,
        risk_level: str = None,      # high|medium|low
        scheduled_start: str = None,
        scheduled_end: str = None,
        actual_start: str = None,
        actual_end: str = None,
        status: str = None           # requested|approved|scheduled|in_progress|completed|failed|rolled_back
    ) -> str:
        try:
            # Helper inside invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            changes = data.get("change_requests", {})
            if change_id not in changes:
                return json.dumps({"success": False, "error": f"Change request {change_id} not found"})

            valid_change_type = {"emergency","standard","normal"}
            valid_risk = {"high","medium","low"}
            valid_status = {"requested","approved","scheduled","in_progress","completed","failed","rolled_back"}

            if change_type and change_type not in valid_change_type:
                return json.dumps({"success": False, "error": f"Invalid change_type. Must be one of {sorted(valid_change_type)}"})
            if risk_level and risk_level not in valid_risk:
                return json.dumps({"success": False, "error": f"Invalid risk_level. Must be one of {sorted(valid_risk)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            for ts in [scheduled_start, scheduled_end, actual_start, actual_end]:
                if ts is not None and not is_iso(ts):
                    return json.dumps({"success": False, "error": "All timestamp fields must be ISO format"})

            c = changes[change_id]
            if incident_id is not None: c["incident_id"] = incident_id
            if title is not None: c["title"] = title
            if change_type is not None: c["change_type"] = change_type
            if requested_by_id is not None: c["requested_by_id"] = requested_by_id
            if approved_by_id is not None: c["approved_by_id"] = approved_by_id
            if risk_level is not None: c["risk_level"] = risk_level
            if scheduled_start is not None: c["scheduled_start"] = scheduled_start
            if scheduled_end is not None: c["scheduled_end"] = scheduled_end
            if actual_start is not None: c["actual_start"] = actual_start
            if actual_end is not None: c["actual_end"] = actual_end
            if status is not None: c["status"] = status

            return json.dumps(c)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"edit_change_request",
                "description":"Update a change request; validates enums/timestamps",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "change_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "title":{"type":"string"},
                        "change_type":{"type":"string","description":"emergency|standard|normal"},
                        "requested_by_id":{"type":"string"},
                        "approved_by_id":{"type":"string"},
                        "risk_level":{"type":"string","description":"high|medium|low"},
                        "scheduled_start":{"type":"string","description":"ISO timestamp"},
                        "scheduled_end":{"type":"string","description":"ISO timestamp"},
                        "actual_start":{"type":"string","description":"ISO timestamp"},
                        "actual_end":{"type":"string","description":"ISO timestamp"},
                        "status":{"type":"string","description":"requested|approved|scheduled|in_progress|completed|failed|rolled_back"}
                    },
                    "required":["change_id"]
                }
            }
        }
