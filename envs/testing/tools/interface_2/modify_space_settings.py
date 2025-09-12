import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifySpaceSettings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, requesting_user_id: str,
               settings_changes: Dict[str, Any], space_administrator_approval: Optional[bool] = None,
               platform_owner_approval: Optional[bool] = None) -> str:
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        user = users[str(requesting_user_id)]
        user_role = user.get("role", "User")
        space = spaces[str(space_id)]
        
        # Check if user has space admin permissions
        has_space_admin = False
        for perm in space_permissions.values():
            if (perm.get("space_id") == space_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") == "moderate"):
                has_space_admin = True
                break
        
        # Authority verification
        if user_role == "PlatformOwner" and platform_owner_approval:
            pass  # Platform owner can modify any space
        elif has_space_admin and space_administrator_approval:
            pass  # Space admin can modify their space
        elif user_role in ["WikiProgramManager"] and space.get("created_by_user_id") == requesting_user_id:
            pass  # Wiki program manager can modify spaces they created
        else:
            return json.dumps({"error": "Insufficient authority to modify space settings"})
        
        # Apply settings changes
        timestamp = "2025-10-01T00:00:00"
        for key, value in settings_changes.items():
            if key in ["name", "description", "theme", "logo_url", "anonymous_access", "public_signup"]:
                space[key] = value
        
        space["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Space settings updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_space_settings",
                "description": "Modify space settings with appropriate authority verification",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to modify"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting modification"},
                        "settings_changes": {"type": "object", "description": "Dictionary of settings to modify"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval if user is Platform Owner (True/False)"}
                    },
                    "required": ["space_id", "requesting_user_id", "settings_changes"]
                }
            }
        }
