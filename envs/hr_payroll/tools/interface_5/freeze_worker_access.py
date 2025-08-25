
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FreezeWorkerAccess(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        user_id = workers[worker_id]["user_id"]
        data["users"][user_id]["status"] = "suspended"

        # freeze cards
        for card in data.get("virtual_cards", {}).values():
            if card["user_id"] == user_id and card["status"] == "active":
                card["status"] = "blocked"

        return json.dumps({"worker_id": worker_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "freeze_worker_access",
                "description": "Freezes system and financial access for a worker by suspending user and blocking cards",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID whose access is to be frozen"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
