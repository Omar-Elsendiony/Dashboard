import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUserPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, space_id: Optional[str] = None, 
               page_id: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        groups = data.get("groups", {})
        user_groups = data.get("user_groups", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        user = users[str(user_id)]
        permissions = {
            "user_id": user_id,
            "user_role": user.get("role"),
            "space_permissions": [],
            "page_permissions": [],
            "inherited_permissions": []
        }
        
        # Get user's groups
        user_group_ids = []
        for ug in user_groups.values():
            if ug.get("user_id") == user_id:
                user_group_ids.append(ug.get("group_id"))
        
        # Get space permissions
        if space_id:
            if str(space_id) not in spaces:
                return json.dumps({"error": f"Space {space_id} not found"})
            
            # Direct user space permissions
            for sp in space_permissions.values():
                if (sp.get("space_id") == space_id and 
                    sp.get("user_id") == user_id):
                    permissions["space_permissions"].append({
                        "permission_id": sp.get("space_permission_id"),
                        "permission_type": sp.get("permission_type"),
                        "granted_at": sp.get("granted_at"),
                        "granted_by_user_id": sp.get("granted_by_user_id")
                    })
            
            # Group-based space permissions
            for sp in space_permissions.values():
                if (sp.get("space_id") == space_id and 
                    sp.get("group_id") in user_group_ids):
                    group_name = groups.get(str(sp.get("group_id")), {}).get("name", "Unknown")
                    permissions["inherited_permissions"].append({
                        "permission_type": sp.get("permission_type"),
                        "source": "group",
                        "source_name": group_name,
                        "granted_at": sp.get("granted_at")
                    })
        
        # Get page permissions
        if page_id:
            if str(page_id) not in pages:
                return json.dumps({"error": f"Page {page_id} not found"})
            
            # Direct user page permissions
            for pp in page_permissions.values():
                if (pp.get("page_id") == page_id and 
                    pp.get("user_id") == user_id):
                    permissions["page_permissions"].append({
                        "permission_id": pp.get("page_permission_id"),
                        "permission_type": pp.get("permission_type"),
                        "granted_at": pp.get("granted_at"),
                        "granted_by_user_id": pp.get("granted_by_user_id")
                    })
            
            # Group-based page permissions
            for pp in page_permissions.values():
                if (pp.get("page_id") == page_id and 
                    pp.get("group_id") in user_group_ids):
                    group_name = groups.get(str(pp.get("group_id")), {}).get("name", "Unknown")
                    permissions["inherited_permissions"].append({
                        "permission_type": pp.get("permission_type"),
                        "source": "group",
                        "source_name": group_name,
                        "granted_at": pp.get("granted_at")
                    })
        
        # If neither space_id nor page_id provided, get all permissions
        if not space_id and not page_id:
            # All space permissions for user
            for sp in space_permissions.values():
                if sp.get("user_id") == user_id:
                    space_name = spaces.get(str(sp.get("space_id")), {}).get("name", "Unknown")
                    permissions["space_permissions"].append({
                        "space_id": sp.get("space_id"),
                        "space_name": space_name,
                        "permission_type": sp.get("permission_type"),
                        "granted_at": sp.get("granted_at")
                    })
            
            # All page permissions for user
            for pp in page_permissions.values():
                if pp.get("user_id") == user_id:
                    page_title = pages.get(str(pp.get("page_id")), {}).get("title", "Unknown")
                    permissions["page_permissions"].append({
                        "page_id": pp.get("page_id"),
                        "page_title": page_title,
                        "permission_type": pp.get("permission_type"),
                        "granted_at": pp.get("granted_at")
                    })
        
        return json.dumps(permissions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_permissions",
                "description": "Get user permissions with inherited and explicit permissions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to check permissions for"},
                        "space_id": {"type": "string", "description": "Space ID to check space-specific permissions"},
                        "page_id": {"type": "string", "description": "Page ID to check page-specific permissions"}
                    },
                    "required": ["user_id"]
                }
            }
        }
