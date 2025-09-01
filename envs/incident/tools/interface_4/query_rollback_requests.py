import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class QueryRollbackRequests(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        rollback_id: str = None,
        change_id: str = None,
        incident_id: str = None,
        requested_by_id: str = None,
        status: str = None,
        executed_since: str = None
    ) -> str:
        try:
            # Helper inside invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            rollbacks: Dict[str, Any] = data.get("rollback_requests", {})
            results: List[Dict[str, Any]] = []

            since_dt = parse_iso(executed_since) if executed_since else None

            for rb in rollbacks.values():
                if rollback_id and rb.get("rollback_id") != rollback_id:
                    continue
                if change_id and rb.get("change_id") != change_id:
                    continue
                if incident_id and rb.get("incident_id") != incident_id:
                    continue
                if requested_by_id and rb.get("requested_by_id") != requested_by_id:
                    continue
                if status and rb.get("status") != status:
                    continue

                if since_dt:
                    ex = rb.get("executed_at")
                    if not ex:
                        continue
                    try:
                        ex_dt = parse_iso(ex)
                        if ex_dt is None or ex_dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(rb)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_rollback_requests",
                "description": "Unified list/get for rollback requests with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "rollback_id": {"type": "string"},
                        "change_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "requested_by_id": {"type": "string"},
                        "status": {"type": "string", "description": "requested|approved|in_progress|completed|failed"},
                        "executed_since": {"type": "string", "description": "ISO timestamp lower bound"}
                    },
                    "required": []
                }
            }
        }
