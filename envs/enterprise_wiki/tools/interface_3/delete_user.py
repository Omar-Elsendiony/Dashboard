import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
        users = data.get("users", {})
        removed = users.pop(str(user_id), None)
        if not removed:
            raise ValueError("User not found.")
        return json.dumps(removed)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_user",
                "description": "Delete a user by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer"}
                    },
                    "required": ["user_id"]
                }
            }
        }
