import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUsersByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        users = data.get("users", {})
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find users by status
        matching_users = []
        for user_id, user in users.items():
            if user.get("status") == status:
                matching_users.append(user)
        
        return json.dumps(matching_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users_by_status",
                "description": "Get all users with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Status to filter by (active, inactive, suspended)"}
                    },
                    "required": ["status"]
                }
            }
        }
