import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddUserToGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str, target_user_id: str, requesting_user_id: str,
               space_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        user_groups = data.get("user_groups", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate entities exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        if str(target_user_id) not in users:
            return json.dumps({"error": f"Target user {target_user_id} not found"})
        
        if str(group_id) not in groups:
            return json.dumps({"error": f"Group {group_id} not found"})
        
        user = users[str(requesting_user_id)]
        
        # Check if user is already in group
        for ug in user_groups.values():
            if ug.get("user_id") == target_user_id and ug.get("group_id") == group_id:
                return json.dumps({"error": "User is already in the group"})
        
        # Check authority
        has_authority = False
        
        # Platform Owner can add any user to any group
        if user.get("role") == "PlatformOwner":
            has_authority = True
        
        # Wiki Program Manager can add users to groups
        elif user.get("role") == "WikiProgramManager":
            has_authority = True
        
        # Space Administrator can add users to groups in their space
        elif space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "moderate"):
                    has_authority = True
                    break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to add user to group"})
        
        # Add user to group
        user_group_id = generate_id(user_groups)
        timestamp = "2025-10-01T00:00:00"
        
        new_user_group = {
            "user_group_id": user_group_id,
            "user_id": target_user_id,
            "group_id": group_id,
            "added_at": timestamp,
            "added_by_user_id": requesting_user_id
        }
        
        user_groups[str(user_group_id)] = new_user_group
        
        return json.dumps({"success": True, "message": "User added to group"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_user_to_group",
                "description": "Add a user to a group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group"},
                        "target_user_id": {"type": "string", "description": "ID of the user to add"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "space_id": {"type": "string", "description": "Space ID if Space Administrator is making the request"}
                    },
                    "required": ["group_id", "target_user_id", "requesting_user_id"]
                }
            }
        }
