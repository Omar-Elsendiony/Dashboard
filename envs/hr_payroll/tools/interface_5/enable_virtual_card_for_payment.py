
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EnableVirtualCardForPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], card_id: str) -> str:
        cards = data.get("virtual_cards", {})
        card = cards.get(card_id)
        if not card:
            raise ValueError("Card not found")
        if card["status"] not in ["blocked", "expired"]:
            raise ValueError("Card must be in blocked or expired state to be re-enabled")
        card["status"] = "active"
        return json.dumps({"card_id": card_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "enable_virtual_card_for_payment",
                "description": "Re-enables a previously blocked or expired virtual card for payment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "card_id": {
                            "type": "string",
                            "description": "ID of the virtual card to be re-enabled"
                        }
                    },
                    "required": ["card_id"]
                }
            }
        }
