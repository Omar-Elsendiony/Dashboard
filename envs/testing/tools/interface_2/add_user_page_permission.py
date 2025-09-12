import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddUserPagePermission(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], target_user_id: str, requesting_user_id: str,
               page_id: str, permission_type: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        pages = data.get("pages", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate users exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        if str(target_user_id) not in users:
            return json.dumps({"error": "Target user not found"})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": "Page not found"})
        
        page = pages[str(page_id)]
        requesting_user = users[str(requesting_user_id)]
        requesting_user_role = requesting_user.get("role", "User")
        
        # Authority verification
        has_authority = False
        if requesting_user_role == "PlatformOwner":
            has_authority = True
        elif page.get("created_by_user_id") == requesting_user_id:
            # Page creator has authority
            has_authority = True
        else:
            # Check if user has admin permission on page
            for perm in page_permissions.values():
                if (perm.get("user_id") == requesting_user_id and 
                    perm.get("page_id") == page_id and 
                    perm.get("permission_type") == "admin"):
                    has_authority = True
                    break
            
            # Check if user is Space Administrator
            if not has_authority and page.get("space_id"):
                for perm in space_permissions.values():
                    if (perm.get("user_id") == requesting_user_id and 
                        perm.get("space_id") == page.get("space_id") and 
                        perm.get("permission_type") == "moderate"):
                        has_authority = True
                        break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to add page permissions"})
        
        # Validate permission type
        valid_permissions = ["view", "create", "edit", "delete", "admin"]
        if permission_type not in valid_permissions:
            return json.dumps({"error": f"Invalid permission type. Must be one of {valid_permissions}"})
        
        # Check if permission already exists
        for perm in page_permissions.values():
            if (perm.get("user_id") == target_user_id and 
                perm.get("page_id") == page_id and 
                perm.get("permission_type") == permission_type):
                return json.dumps({"error": "Permission already exists"})
        
        # Create permission
        permission_id = generate_id(page_permissions)
        timestamp = "2025-10-01T00:00:00"
        
        new_permission = {
            "page_permission_id": permission_id,
            "page_id": page_id,
            "user_id": target_user_id,
            "group_id": None,
            "permission_type": permission_type,
            "granted_at": timestamp,
            "granted_by_user_id": requesting_user_id
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
                "name": "add_user_page_permission",
                "description": "Add a page permission for a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_user_id": {"type": "string", "description": "ID of the user to grant permission to"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting to add the permission"},
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "permission_type": {"type": "string", "description": "Type of permission (view, create, edit, delete, admin)"}
                    },
                    "required": ["target_user_id", "requesting_user_id", "page_id", "permission_type"]
                }
            }
        }

