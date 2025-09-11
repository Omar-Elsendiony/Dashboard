import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserByUsername(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], username: str) -> str:
        users = data.get("users", {})
        
        # Find user by username
        for user_id, user in users.items():
            if user.get("username") == username:
                return json.dumps(user)
        
        return json.dumps({"error": f"User with username '{username}' not found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_by_username",
                "description": "Get a user record by username",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "Username of the user to retrieve"}
                    },
                    "required": ["username"]
                }
            }
        }
