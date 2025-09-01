import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class RetrieveCommunications(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        communication_id: str = None,
        incident_id: str = None,
        sender_id: str = None,
        recipient_id: str = None,
        recipient_type: str = None,
        communication_type: str = None,
        delivery_status: str = None,
        sent_since: str = None
    ) -> str:
        try:
            # Helper kept inside invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            comms: Dict[str, Any] = data.get("communications", {})
            results: List[Dict[str, Any]] = []

            since_dt = parse_iso(sent_since) if sent_since else None

            for c in comms.values():
                if communication_id and c.get("communication_id") != communication_id:
                    continue
                if incident_id and c.get("incident_id") != incident_id:
                    continue
                if sender_id and c.get("sender_id") != sender_id:
                    continue
                if recipient_id and c.get("recipient_id") != recipient_id:
                    continue
                if recipient_type and c.get("recipient_type") != recipient_type:
                    continue
                if communication_type and c.get("communication_type") != communication_type:
                    continue
                if delivery_status and c.get("delivery_status") != delivery_status:
                    continue

                if since_dt:
                    sent_at = c.get("sent_at")
                    if not sent_at:
                        continue
                    try:
                        sent_dt = parse_iso(sent_at)
                        if sent_dt is None or sent_dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(c)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_communications",
                "description": "Unified list/get for communications with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "communication_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "sender_id": {"type": "string"},
                        "recipient_id": {"type": "string"},
                        "recipient_type": {"type": "string", "description": "client|internal_team|executive|vendor|regulatory"},
                        "communication_type": {"type": "string", "description": "email|sms|phone_call|status_page|portal_update"},
                        "delivery_status": {"type": "string", "description": "sent|delivered|failed|pending"},
                        "sent_since": {"type": "string", "description": "ISO timestamp"}
                    },
                    "required": []
                }
            }
        }
