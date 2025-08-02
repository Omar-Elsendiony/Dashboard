import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateUserStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int, status: str) -> str:
        users = data.get("users", {})
        user = users.get(str(user_id))
        if not user:
            raise ValueError("User not found")
        
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        user["status"] = status
        # set_updated_at("users", user_id, data)
        user["updated_at"] = None
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_status",
                "description": "Update user status (active/inactive/suspended)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "ID of the user"},
                        "status": {"type": "string", "description": "New status for the user"}
                    },
                    "required": ["user_id", "status"]
                }
            }
        }
