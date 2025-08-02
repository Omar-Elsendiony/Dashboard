
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AssignRoleToUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, role: str) -> str:
        users = data.get("users", {})
        user = users.get(user_id)
        if not user:
            raise ValueError("User not found")
        if user.get("role") == role:
            return json.dumps({"user_id": user_id})  # No change needed
        user["role"] = role
        return json.dumps({"user_id": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_role_to_user",
                "description": "Assigns a new role to a user if not already assigned",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user"
                        },
                        "role": {
                            "type": "string",
                            "description": "Role to assign (admin, hr_manager, etc.)"
                        }
                    },
                    "required": ["user_id", "role"]
                }
            }
        }
