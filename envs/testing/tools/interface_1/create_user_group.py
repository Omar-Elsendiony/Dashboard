import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateUserGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_name: str, requesting_user_id: str,
               group_description: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        user = users[str(requesting_user_id)]
        
        # Check authority - only Platform Owner can create user groups
        if user.get("role") != "PlatformOwner":
            return json.dumps({"error": "Only Platform Owner can create user groups"})
        
        # Check if group name already exists
        for group in groups.values():
            if group.get("name").lower() == group_name.lower():
                return json.dumps({"error": f"Group with name '{group_name}' already exists"})
        
        # Create group
        group_id = generate_id(groups)
        timestamp = "2025-10-01T00:00:00"
        
        new_group = {
            "group_id": group_id,
            "name": group_name,
            "description": group_description,
            "type": "custom",
            "created_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        groups[str(group_id)] = new_group
        
        return json.dumps({"group_id": str(group_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user_group",
                "description": "Create a new user group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_name": {"type": "string", "description": "Name of the user group"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the group"},
                        "group_description": {"type": "string", "description": "Description of the group"},
                    },
                    "required": ["group_name", "requesting_user_id"]
                }
            }
        }
