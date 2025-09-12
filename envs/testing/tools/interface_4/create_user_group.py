import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateUserGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, group_name: str,
               description: Optional[str] = None, group_type: str = "custom") -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - only Platform Owner can create groups
        if requesting_user.get("role") != "PlatformOwner":
            return json.dumps({"error": "Only Platform Owner can create user groups"})
        
        # Validate enum values
        if group_type not in ["system", "custom"]:
            return json.dumps({"error": "Invalid group_type. Must be one of: system, custom"})
        
        # Check if group name already exists
        for group in groups.values():
            if group.get("name").lower() == group_name.lower():
                return json.dumps({"error": f"Group '{group_name}' already exists"})
        
        # Create group
        group_id = generate_id(groups)
        timestamp = "2025-10-01T00:00:00"
        
        new_group = {
            "group_id": int(group_id),
            "name": group_name,
            "description": description,
            "type": group_type,
            "created_by_user_id": requesting_user_id,
            "member_count": 0,
            "created_at": timestamp
        }
        
        groups[group_id] = new_group
        
        return json.dumps({
            "group_id": group_id,
            "success": True
        })

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
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the group"},
                        "group_name": {"type": "string", "description": "Name of the group"},
                        "description": {"type": "string", "description": "Group description"},
                        "group_type": {"type": "string", "description": "Group type (system, custom)"}
                    },
                    "required": ["requesting_user_id", "group_name"]
                }
            }
        }