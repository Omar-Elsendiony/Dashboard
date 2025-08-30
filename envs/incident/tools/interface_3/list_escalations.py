import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class ListEscalations(Tool):
    @staticmethod
    def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None
        # Support "Z" suffix
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        escalation_id: str = None,
        incident_id: str = None,
        escalated_by_id: str = None,
        escalated_to_id: str = None,
        escalation_reason: str = None,   # sla_breach|severity_increase|resource_unavailable|executive_request|client_demand
        escalation_level: str = None,    # technical|management|executive|vendor
        status: str = None,              # open|acknowledged|resolved
        escalated_at_from: str = None,   # ISO 8601
        escalated_at_to: str = None,     # ISO 8601
        acknowledged: Optional[bool] = None,  # True -> acknowledged_at not null; False -> null
        resolved: Optional[bool] = None,      # True -> resolved_at not null; False -> null
        created_at_from: str = None,     # ISO 8601
        created_at_to: str = None        # ISO 8601
    ) -> str:
        try:
            escalations: Dict[str, Any] = data.get("escalations", {})
            results: List[Dict[str, Any]] = []

            esc_from = ListEscalations._parse_iso(escalated_at_from) if escalated_at_from else None
            esc_to = ListEscalations._parse_iso(escalated_at_to) if escalated_at_to else None
            crt_from = ListEscalations._parse_iso(created_at_from) if created_at_from else None
            crt_to = ListEscalations._parse_iso(created_at_to) if created_at_to else None

            for e in escalations.values():
                if escalation_id and e.get("escalation_id") != escalation_id:
                    continue
                if incident_id and e.get("incident_id") != incident_id:
                    continue
                if escalated_by_id and e.get("escalated_by_id") != escalated_by_id:
                    continue
                if escalated_to_id and e.get("escalated_to_id") != escalated_to_id:
                    continue
                if escalation_reason and e.get("escalation_reason") != escalation_reason:
                    continue
                if escalation_level and e.get("escalation_level") != escalation_level:
                    continue
                if status and e.get("status") != status:
                    continue

                # Time window: escalated_at
                if esc_from or esc_to:
                    esc_at_raw = e.get("escalated_at")
                    if not esc_at_raw:
                        continue
                    try:
                        esc_at = ListEscalations._parse_iso(esc_at_raw)
                    except Exception:
                        continue
                    if esc_from and esc_at < esc_from:
                        continue
                    if esc_to and esc_at > esc_to:
                        continue

                # acknowledged filter
                if acknowledged is not None:
                    has_ack = bool(e.get("acknowledged_at"))
                    if acknowledged is True and not has_ack:
                        continue
                    if acknowledged is False and has_ack:
                        continue

                # resolved filter
                if resolved is not None:
                    has_res = bool(e.get("resolved_at"))
                    if resolved is True and not has_res:
                        continue
                    if resolved is False and has_res:
                        continue

                # Time window: created_at
                if crt_from or crt_to:
                    ca_raw = e.get("created_at")
                    if not ca_raw:
                        continue
                    try:
                        ca = ListEscalations._parse_iso(ca_raw)
                    except Exception:
                        continue
                    if crt_from and ca < crt_from:
                        continue
                    if crt_to and ca > crt_to:
                        continue

                results.append(e)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_escalations",
                "description": "Unified get/list for escalations with rich filtering on identifiers, enums, and time windows.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "escalation_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "escalated_by_id": {"type": "string"},
                        "escalated_to_id": {"type": "string"},
                        "escalation_reason": {"type": "string", "description": "sla_breach|severity_increase|resource_unavailable|executive_request|client_demand"},
                        "escalation_level": {"type": "string", "description": "technical|management|executive|vendor"},
                        "status": {"type": "string", "description": "open|acknowledged|resolved"},
                        "escalated_at_from": {"type": "string", "description": "ISO 8601 lower bound"},
                        "escalated_at_to": {"type": "string", "description": "ISO 8601 upper bound"},
                        "acknowledged": {"type": "boolean", "description": "True => acknowledged_at not null; False => null"},
                        "resolved": {"type": "boolean", "description": "True => resolved_at not null; False => null"},
                        "created_at_from": {"type": "string", "description": "ISO 8601 lower bound on created_at"},
                        "created_at_to": {"type": "string", "description": "ISO 8601 upper bound on created_at"}
                    },
                    "required": []
                }
            }
        }
