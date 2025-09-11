import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ToggleAnonymousAccess(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, requesting_user_id: str,
               enable_anonymous: bool, platform_owner_approval: bool) -> str:
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        user = users[str(requesting_user_id)]
        user_role = user.get("role", "User")
        space = spaces[str(space_id)]
        
        # Authority verification - only Platform Owner can toggle anonymous access
        if user_role != "PlatformOwner" or not platform_owner_approval:
            return json.dumps({"error": "Insufficient authority to toggle anonymous access"})
        
        # Toggle anonymous access
        timestamp = "2025-10-01T00:00:00"
        space["anonymous_access"] = enable_anonymous
        space["updated_at"] = timestamp
        
        status = "enabled" if enable_anonymous else "disabled"
        return json.dumps({"success": True, "message": f"Anonymous access {status}"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "toggle_anonymous_access",
                "description": "Toggle anonymous access for a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting toggle"},
                        "enable_anonymous": {"type": "boolean", "description": "True to enable, False to disable anonymous access (True/False)"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval flag (True/False)"}
                    },
                    "required": ["space_id", "requesting_user_id", "enable_anonymous", "platform_owner_approval"]
                }
            }
        }
