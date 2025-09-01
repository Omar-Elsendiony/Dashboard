import json
from typing import Any, Dict, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool

class QueryIncidents(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str = None,
        client_id: str = None,
        reporter_id: str = None,
        assigned_manager_id: str = None,
        component_id: str = None,
        status: str = None,
        severity: str = None,
        category: str = None,
        impact: str = None,
        urgency: str = None,
        rto_breach: Optional[bool] = None,
        sla_breach: Optional[bool] = None,
        is_recurring: Optional[bool] = None,
        title_contains: str = None,
        detected_since: str = None,
        detected_until: str = None,
        resolved_since: str = None,
        resolved_until: str = None,
        closed_since: str = None,
        closed_until: str = None,
        downtime_minutes_min: Optional[int] = None,
        downtime_minutes_max: Optional[int] = None
    ) -> str:
        try:
            incidents = data.get("incidents", {})
            results = []

            # Local ISO8601 parser (handles trailing 'Z')
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                s = ts.strip().replace("Z", "+00:00")
                return datetime.fromisoformat(s)

            # Pre-parse time bounds
            ds = parse_iso(detected_since)
            du = parse_iso(detected_until)
            rs = parse_iso(resolved_since)
            ru = parse_iso(resolved_until)
            cs = parse_iso(closed_since)
            cu = parse_iso(closed_until)

            def within_range(value_ts: Optional[str],
                             start: Optional[datetime],
                             end: Optional[datetime]) -> bool:
                if start is None and end is None:
                    return True
                if not value_ts:
                    return False
                try:
                    dt = parse_iso(value_ts)
                except Exception:
                    return False
                if start and dt < start:
                    return False
                if end and dt > end:
                    return False
                return True

            for inc in incidents.values():
                if incident_id and inc.get("incident_id") != incident_id:
                    continue
                if client_id and inc.get("client_id") != client_id:
                    continue
                if reporter_id and inc.get("reporter_id") != reporter_id:
                    continue
                if assigned_manager_id and inc.get("assigned_manager_id") != assigned_manager_id:
                    continue
                if component_id and inc.get("component_id") != component_id:
                    continue
                if status and inc.get("status") != status:
                    continue
                if severity and inc.get("severity") != severity:
                    continue
                if category and inc.get("category") != category:
                    continue
                if impact and inc.get("impact") != impact:
                    continue
                if urgency and inc.get("urgency") != urgency:
                    continue
                if rto_breach is not None and bool(inc.get("rto_breach")) != rto_breach:
                    continue
                if sla_breach is not None and bool(inc.get("sla_breach")) != sla_breach:
                    continue
                if is_recurring is not None and bool(inc.get("is_recurring")) != is_recurring:
                    continue
                if title_contains and title_contains.lower() not in (inc.get("title", "").lower()):
                    continue

                # Time filters (inclusive bounds)
                if not within_range(inc.get("detected_at"), ds, du):
                    continue
                if not within_range(inc.get("resolved_at"), rs, ru):
                    continue
                if not within_range(inc.get("closed_at"), cs, cu):
                    continue

                # Numeric ranges
                dm = inc.get("downtime_minutes")
                if downtime_minutes_min is not None and (dm is None or dm < downtime_minutes_min):
                    continue
                if downtime_minutes_max is not None and (dm is None or dm > downtime_minutes_max):
                    continue

                results.append(inc)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_incidents",
                "description": "Unified get/list for incidents with flexible filters and time/range queries",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "client_id": {"type": "string"},
                        "reporter_id": {"type": "string"},
                        "assigned_manager_id": {"type": "string"},
                        "component_id": {"type": "string"},
                        "status": {"type": "string", "description": "open|in_progress|resolved|closed"},
                        "severity": {"type": "string", "description": "P1|P2|P3|P4"},
                        "category": {"type": "string"},
                        "impact": {"type": "string", "description": "critical|high|medium|low"},
                        "urgency": {"type": "string", "description": "critical|high|medium|low"},
                        "rto_breach": {"type": "boolean"},
                        "sla_breach": {"type": "boolean"},
                        "is_recurring": {"type": "boolean"},
                        "title_contains": {"type": "string", "description": "Case-insensitive contains"},
                        "detected_since": {"type": "string", "description": "ISO timestamp (e.g., 2025-08-30T12:00:00)"},
                        "detected_until": {"type": "string", "description": "ISO timestamp"},
                        "resolved_since": {"type": "string", "description": "ISO timestamp"},
                        "resolved_until": {"type": "string", "description": "ISO timestamp"},
                        "closed_since": {"type": "string", "description": "ISO timestamp"},
                        "closed_until": {"type": "string", "description": "ISO timestamp"},
                        "downtime_minutes_min": {"type": "integer"},
                        "downtime_minutes_max": {"type": "integer"}
                    },
                    "required": []
                }
            }
        }
