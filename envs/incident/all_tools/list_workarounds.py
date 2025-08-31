import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class ListWorkarounds(Tool):
    @staticmethod
    def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        workaround_id: str = None,
        incident_id: str = None,
        implemented_by_id: str = None,
        effectiveness: str = None,
        status: str = None,
        implemented_since: str = None
    ) -> str:
        try:
            workarounds: Dict[str, Any] = data.get("workarounds", {})
            results: List[Dict[str, Any]] = []

            since_dt = ListWorkarounds._parse_iso(implemented_since) if implemented_since else None

            for w in workarounds.values():
                if workaround_id and w.get("workaround_id") != workaround_id:
                    continue
                if incident_id and w.get("incident_id") != incident_id:
                    continue
                if implemented_by_id and w.get("implemented_by_id") != implemented_by_id:
                    continue
                if effectiveness and w.get("effectiveness") != effectiveness:
                    continue
                if status and w.get("status") != status:
                    continue

                if since_dt:
                    ts = w.get("implemented_at")
                    if not ts:
                        continue
                    try:
                        dt = ListWorkarounds._parse_iso(ts)
                        if dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(w)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_workarounds",
                "description": "Unified list/get for incident workarounds with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "workaround_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "implemented_by_id": {"type": "string"},
                        "effectiveness": {"type": "string", "description": "complete|partial|minimal"},
                        "status": {"type": "string", "description": "active|inactive|replaced"},
                        "implemented_since": {"type": "string", "description": "ISO timestamp"}
                    },
                    "required": []
                }
            }
        }
