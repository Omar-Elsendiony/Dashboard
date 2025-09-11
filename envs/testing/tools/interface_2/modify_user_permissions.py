import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifyUserPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               permission_type: str, action: str, space_id: Optional[str] = None,
               page_id: Optional[str] = None, target_user_id: str = None, group_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        groups = data.get("groups", {})
        
        # Validate entities exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        if target_user_id and str(target_user_id) not in users:
            return json.dumps({"error": f"Target user {target_user_id} not found"})
        
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
            return json.dumps({"error": "Insufficient authority to modify user permissions"})
        
        # Validate action
        if action not in ["grant", "revoke"]:
            return json.dumps({"error": "Action must be 'grant' or 'revoke'"})
        
        timestamp = "2025-10-01T00:00:00"
        
        # Handle space permissions
        if space_id:
            if permission_type not in ["view", "contribute", "moderate"]:
                return json.dumps({"error": f"Invalid space permission type. Must be one of ['view', 'contribute', 'moderate']"})
            
            if str(space_id) not in spaces:
                return json.dumps({"error": f"Space {space_id} not found"})
            
            if action == "grant":
                # Check if permission already exists
                exists = False
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == target_user_id and
                        perm.get("group_id") == group_id and
                        perm.get("permission_type") == permission_type):
                        exists = True
                        break
                
                if exists:
                    return json.dumps({"error": "Permission already exists"})
                
                perm_id = generate_id(space_permissions)
                new_permission = {
                    "space_permission_id": perm_id,
                    "space_id": space_id,
                    "user_id": target_user_id,
                    "group_id": group_id,
                    "permission_type": permission_type,
                    "granted_at": timestamp,
                    "granted_by_user_id": requesting_user_id
                }
                space_permissions[perm_id] = new_permission
                return json.dumps({
                    "permission_id": perm_id,
                    "success": True,
                    "permission_type": "space",
                    "granted_to": "user" if target_user_id else "group"
                })
            
            elif action == "revoke":
                # Find and remove permission
                to_remove = []
                for perm_id, perm in space_permissions.items():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == target_user_id and
                        perm.get("group_id") == group_id and
                        perm.get("permission_type") == permission_type):
                        to_remove.append(perm_id)
                
                if not to_remove:
                    return json.dumps({"error": "Permission not found"})
                
                for perm_id in to_remove:
                    del space_permissions[perm_id]
                
                return json.dumps({"success": True, "message": "Space permission revoked"})
        
        # Handle page permissions
        elif page_id:
            if permission_type not in ["view", "create", "edit", "delete", "admin"]:
                return json.dumps({"error": f"Invalid page permission type. Must be one of ['view', 'create', 'edit', 'delete', 'admin']"})
            
            if str(page_id) not in pages:
                return json.dumps({"error": f"Page {page_id} not found"})
            
            if action == "grant":
                # Check if permission already exists
                exists = False
                for perm in page_permissions.values():
                    if (perm.get("page_id") == page_id and 
                        perm.get("user_id") == target_user_id and
                        perm.get("group_id") == group_id and
                        perm.get("permission_type") == permission_type):
                        exists = True
                        break
                
                if exists:
                    return json.dumps({"error": "Permission already exists"})
                
                perm_id = generate_id(page_permissions)
                new_permission = {
                    "page_permission_id": perm_id,
                    "page_id": page_id,
                    "user_id": target_user_id,
                    "group_id": group_id,
                    "permission_type": permission_type,
                    "granted_at": timestamp,
                    "granted_by_user_id": requesting_user_id
                }
                page_permissions[perm_id] = new_permission
                return json.dumps({
                    "permission_id": perm_id,
                    "success": True,
                    "permission_type": "page",
                    "granted_to": "user" if target_user_id else "group"
                })
            
            elif action == "revoke":
                # Find and remove permission
                to_remove = []
                for perm_id, perm in page_permissions.items():
                    if (perm.get("page_id") == page_id and 
                        perm.get("user_id") == target_user_id and
                        perm.get("group_id") == group_id and
                        perm.get("permission_type") == permission_type):
                        to_remove.append(perm_id)
                
                if not to_remove:
                    return json.dumps({"error": "Permission not found"})
                
                for perm_id in to_remove:
                    del page_permissions[perm_id]
                
                return json.dumps({"success": True, "message": "Page permission revoked"})
        
        else:
            return json.dumps({"error": "Must specify either space_id or page_id"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_user_permissions",
                "description": "Modify user permissions for spaces or pages",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_user_id": {"type": "string", "description": "ID of the user to modify permissions for (required if not group permission)"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "permission_type": {"type": "string", "description": "Type of permission (space: view/contribute/moderate, page: view/create/edit/delete/admin)"},
                        "action": {"type": "string", "description": "Action to take: 'grant' or 'revoke'"},
                        "space_id": {"type": "string", "description": "Space ID if modifying space-specific permissions"},
                        "page_id": {"type": "string", "description": "Page ID if modifying page-specific permissions"},
                        "group_id": {"type": "string", "description": "ID of the group (for group permissions instead of user)"}
                    },
                    "required": ["requesting_user_id", "permission_type", "action"]
                }
            }
        }