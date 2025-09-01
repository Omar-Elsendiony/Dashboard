import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LogCommunication(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        sender_id: str,
        recipient_type: str,
        communication_type: str,
        recipient_id: str = None,
        delivery_status: str = "sent"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            communications = data.setdefault("communications", {})

            valid_recipient_types = {"client","internal_team","executive","vendor","regulatory"}
            if recipient_type not in valid_recipient_types:
                return json.dumps({"success": False, "error": f"Invalid recipient_type. Must be one of {sorted(valid_recipient_types)}"})

            valid_comm_types = {"email","sms","phone_call","status_page","portal_update"}
            if communication_type not in valid_comm_types:
                return json.dumps({"success": False, "error": f"Invalid communication_type. Must be one of {sorted(valid_comm_types)}"})

            valid_delivery = {"sent","delivered","failed","pending"}
            if delivery_status not in valid_delivery:
                return json.dumps({"success": False, "error": f"Invalid delivery_status. Must be one of {sorted(valid_delivery)}"})

            communication_id = generate_id(communications)
            timestamp = "2025-10-01T00:00:00"

            new_comm = {
                "communication_id": communication_id,
                "incident_id": incident_id,
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "recipient_type": recipient_type,
                "communication_type": communication_type,
                "sent_at": timestamp,           # NOW surrogate
                "delivery_status": delivery_status,
                "created_at": timestamp
            }

            communications[communication_id] = new_comm
            return json.dumps({"communication_id": communication_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_communication",
                "description": "Create a communication entry for an incident; sets sent_at and created_at",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "sender_id": {"type": "string"},
                        "recipient_type": {"type": "string", "description": "client|internal_team|executive|vendor|regulatory"},
                        "communication_type": {"type": "string", "description": "email|sms|phone_call|status_page|portal_update"},
                        "recipient_id": {"type": "string"},
                        "delivery_status": {"type": "string", "description": "sent|delivered|failed|pending (default sent)"}
                    },
                    "required": ["incident_id","sender_id","recipient_type","communication_type"]
                }
            }
        }
