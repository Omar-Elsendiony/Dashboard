import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class IssueVirtualCard(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str = None,
        limit: float = None,
        currency: str = "USD",
        provider_id: str = None,
        status: str = "active",
        worker_id: str = None  # Deprecated
    ) -> str:
        if not user_id:
            # Resolve user_id if deprecated worker_id is provided
            if not worker_id:
                raise ValueError("user_id is required (worker_id is deprecated)")
            workers = data.get("workers", {})
            if worker_id not in workers:
                raise ValueError("Invalid worker_id")
            user_id = workers[worker_id].get("user_id")
            if not user_id:
                raise ValueError("Unable to resolve user_id from worker_id")

        if limit is None or limit <= 0:
            raise ValueError("Limit must be a positive number")

        cards = data.setdefault("virtual_cards", {})
        existing = [
            c for c in cards.values()
            if c.get("user_id") == user_id and c.get("status") == "active"
        ]
        if existing:
            raise ValueError("Active virtual card already exists for this user")

        # Default to first provider if not given
        if not provider_id:
            provider_id = next(iter(data.get("financial_providers", {})), None)
            if not provider_id:
                raise ValueError("No financial provider available")

        card_id = str(uuid.uuid4())
        card_data = {
            "user_id": user_id,
            "provider_id": provider_id,
            "currency": currency,
            "limit": round(limit, 2),
            "status": status
        }
        cards[card_id] = card_data

        return json.dumps({
            "card_id": card_id,
            **card_data
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "issue_virtual_card",
                "description": (
                    "Creates a virtual card for a user. "
                    "worker_id is deprecated and no longer stored in virtual_cards table. "
                    "Only one active card per user is allowed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user to whom the virtual card is issued"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Spending limit on the card"
                        },
                        "currency": {
                            "type": "string",
                            "description": "3-letter ISO currency code (e.g. USD, EUR, INR)",
                            "default": "USD"
                        },
                        "provider_id": {
                            "type": "string",
                            "description": "ID of the financial provider backing the card"
                        },
                        "status": {
                            "type": "string",
                            "description": "Card status (e.g. active, blocked, expired)",
                            "default": "active"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "(Deprecated) Used to resolve user_id if user_id not given"
                        }
                    },
                    "required": ["limit", "provider_id"]
                }
            }
        }
