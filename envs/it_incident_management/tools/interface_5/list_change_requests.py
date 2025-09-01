import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class ListChangeRequests(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        change_id: str = None,
        incident_id: str = None,
        requested_by_id: str = None,
        change_type: str = None,
        risk_level: str = None,
        status: str = None,
        scheduled_start_from: str = None,
        scheduled_end_to: str = None
    ) -> str:
        try:
            # Helper kept inside invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            changes: Dict[str, Any] = data.get("change_requests", {})
            results: List[Dict[str, Any]] = []

            start_from_dt = parse_iso(scheduled_start_from) if scheduled_start_from else None
            end_to_dt = parse_iso(scheduled_end_to) if scheduled_end_to else None

            for cr in changes.values():
                if change_id and cr.get("change_id") != change_id:
                    continue
                if incident_id and cr.get("incident_id") != incident_id:
                    continue
                if requested_by_id and cr.get("requested_by_id") != requested_by_id:
                    continue
                if change_type and cr.get("change_type") != change_type:
                    continue
                if risk_level and cr.get("risk_level") != risk_level:
                    continue
                if status and cr.get("status") != status:
                    continue

                # time bounds
                if start_from_dt:
                    cr_start = cr.get("scheduled_start")
                    if not cr_start:
                        continue
                    try:
                        if parse_iso(cr_start) < start_from_dt:
                            continue
                    except Exception:
                        continue

                if end_to_dt:
                    cr_end = cr.get("scheduled_end")
                    if not cr_end:
                        continue
                    try:
                        if parse_iso(cr_end) > end_to_dt:
                            continue
                    except Exception:
                        continue

                results.append(cr)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_change_requests",
                "description": "Unified list/get for change requests with time window filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "change_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "requested_by_id": {"type": "string"},
                        "change_type": {"type": "string", "description": "emergency|standard|normal"},
                        "risk_level": {"type": "string", "description": "high|medium|low"},
                        "status": {"type": "string", "description": "requested|approved|scheduled|in_progress|completed|failed|rolled_back"},
                        "scheduled_start_from": {"type": "string", "description": "ISO lower bound on scheduled_start"},
                        "scheduled_end_to": {"type": "string", "description": "ISO upper bound on scheduled_end"}
                    },
                    "required": []
                }
            }
        }
