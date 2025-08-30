import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class ListClientSubscriptions(Tool):
    @staticmethod
    def _parse_date(s: str):
        return datetime.strptime(s, "%Y-%m-%d").date()

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        subscription_id: str = None,
        client_id: str = None,
        product_id: str = None,
        subscription_type: str = None,
        sla_tier: str = None,
        status: str = None,
        start_date_from: str = None,
        start_date_to: str = None
    ) -> str:
        subs = data.get("client_subscriptions", {})
        results = []

        # Pre-parse dates if supplied
        try:
            start_from = ListClientSubscriptions._parse_date(start_date_from) if start_date_from else None
            start_to   = ListClientSubscriptions._parse_date(start_date_to) if start_date_to else None
        except Exception as e:
            return json.dumps({"error": f"Invalid date format: {e}"})

        for sub in subs.values():
            if subscription_id and sub.get("subscription_id") != subscription_id:
                continue
            if client_id and sub.get("client_id") != client_id:
                continue
            if product_id and sub.get("product_id") != product_id:
                continue
            if subscription_type and sub.get("subscription_type") != subscription_type:
                continue
            if sla_tier and sub.get("sla_tier") != sla_tier:
                continue
            if status and sub.get("status") != status:
                continue

            if start_from or start_to:
                try:
                    sub_start = ListClientSubscriptions._parse_date(sub.get("start_date"))
                except Exception:
                    # If stored value is malformed, exclude from results
                    continue
                if start_from and sub_start < start_from:
                    continue
                if start_to and sub_start > start_to:
                    continue

            results.append(sub)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_client_subscriptions",
                "description": "Unified get/list for client subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string"},
                        "client_id": {"type": "string"},
                        "product_id": {"type": "string"},
                        "subscription_type": {"type": "string", "description": "full_service|limited_service|trial|custom"},
                        "sla_tier": {"type": "string", "description": "premium|standard|basic"},
                        "status": {"type": "string", "description": "active|expired|cancelled|suspended"},
                        "start_date_from": {"type": "string", "description": "YYYY-MM-DD"},
                        "start_date_to": {"type": "string", "description": "YYYY-MM-DD"}
                    },
                    "required": []
                }
            }
        }
