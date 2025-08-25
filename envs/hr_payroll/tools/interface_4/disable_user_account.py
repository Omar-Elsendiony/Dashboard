
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DisableUserAccount(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        if user_id not in users:
            raise ValueError("User not found")

        users[user_id]["status"] = "inactive"
        return json.dumps({"user_id": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "disable_user_account",
                "description": "Disables a user from accessing the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user to disable"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
