import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ReadUserPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, target_user_id: str,
               filter_permission_type: Optional[str] = None, filter_target_type: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        # Validate target user exists
        if str(target_user_id) not in users:
            return json.dumps({"error": "Target user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - Platform Owner can read any permissions, users can read their own
        if requesting_user.get("role") != "PlatformOwner" and requesting_user_id != target_user_id:
            return json.dumps({"error": "Can only read your own permissions or Platform Owner can read any"})
        
        # Validate enum values
        if filter_target_type and filter_target_type not in ["page", "space"]:
            return json.dumps({"error": "Invalid filter_target_type. Must be one of: page, space"})
        
        user_permissions = {
            "user_id": target_user_id,
            "page_permissions": [],
            "space_permissions": []
        }
        
        # Collect page permissions
        if not filter_target_type or filter_target_type == "page":
            for perm in page_permissions.values():
                if perm.get("user_id") == target_user_id:
                    if not filter_permission_type or perm.get("permission_type") == filter_permission_type:
                        # Add page title for context
                        page_id = perm.get("page_id")
                        page_title = pages.get(str(page_id), {}).get("title", "Unknown") if page_id else "Unknown"
                        perm_with_context = dict(perm)
                        perm_with_context["page_title"] = page_title
                        user_permissions["page_permissions"].append(perm_with_context)
        
        # Collect space permissions
        if not filter_target_type or filter_target_type == "space":
            for perm in space_permissions.values():
                if perm.get("user_id") == target_user_id:
                    if not filter_permission_type or perm.get("permission_type") == filter_permission_type:
                        # Add space name for context
                        space_id = perm.get("space_id")
                        space_name = spaces.get(str(space_id), {}).get("name", "Unknown") if space_id else "Unknown"
                        perm_with_context = dict(perm)
                        perm_with_context["space_name"] = space_name
                        user_permissions["space_permissions"].append(perm_with_context)
        
        return json.dumps(user_permissions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "read_user_permissions",
                "description": "Read permissions for a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "target_user_id": {"type": "string", "description": "ID of the user whose permissions to read"},
                        "filter_permission_type": {"type": "string", "description": "Filter by permission type"},
                        "filter_target_type": {"type": "string", "description": "Filter by target type (page, space)"}
                    },
                    "required": ["requesting_user_id", "target_user_id"]
                }
            }
        }