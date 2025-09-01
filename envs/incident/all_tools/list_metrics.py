import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class ListMetrics(Tool):
    @staticmethod
    def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        metric_id: str = None,
        incident_id: str = None,
        metric_type: str = None,   # MTTA|MTTD|MTTR|MTTM|FTR
        recorded_since: str = None,
        recorded_until: str = None
    ) -> str:
        try:
            metrics: Dict[str, Any] = data.get("metrics", {})
            results: List[Dict[str, Any]] = []

            since_dt = ListMetrics._parse_iso(recorded_since) if recorded_since else None
            until_dt = ListMetrics._parse_iso(recorded_until) if recorded_until else None

            for m in metrics.values():
                if metric_id and m.get("metric_id") != metric_id:
                    continue
                if incident_id and m.get("incident_id") != incident_id:
                    continue
                if metric_type and m.get("metric_type") != metric_type:
                    continue

                if since_dt or until_dt:
                    ra = m.get("recorded_at")
                    if not ra:
                        continue
                    try:
                        ra_dt = ListMetrics._parse_iso(ra)
                    except Exception:
                        continue
                    if since_dt and ra_dt < since_dt:
                        continue
                    if until_dt and ra_dt > until_dt:
                        continue

                results.append(m)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_metrics",
                "description": "Unified get/list for metrics with optional filters and time bounds",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "metric_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "metric_type": {"type": "string", "description": "MTTA|MTTD|MTTR|MTTM|FTR"},
                        "recorded_since": {"type": "string", "description": "ISO timestamp lower bound"},
                        "recorded_until": {"type": "string", "description": "ISO timestamp upper bound"}
                    },
                    "required": []
                }
            }
        }
