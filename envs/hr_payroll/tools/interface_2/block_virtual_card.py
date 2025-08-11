
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class BlockVirtualCard(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], card_id: str) -> str:
        cards = data.get("virtual_cards", {})
        if card_id not in cards:
            raise ValueError("Card not found")

        card = cards[card_id]
        if card.get("status") in ["revoked", "expired", "blocked"]:
            raise ValueError("Card cannot be blocked in current status")

        card["status"] = "blocked"
        return json.dumps({"card_id": card_id, "status": "blocked"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "block_virtual_card",
                "description": "Blocks a virtual card to block spending",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "card_id": {
                            "type": "string",
                            "description": "The ID of the virtual card to block"
                        }
                    },
                    "required": ["card_id"]
                }
            }
        }
