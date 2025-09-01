import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddClientSubscription(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        client_id: str,
        product_id: str,
        subscription_type: str,
        sla_tier: str,
        rto_hours: int,
        start_date: str,
        end_date: str = None,
        status: str = "active"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            subscriptions = data.setdefault("client_subscriptions", {})

            valid_types = ["full_service","limited_service","trial","custom"]
            if subscription_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid subscription_type. Must be one of {valid_types}"})

            valid_tiers = ["premium","standard","basic"]
            if sla_tier not in valid_tiers:
                return json.dumps({"success": False, "error": f"Invalid sla_tier. Must be one of {valid_tiers}"})

            valid_status = ["active","expired","cancelled","suspended"]
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_status}"})

            # Basic type checks
            if not isinstance(rto_hours, int):
                return json.dumps({"success": False, "error": "rto_hours must be an integer"})

            subscription_id = generate_id(subscriptions)
            timestamp = "2025-10-01T00:00:00"

            new_sub = {
                "subscription_id": subscription_id,
                "client_id": client_id,
                "product_id": product_id,
                "subscription_type": subscription_type,
                "start_date": start_date,
                "end_date": end_date,
                "sla_tier": sla_tier,
                "rto_hours": rto_hours,
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            subscriptions[subscription_id] = new_sub
            return json.dumps({"subscription_id": subscription_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_client_subscription",
                "description": "Create a new client subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string"},
                        "product_id": {"type": "string"},
                        "subscription_type": {"type": "string", "description": "full_service|limited_service|trial|custom"},
                        "sla_tier": {"type": "string", "description": "premium|standard|basic"},
                        "rto_hours": {"type": "integer"},
                        "start_date": {"type": "string"},
                        "end_date": {"type": "string"},
                        "status": {"type": "string", "description": "active|expired|cancelled|suspended (default active)"}
                    },
                    "required": ["client_id","product_id","subscription_type","sla_tier","rto_hours","start_date"]
                }
            }
        }
