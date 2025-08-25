
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        if user_id not in users:
            raise ValueError("User not found")
        user = users[user_id]
        return json.dumps({
            "user_id": user_id,
            "role": user.get("role"),
            "locale": user.get("locale"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "email": user.get("email"),
            "timezone": user.get("timezone"),
            "status": user.get("status")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_profile",
                "description": "Retrieves user metadata (first name, last name, role, locale, email, timezone, status)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        }
