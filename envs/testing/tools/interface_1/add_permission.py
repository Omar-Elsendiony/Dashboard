import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddPermission(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               permission_type: str, space_id: Optional[str] = None, 
               page_id: Optional[str] = None, target_user_id: str = None, group_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        groups = data.get("groups", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        # Validate target user exists (unless adding group permission)
        if target_user_id and str(target_user_id) not in users:
            return json.dumps({"error": "Target user not found"})
        
        # Validate group exists (if group permission)
        if group_id and str(group_id) not in groups:
            return json.dumps({"error": "Group not found"})
        
        requesting_user = users[str(requesting_user_id)]
        requesting_user_role = requesting_user.get("role", "User")
        
        # Authority verification
        def has_permission_authority(requesting_role: str, space_id: str = None, page_id: str = None) -> bool:
            # Platform Owner can manage any permissions
            if requesting_role == "PlatformOwner":
                return True
            
            # Space Administrator can manage permissions in their space
            if space_id:
                for perm in space_permissions.values():
                    if (perm.get("user_id") == requesting_user_id and 
                        perm.get("space_id") == space_id and 
                        perm.get("permission_type") == "moderate"):
                        return True
            
            # Content Owner can manage permissions on their page
            if page_id:
                for perm in page_permissions.values():
                    if (perm.get("user_id") == requesting_user_id and 
                        perm.get("page_id") == page_id and 
                        perm.get("permission_type") == "admin"):
                        return True
                
                # Check if user created the page
                if str(page_id) in pages:
                    page = pages[str(page_id)]
                    if page.get("created_by_user_id") == requesting_user_id:
                        return True
            
            return False
        
        if not has_permission_authority(requesting_user_role, space_id, page_id):
            return json.dumps({"error": "Insufficient authority to add permissions"})
        
        # Validate permission type
        if space_id:
            valid_space_permissions = ["view", "contribute", "moderate"]
            if permission_type not in valid_space_permissions:
                return json.dumps({"error": f"Invalid space permission type. Must be one of {valid_space_permissions}"})
            
            # Validate space exists
            if str(space_id) not in spaces:
                return json.dumps({"error": "Space not found"})
            
            # Check if permission already exists
            for perm in space_permissions.values():
                if (perm.get("user_id") == target_user_id and 
                    perm.get("group_id") == group_id and
                    perm.get("space_id") == space_id and 
                    perm.get("permission_type") == permission_type):
                    return json.dumps({"error": "Permission already exists"})
            
            # Create space permission
            permission_id = generate_id(space_permissions)
            timestamp = "2025-10-01T00:00:00"
            
            new_permission = {
                "space_permission_id": permission_id,
                "space_id": space_id,
                "user_id": target_user_id,
                "group_id": group_id,
                "permission_type": permission_type,
                "granted_at": timestamp,
                "granted_by_user_id": requesting_user_id
            }
            
            space_permissions[permission_id] = new_permission
            return json.dumps({
                "permission_id": permission_id,
                "success": True,
                "permission_type": "space",
                "granted_to": "user" if target_user_id else "group"
            })
        
        elif page_id:
            valid_page_permissions = ["view", "create", "edit", "delete", "admin"]
            if permission_type not in valid_page_permissions:
                return json.dumps({"error": f"Invalid page permission type. Must be one of {valid_page_permissions}"})
            
            # Validate page exists
            if str(page_id) not in pages:
                return json.dumps({"error": "Page not found"})
            
            # Check if permission already exists
            for perm in page_permissions.values():
                if (perm.get("user_id") == target_user_id and 
                    perm.get("group_id") == group_id and
                    perm.get("page_id") == page_id and 
                    perm.get("permission_type") == permission_type):
                    return json.dumps({"error": "Permission already exists"})
            
            # Create page permission
            permission_id = generate_id(page_permissions)
            timestamp = "2025-10-01T00:00:00"
            
            new_permission = {
                "page_permission_id": permission_id,
                "page_id": page_id,
                "user_id": target_user_id,
                "group_id": group_id,
                "permission_type": permission_type,
                "granted_at": timestamp,
                "granted_by_user_id": requesting_user_id
            }
            
            page_permissions[permission_id] = new_permission
            return json.dumps({
                "permission_id": permission_id,
                "success": True,
                "permission_type": "page",
                "granted_to": "user" if target_user_id else "group"
            })
        
        else:
            return json.dumps({"error": "Must specify either space_id or page_id"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_permission",
                "description": "Add a permission for a user or group on a space or page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_user_id": {"type": "string", "description": "ID of the user to grant permission to (required if not group permission)"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting to add the permission"},
                        "permission_type": {"type": "string", "description": "Type of permission (space: view/contribute/moderate, page: view/create/edit/delete/admin)"},
                        "space_id": {"type": "string", "description": "ID of the space (for space permissions)"},
                        "page_id": {"type": "string", "description": "ID of the page (for page permissions)"},
                        "group_id": {"type": "string", "description": "ID of the group (for group permissions instead of user)"}
                    },
                    "required": ["requesting_user_id", "permission_type"]
                }
            }
        }