import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DeletePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, requesting_user_id: str,
               content_owner_approval: Optional[bool] = None,
               space_administrator_approval: Optional[bool] = None,
               force_delete: bool = False) -> str:
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": "Page not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        page = pages[str(page_id)]
        space_id = page.get("space_id")
        
        # Check for child pages (dependencies)
        child_pages = []
        for p in pages.values():
            if p.get("parent_page_id") == page_id:
                child_pages.append(p)
        
        if child_pages and not force_delete:
            return json.dumps({"error": "Cannot delete page with child pages. Use force_delete or remove child pages first"})
        
        # Check user permissions
        has_delete_permission = False
        is_content_owner = False
        is_space_admin = False
        
        # Check if user is content owner (has admin permission on page)
        for perm in page_permissions.values():
            if (perm.get("page_id") == page_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") == "admin"):
                is_content_owner = True
                break
        
        # Check if user is space administrator
        for perm in space_permissions.values():
            if (perm.get("space_id") == space_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") == "moderate"):
                is_space_admin = True
                break
        
        # Check if user has delete permission
        for perm in page_permissions.values():
            if (perm.get("page_id") == page_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") in ["delete", "admin"]):
                has_delete_permission = True
                break
        
        # Authority verification
        if is_content_owner and content_owner_approval:
            pass
        elif is_space_admin and space_administrator_approval:
            pass
        elif has_delete_permission:
            pass
        else:
            return json.dumps({"error": "Insufficient authority to delete page"})
        
        # Delete the page (mark as deleted)
        timestamp = "2025-10-01T00:00:00"
        page["status"] = "deleted"
        page["updated_at"] = timestamp
        
        # Delete child pages if force_delete is True
        if force_delete:
            for child in child_pages:
                child["status"] = "deleted"
                child["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Page deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_page",
                "description": "Delete a wiki page with dependency checking",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting deletion"},
                        "content_owner_approval": {"type": "boolean", "description": "Content Owner approval if user is Content Owner (True/False)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"},
                        "force_delete": {"type": "boolean", "description": "Force deletion despite dependencies (True/False)"}
                    },
                    "required": ["page_id", "requesting_user_id"]
                }
            }
        }
