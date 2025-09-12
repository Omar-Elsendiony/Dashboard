import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GrantPagePermission(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, page_id: str,
               permission_type: str, target_user_id: Optional[str] = None,
               target_group_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        pages = data.get("pages", {})
        groups = data.get("groups", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate entities exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        if str(page_id) not in pages:
            return json.dumps({"error": "Page not found"})
        
        if target_user_id and str(target_user_id) not in users:
            return json.dumps({"error": "Target user not found"})
        
        if target_group_id and str(target_group_id) not in groups:
            return json.dumps({"error": "Target group not found"})
        
        if not target_user_id and not target_group_id:
            return json.dumps({"error": "Must specify either target_user_id or target_group_id"})
        
        if target_user_id and target_group_id:
            return json.dumps({"error": "Cannot specify both target_user_id and target_group_id"})
        
        # Validate enum values
        if permission_type not in ["view", "edit", "admin"]:
            return json.dumps({"error": "Invalid permission_type. Must be one of: view, edit, admin"})
        
        requesting_user = users[str(requesting_user_id)]
        page = pages[str(page_id)]
        space_id = page.get("space_id")
        
        # Check authority to grant permissions
        has_authority = False
        
        # Platform Owner can grant any permission
        if requesting_user.get("role") == "PlatformOwner":
            has_authority = True
        else:
            # Check if user has admin permission on the page
            for perm in page_permissions.values():
                if (perm.get("page_id") == page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "admin"):
                    has_authority = True
                    break
            
            # Check if user has moderate permission on the space
            if not has_authority:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_authority = True
                        break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to grant page permissions"})
        
        # Check if permission already exists
        for perm in page_permissions.values():
            if (perm.get("page_id") == page_id and
                ((target_user_id and perm.get("user_id") == target_user_id) or
                 (target_group_id and perm.get("group_id") == target_group_id))):
                return json.dumps({"error": "Permission already exists for this user/group on this page"})
        
        # Create permission
        permission_id = generate_id(page_permissions)
        timestamp = "2025-10-01T00:00:00"
        
        new_permission = {
            "permission_id": int(permission_id),
            "page_id": page_id,
            "user_id": target_user_id,
            "group_id": target_group_id,
            "permission_type": permission_type,
            "granted_by_user_id": requesting_user_id,
            "granted_at": timestamp
        }
        
        page_permissions[permission_id] = new_permission
        
        return json.dumps({
            "permission_id": permission_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "grant_page_permission",
                "description": "Grant page permission to a user or group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user granting permission"},
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "permission_type": {"type": "string", "description": "Type of permission (view, edit, admin)"},
                        "target_user_id": {"type": "string", "description": "ID of the user to grant permission to"},
                        "target_group_id": {"type": "string", "description": "ID of the group to grant permission to"}
                    },
                    "required": ["requesting_user_id", "page_id", "permission_type"]
                }
            }
        }