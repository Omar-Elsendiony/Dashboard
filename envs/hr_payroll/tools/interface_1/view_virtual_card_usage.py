import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ViewVirtualCardUsage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], virtual_card_id: str = None, user_id: str = None) -> str:
        cards = data.get("virtual_cards", {})

        # Resolve virtual_card_id if only user_id is given
        if not virtual_card_id:
            if not user_id:
                raise ValueError("Either virtual_card_id or user_id must be provided")
            for cid, card in cards.items():
                if card.get("user_id") == user_id:
                    virtual_card_id = cid
                    break
            if not virtual_card_id:
                raise ValueError("No virtual card found for the given user_id")

        card = cards.get(virtual_card_id)
        if not card:
            raise ValueError("Virtual card not found")

        # Validate if both are provided
        if user_id and card.get("user_id") != user_id:
            raise ValueError("Provided user_id does not match the virtual_card_id")

        # Simulated usage: 60% of the limit used
        usage = float(card.get("limit", 0)) * 0.6
        return json.dumps({
            "card_id": virtual_card_id,
            "user_id": card.get("user_id"),
            "provider_id": card.get("provider_id"),
            "limit": card.get("limit"),
            "currency": card.get("currency"),
            "status": card.get("status"),
            "used": round(usage, 2),
            "available": round(float(card.get("limit", 0)) - usage, 2)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "view_virtual_card_usage",
                "description": "Shows limit, usage, provider, and status of a virtual card using either virtual_card_id or user_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "virtual_card_id": {
                            "type": "string",
                            "description": "The ID of the virtual card"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID linked to the virtual card, used if virtual_card_id is not provided"
                        }
                    },
                    "required": []
                }
            }
        }
