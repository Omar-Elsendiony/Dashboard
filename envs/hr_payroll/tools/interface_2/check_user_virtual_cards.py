import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckUserVirtualCards(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        limit: float = None,
        provider_id: str = None
    ) -> str:
        cards = data.get("virtual_cards", {})

        result = [
            {**card, "card_id": cid}
            for cid, card in cards.items()
            if card.get("user_id") == user_id
            and (limit is None or card.get("limit") == round(limit, 2))
            and (provider_id is None or card.get("provider_id") == provider_id)
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_user_virtual_cards",
                "description": (
                    "Returns the virtual cards owned by the user, "
                    "optionally filtered by exact limit or provider ID."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose virtual cards are being queried"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Optional filter for the card's exact limit"
                        },
                        "provider_id": {
                            "type": "string",
                            "description": "Optional filter for the card's provider ID"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
