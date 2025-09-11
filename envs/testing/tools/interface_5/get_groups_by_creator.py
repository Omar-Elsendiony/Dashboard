import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupsByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        groups = data.get("groups", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find groups created by the user
        user_groups = []
        for group in groups.values():
            if group.get("created_by_user_id") == created_by_user_id:
                user_groups.append(group)
        
        return json.dumps(user_groups)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_groups_by_creator",
                "description": "Get all groups created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user to get groups for"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
