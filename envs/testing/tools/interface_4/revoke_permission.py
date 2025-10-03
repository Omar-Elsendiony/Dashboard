import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RevokePermission(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, permission_id: str,
               permission_table: str) -> str:
        
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        # Validate permission table type
        if permission_table not in ["page_permissions", "space_permissions"]:
            return json.dumps({"error": "Invalid permission_table. Must be 'page_permissions' or 'space_permissions'"})
        
        permissions_table = page_permissions if permission_table == "page_permissions" else space_permissions
        
        # Validate permission exists
        if str(permission_id) not in permissions_table:
            return json.dumps({"error": "Permission not found"})
        
        requesting_user = users[str(requesting_user_id)]
        permission = permissions_table[str(permission_id)]
        
        # Check authority to revoke permission
        has_authority = False
        
        # Platform Owner can revoke any permission
        if requesting_user.get("role") == "PlatformOwner":
            has_authority = True
        # User who granted the permission can revoke it
        elif permission.get("granted_by_user_id") == requesting_user_id:
            has_authority = True
        # For page permissions, page admin or space moderator can revoke
        elif permission_table == "page_permissions":
            page_id = permission.get("page_id")
            # Check page admin permission
            for perm in page_permissions.values():
                if (perm.get("page_id") == page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "admin"):
                    has_authority = True
                    break
            
            # Check space moderate permission
            if not has_authority:
                # Get space_id from page
                pages = data.get("pages", {})
                if str(page_id) in pages:
                    space_id = pages[str(page_id)].get("space_id")
                    for perm in space_permissions.values():
                        if (perm.get("space_id") == space_id and 
                            perm.get("user_id") == requesting_user_id and 
                            perm.get("permission_type") == "moderate"):
                            has_authority = True
                            break
        
        # For space permissions, space moderator can revoke
        elif permission_table == "space_permissions":
            space_id = permission.get("space_id")
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "moderate"):
                    has_authority = True
                    break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to revoke permission"})
        
        # Revoke the permission
        del permissions_table[str(permission_id)]
        
        return json.dumps({"success": True, "message": "Permission revoked"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "revoke_permission",
                "description": "Revoke a page or space permission",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user revoking permission"},
                        "permission_id": {"type": "string", "description": "ID of the permission to revoke"},
                        "permission_table": {"type": "string", "description": "Type of permission (page_permissions, space_permissions)"}
                    },
                    "required": ["requesting_user_id", "permission_id", "permission_table"]
                }
            }
        }