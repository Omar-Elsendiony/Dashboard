import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class QueryPostIncidentReviews(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        pir_id: str = None,
        incident_id: str = None,
        facilitator_id: str = None,
        status: str = None,            # scheduled|completed|cancelled
        scheduled_from: str = None,    # ISO
        scheduled_to: str = None       # ISO
    ) -> str:
        try:
            # Helper inside invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            pirs: Dict[str, Any] = data.get("post_incident_reviews", {})
            results: List[Dict[str, Any]] = []

            from_dt = parse_iso(scheduled_from) if scheduled_from else None
            to_dt = parse_iso(scheduled_to) if scheduled_to else None

            for p in pirs.values():
                if pir_id and p.get("pir_id") != pir_id:
                    continue
                if incident_id and p.get("incident_id") != incident_id:
                    continue
                if facilitator_id and p.get("facilitator_id") != facilitator_id:
                    continue
                if status and p.get("status") != status:
                    continue

                if from_dt or to_dt:
                    sched = p.get("scheduled_date")
                    if not sched:
                        continue
                    try:
                        sched_dt = parse_iso(sched)
                        if sched_dt is None:
                            continue
                    except Exception:
                        continue
                    if from_dt and sched_dt < from_dt:
                        continue
                    if to_dt and sched_dt > to_dt:
                        continue

                results.append(p)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return  {
            "type": "function",
            "function": {
                "name": "query_post_incident_reviews",
                "description": "Unified get/list for post-incident reviews with time filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pir_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "facilitator_id": {"type": "string"},
                        "status": {"type": "string", "description": "scheduled|completed|cancelled"},
                        "scheduled_from": {"type": "string", "description": "ISO lower bound on scheduled_date"},
                        "scheduled_to": {"type": "string", "description": "ISO upper bound on scheduled_date"}
                    },
                    "required": []
                }
            }
        }
