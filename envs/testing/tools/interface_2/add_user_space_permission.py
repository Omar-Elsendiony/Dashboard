import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddUserSpacePermission(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], target_user_id: str, requesting_user_id: str,
               space_id: str, permission_type: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate users exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        if str(target_user_id) not in users:
            return json.dumps({"error": "Target user not found"})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        requesting_user = users[str(requesting_user_id)]
        requesting_user_role = requesting_user.get("role", "User")
        
        # Authority verification
        has_authority = False
        if requesting_user_role == "PlatformOwner":
            has_authority = True
        else:
            # Check if user is Space Administrator
            for perm in space_permissions.values():
                if (perm.get("user_id") == requesting_user_id and 
                    perm.get("space_id") == space_id and 
                    perm.get("permission_type") == "moderate"):
                    has_authority = True
                    break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to add space permissions"})
        
        # Validate permission type
        valid_permissions = ["view", "contribute", "moderate"]
        if permission_type not in valid_permissions:
            return json.dumps({"error": f"Invalid permission type. Must be one of {valid_permissions}"})
        
        # Check if permission already exists
        for perm in space_permissions.values():
            if (perm.get("user_id") == target_user_id and 
                perm.get("space_id") == space_id and 
                perm.get("permission_type") == permission_type):
                return json.dumps({"error": "Permission already exists"})
        
        # Create permission
        permission_id = generate_id(space_permissions)
        timestamp = "2025-10-01T00:00:00"
        
        new_permission = {
            "space_permission_id": permission_id,
            "space_id": space_id,
            "user_id": target_user_id,
            "group_id": None,
            "permission_type": permission_type,
            "granted_at": timestamp,
            "granted_by_user_id": requesting_user_id
        }
        
        space_permissions[permission_id] = new_permission
        return json.dumps({
            "permission_id": permission_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_user_space_permission",
                "description": "Add a space permission for a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_user_id": {"type": "string", "description": "ID of the user to grant permission to"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting to add the permission"},
                        "space_id": {"type": "string", "description": "ID of the space"},
                        "permission_type": {"type": "string", "description": "Type of permission (view, contribute, moderate)"}
                    },
                    "required": ["target_user_id", "requesting_user_id", "space_id", "permission_type"]
                }
            }
        }


