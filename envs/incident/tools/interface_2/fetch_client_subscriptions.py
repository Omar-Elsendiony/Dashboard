import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class FetchClientSubscriptions(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        subscription_id: str = None,
        client_id: str = None,
        product_id: str = None,
        subscription_type: str = None,
        sla_tier: str = None,
        status: str = None,
        start_date_from: str = None,  # YYYY-MM-DD
        start_date_to: str = None     # YYYY-MM-DD
    ) -> str:
        subs = data.get("client_subscriptions", {})
        results = []

        # Local, strict YYYY-MM-DD parser (no ISO datetimes)
        def parse_ymd(s: str):
            try:
                return datetime.strptime(s.strip(), "%Y-%m-%d").date()
            except Exception:
                raise ValueError(f"Expected YYYY-MM-DD, got {s!r}")

        # Pre-parse bounds (strict format)
        try:
            start_from = parse_ymd(start_date_from) if start_date_from else None
            start_to   = parse_ymd(start_date_to) if start_date_to else None
        except ValueError as e:
            return json.dumps({"error": str(e)})

        if start_from and start_to and start_from > start_to:
            return json.dumps({"error": "start_date_from must be <= start_date_to"})

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

            # Apply start_date range if provided (inclusive)
            if start_from or start_to:
                sub_start_str = sub.get("start_date")
                if not isinstance(sub_start_str, str):
                    continue
                try:
                    sub_start = parse_ymd(sub_start_str)
                except ValueError:
                    # Skip malformed start_date entries
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
                "name": "fetch_client_subscriptions",
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
                        "start_date_from": {"type": "string", "description": "YYYY-MM-DD (inclusive lower bound)"},
                        "start_date_to": {"type": "string", "description": "YYYY-MM-DD (inclusive upper bound)"}
                    },
                    "required": []
                }
            }
        }
