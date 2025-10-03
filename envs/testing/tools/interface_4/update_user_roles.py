import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateUserRoles(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, new_role: str,
               filter_current_role: Optional[str] = None, filter_email_domain: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - only Platform Owner can update user roles
        if requesting_user.get("role") != "PlatformOwner":
            return json.dumps({"error": "Only Platform Owner can update user roles"})
        
        # Validate enum values
        if filter_current_role and filter_current_role not in ["PlatformOwner", "WikiProgramManager", "User"]:
            return json.dumps({"error": "Invalid filter_current_role. Must be one of: PlatformOwner, WikiProgramManager, User"})
        
        if new_role not in ["PlatformOwner", "WikiProgramManager", "User"]:
            return json.dumps({"error": "Invalid new_role. Must be one of: PlatformOwner, WikiProgramManager, User"})
        
        updated_users = []
        timestamp = "2025-10-01T00:00:00"
        
        for user_id, user in users.items():
            # Apply filters
            if filter_current_role and user.get("role") != filter_current_role:
                continue
            if filter_email_domain and not user.get("email", "").endswith(f"@{filter_email_domain}"):
                continue
            
            # Update role
            user["role"] = new_role
            user["updated_at"] = timestamp
            updated_users.append(user)
        
        return json.dumps(updated_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_roles",
                "description": "Update user roles based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "new_role": {"type": "string", "description": "New role to assign (PlatformOwner, WikiProgramManager, User)"},
                        "filter_current_role": {"type": "string", "description": "Filter by current role (PlatformOwner, WikiProgramManager, User)"},
                        "filter_email_domain": {"type": "string", "description": "Filter by email domain"}
                    },
                    "required": ["requesting_user_id", "new_role"]
                }
            }
        }