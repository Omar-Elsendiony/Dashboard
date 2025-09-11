import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUsersByRole(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], role: str) -> str:
        users = data.get("users", {})
        
        # Validate role
        valid_roles = ["PlatformOwner", "WikiProgramManager", "User"]
        if role not in valid_roles:
            return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}"})
        
        # Find users by role
        matching_users = []
        for user_id, user in users.items():
            if user.get("role") == role:
                matching_users.append(user)
        
        return json.dumps(matching_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users_by_role",
                "description": "Get all users with a specific role",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "description": "Role to filter by (PlatformOwner, WikiProgramManager, User)"}
                    },
                    "required": ["role"]
                }
            }
        }
