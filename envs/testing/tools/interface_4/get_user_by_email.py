import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        users = data.get("users", {})
        
        # Find user by email
        for user_id, user in users.items():
            if user.get("email") == email:
                return json.dumps(user)
        
        return json.dumps({"error": f"User with email '{email}' not found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_by_email",
                "description": "Get a user record by email address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Email address of the user to retrieve"}
                    },
                    "required": ["email"]
                }
            }
        }
