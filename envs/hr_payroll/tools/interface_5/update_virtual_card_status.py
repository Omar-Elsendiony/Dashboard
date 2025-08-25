
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateVirtualCardStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], card_id: str, status: str) -> str:
        cards = data.get("virtual_cards", {})
        card = cards.get(card_id)
        if not card:
            raise ValueError("Card not found")
        if card["status"] == "revoked":
            raise ValueError("Cannot change status of revoked card")

        card["status"] = status
        return json.dumps({"card_id": card_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_virtual_card_status",
                "description": "Updates status of a virtual card to frozen or active",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "card_id": {
                            "type": "string",
                            "description": "ID of the virtual card"
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (e.g., 'active', 'blocked')"
                        }
                    },
                    "required": ["card_id", "status"]
                }
            }
        }
