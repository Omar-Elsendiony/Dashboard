
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListVirtualCardsByOrg(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], org_id: str) -> str:
        workers = data.get("workers", {})
        user_ids = {w["user_id"] for w in workers.values() if w["organization_id"] == org_id}
        cards = data.get("virtual_cards", {})
        results = [
            {**c, "card_id": cid}
            for cid, c in cards.items()
            if c.get("user_id") in user_ids
        ]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_virtual_cards_by_org",
                "description": "Lists all virtual cards issued under an organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "org_id": {
                            "type": "string",
                            "description": "The organization ID to search virtual cards under"
                        }
                    },
                    "required": ["org_id"]
                }
            }
        }
