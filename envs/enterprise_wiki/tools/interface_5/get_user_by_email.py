import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        users = data.get("users", {})
        
        for user_id, user in users.items():
            if user.get("email") == email:
                return json.dumps(user)
        
        raise ValueError("User not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_by_email",
                "description": "Get user information by email",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "The email address of the user"
                        }
                    },
                    "required": ["email"]
                }
            }
        }
