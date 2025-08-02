
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateVirtualCardLimit(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], card_id: str, new_limit: float) -> str:
        cards = data.get("virtual_cards", {})
        card = cards.get(card_id)

        if not card:
            raise ValueError("Card not found")
        if card.get("status") in ["revoked", "expired", "blocked"]:
            raise ValueError("Card cannot be modified in current status")
        if new_limit <= 0 or new_limit > 100000:
            raise ValueError("Limit must be between 1 and 100000")

        card["limit"] = round(new_limit, 2)
        return json.dumps({"card_id": card_id, "new_limit": new_limit})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_virtual_card_limit",
                "description": "Modifies spending limit of a virtual card",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "card_id": {"type": "string"},
                        "new_limit": {"type": "number"}
                    },
                    "required": ["card_id", "new_limit"]
                }
            }
        }
