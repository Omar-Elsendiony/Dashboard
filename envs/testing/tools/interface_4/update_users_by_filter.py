import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateUsersByFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               filter_role: Optional[str] = None, filter_status: Optional[str] = None, 
               filter_email_domain: Optional[str] = None, update_status: Optional[str] = None,
               update_timezone: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - only Platform Owner can update users
        if requesting_user.get("role") != "PlatformOwner":
            return json.dumps({"error": "Only Platform Owner can update users"})
        
        # Validate enum values
        if filter_role and filter_role not in ["PlatformOwner", "WikiProgramManager", "User"]:
            return json.dumps({"error": "Invalid filter_role. Must be one of: PlatformOwner, WikiProgramManager, User"})
        
        if filter_status and filter_status not in ["active", "inactive", "suspended"]:
            return json.dumps({"error": "Invalid filter_status. Must be one of: active, inactive, suspended"})
        
        if update_status and update_status not in ["active", "inactive", "suspended"]:
            return json.dumps({"error": "Invalid update_status. Must be one of: active, inactive, suspended"})
        
        updated_users = []
        timestamp = "2025-10-01T00:00:00"
        
        for user_id, user in users.items():
            # Apply filters
            if filter_role and user.get("role") != filter_role:
                continue
            if filter_status and user.get("status") != filter_status:
                continue
            if filter_email_domain and not user.get("email", "").endswith(f"@{filter_email_domain}"):
                continue
            
            # Apply updates
            if update_status:
                user["status"] = update_status
            if update_timezone:
                user["timezone"] = update_timezone
            
            user["updated_at"] = timestamp
            updated_users.append(user)
        
        return json.dumps(updated_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_users_by_filter",
                "description": "Update users based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "filter_role": {"type": "string", "description": "Filter by role (PlatformOwner, WikiProgramManager, User)"},
                        "filter_status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"},
                        "filter_email_domain": {"type": "string", "description": "Filter by email domain"},
                        "update_status": {"type": "string", "description": "New status to set (active, inactive, suspended)"},
                        "update_timezone": {"type": "string", "description": "New timezone to set"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }