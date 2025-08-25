import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListWorkersWithVirtualCards(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], organization_id: str) -> str:
        workers = data.get("workers", {})
        cards = data.get("virtual_cards", {})

        user_ids_with_cards = {card["user_id"] for card in cards.values()}

        result = [
            {**w, "worker_id": wid}
            for wid, w in workers.items()
            if w.get("user_id") in user_ids_with_cards and w.get("organization_id") == organization_id
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_workers_with_virtual_cards",
                "description": "Lists workers who have at least one virtual card in a specific organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "The ID of the organization to scope the worker search"
                        }
                    },
                    "required": ["organization_id"]
                }
            }
        }
