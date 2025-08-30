import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateCommunication(Tool):
    @staticmethod
    def _is_iso(ts: str) -> bool:
        try:
            datetime.fromisoformat(ts.replace("Z","+00:00"))
            return True
        except Exception:
            return False

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        communication_id: str,
        incident_id: str = None,
        sender_id: str = None,
        recipient_id: str = None,
        recipient_type: str = None,     # client|internal_team|executive|vendor|regulatory
        communication_type: str = None, # email|sms|phone_call|status_page|portal_update
        sent_at: str = None,
        delivery_status: str = None     # sent|delivered|failed|pending
    ) -> str:
        try:
            comms = data.get("communications", {})
            if communication_id not in comms:
                return json.dumps({"success": False, "error": f"Communication {communication_id} not found"})

            valid_recipient = {"client","internal_team","executive","vendor","regulatory"}
            valid_comm_type = {"email","sms","phone_call","status_page","portal_update"}
            valid_delivery = {"sent","delivered","failed","pending"}

            if recipient_type and recipient_type not in valid_recipient:
                return json.dumps({"success": False, "error": f"Invalid recipient_type. Must be one of {sorted(valid_recipient)}"})
            if communication_type and communication_type not in valid_comm_type:
                return json.dumps({"success": False, "error": f"Invalid communication_type. Must be one of {sorted(valid_comm_type)}"})
            if delivery_status and delivery_status not in valid_delivery:
                return json.dumps({"success": False, "error": f"Invalid delivery_status. Must be one of {sorted(valid_delivery)}"})
            if sent_at is not None and not UpdateCommunication._is_iso(sent_at):
                return json.dumps({"success": False, "error": "sent_at must be ISO timestamp"})

            c = comms[communication_id]
            if incident_id is not None: c["incident_id"] = incident_id
            if sender_id is not None: c["sender_id"] = sender_id
            if recipient_id is not None: c["recipient_id"] = recipient_id
            if recipient_type is not None: c["recipient_type"] = recipient_type
            if communication_type is not None: c["communication_type"] = communication_type
            if sent_at is not None: c["sent_at"] = sent_at
            if delivery_status is not None: c["delivery_status"] = delivery_status

            # No updated_at
            return json.dumps(c)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
    
    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_communication",
                "description":"Update a communication record; validates enums/timestamp",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "communication_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "sender_id":{"type":"string"},
                        "recipient_id":{"type":"string"},
                        "recipient_type":{"type":"string","description":"client|internal_team|executive|vendor|regulatory"},
                        "communication_type":{"type":"string","description":"email|sms|phone_call|status_page|portal_update"},
                        "sent_at":{"type":"string","description":"ISO timestamp"},
                        "delivery_status":{"type":"string","description":"sent|delivered|failed|pending"}
                    },
                    "required":["communication_id"]
                }
            }
        }
