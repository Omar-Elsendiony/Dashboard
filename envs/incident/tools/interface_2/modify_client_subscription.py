import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class ModifyClientSubscription(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        subscription_id: str,
        client_id: str = None,
        product_id: str = None,
        subscription_type: str = None,  # full_service|limited_service|trial|custom
        sla_tier: str = None,           # premium|standard|basic
        rto_hours: int = None,
        start_date: str = None,         # ISO date
        end_date: str = None,           # ISO date
        status: str = None              # active|expired|cancelled|suspended
    ) -> str:
        try:
            # Helper kept inside invoke per requirement
            def is_iso_date(d: str) -> bool:
                try:
                    datetime.fromisoformat(d)
                    return True
                except Exception:
                    return False

            subs = data.get("client_subscriptions", {})
            if subscription_id not in subs:
                return json.dumps({"success": False, "error": f"Subscription {subscription_id} not found"})

            valid_type = {"full_service","limited_service","trial","custom"}
            valid_tier = {"premium","standard","basic"}
            valid_status = {"active","expired","cancelled","suspended"}

            if subscription_type and subscription_type not in valid_type:
                return json.dumps({"success": False, "error": f"Invalid subscription_type. Must be one of {sorted(valid_type)}"})
            if sla_tier and sla_tier not in valid_tier:
                return json.dumps({"success": False, "error": f"Invalid sla_tier. Must be one of {sorted(valid_tier)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if rto_hours is not None and rto_hours < 0:
                return json.dumps({"success": False, "error": "rto_hours must be non-negative"})
            if start_date is not None and not is_iso_date(start_date):
                return json.dumps({"success": False, "error": "start_date must be an ISO date (e.g., 2025-09-01)"})
            if end_date is not None and not is_iso_date(end_date):
                return json.dumps({"success": False, "error": "end_date must be an ISO date (e.g., 2025-09-30)"})

            s = subs[subscription_id]
            if client_id is not None: s["client_id"] = client_id
            if product_id is not None: s["product_id"] = product_id
            if subscription_type is not None: s["subscription_type"] = subscription_type
            if sla_tier is not None: s["sla_tier"] = sla_tier
            if rto_hours is not None: s["rto_hours"] = rto_hours
            if start_date is not None: s["start_date"] = start_date
            if end_date is not None: s["end_date"] = end_date
            if status is not None: s["status"] = status

            s["updated_at"] = "2025-09-02T23:59:59"
            return json.dumps(s)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_client_subscription",
                "description": "Update a client subscription; validates enums/dates; sets updated_at. Date format: ISO date YYYY-MM-DD (e.g., 2025-09-01).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string"},
                        "client_id": {"type": "string"},
                        "product_id": {"type": "string"},
                        "subscription_type": {"type": "string", "description": "full_service|limited_service|trial|custom"},
                        "sla_tier": {"type": "string", "description": "premium|standard|basic"},
                        "rto_hours": {"type": "integer"},
                        "start_date": {"type": "string", "description": "ISO date YYYY-MM-DD (e.g., 2025-09-01)"},
                        "end_date": {"type": "string", "description": "ISO date YYYY-MM-DD (e.g., 2025-09-30)"},
                        "status": {"type": "string", "description": "active|expired|cancelled|suspended"}
                    },
                    "required": ["subscription_id"]
                }
            }
        }
