import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

class CreatePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_title: str, space_id: str, requesting_user_id: str,
               parent_page_id: Optional[str] = None, content: Optional[str] = None,
               labels: Optional[List[str]] = None, template_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        page_labels = data.get("page_labels", {})
        labels_table = data.get("labels", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        # Validate parent page if specified
        if parent_page_id and str(parent_page_id) not in pages:
            return json.dumps({"error": "Parent page not found"})
        
        # Check user permissions - need contribute permission in space or create permission on parent page
        has_permission = False
        
        # Check space permissions
        for perm in space_permissions.values():
            if (perm.get("space_id") == space_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") in ["contribute", "moderate"]):
                has_permission = True
                break
        
        # Check parent page permissions if creating subpage
        if parent_page_id and not has_permission:
            for perm in page_permissions.values():
                if (perm.get("page_id") == parent_page_id and 
                    perm.get("user_id") == requesting_user_id and
                    perm.get("permission_type") in ["create", "admin"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"error": "Insufficient permissions to create page"})
        
        page_id = generate_id(pages)
        timestamp = "2025-10-01T00:00:00"
        
        new_page = {
            "page_id": page_id,
            "space_id": space_id,
            "title": page_title,
            "content": content,
            "content_format": "wiki",
            "parent_page_id": parent_page_id,
            "position": 0,
            "status": "current",
            "version": 1,
            "template_id": template_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "published_at": timestamp,
            "created_by_user_id": requesting_user_id,
            "last_modified_by_user_id": requesting_user_id
        }
        
        pages[page_id] = new_page
        
        # Create content owner permission
        owner_permission_id = generate_id(page_permissions)
        owner_permission = {
            "page_permission_id": owner_permission_id,
            "page_id": page_id,
            "user_id": requesting_user_id,
            "group_id": None,
            "permission_type": "admin",
            "granted_at": timestamp,
            "granted_by_user_id": requesting_user_id
        }
        
        page_permissions[owner_permission_id] = owner_permission
        
        # Add labels if specified
        if labels:
            for label_name in labels:
                # Find or create label
                label_id = None
                for lid, label in labels_table.items():
                    if label.get("name") == label_name and label.get("space_id") == space_id:
                        label_id = lid
                        break
                
                if label_id:
                    page_label_id = generate_id(page_labels)
                    page_label = {
                        "page_label_id": page_label_id,
                        "page_id": page_id,
                        "label_id": label_id,
                        "added_at": timestamp,
                        "added_by_user_id": requesting_user_id
                    }
                    page_labels[str(page_label_id)] = page_label
        
        return json.dumps({
            "page_id": page_id,
            "success": True,
            "content_owner_id": requesting_user_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_page",
                "description": "Create a new wiki page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_title": {"type": "string", "description": "Title of the page"},
                        "space_id": {"type": "string", "description": "ID of the target space"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the page"},
                        "parent_page_id": {"type": "string", "description": "ID of parent page if creating subpage"},
                        "content": {"type": "string", "description": "Initial page content"},
                        "labels": {"type": "array", "items": {"type": "string"}, "description": "Initial labels for the page"},
                        "template_id": {"type": "string", "description": "Template to use for page creation"}
                    },
                    "required": ["page_title", "space_id", "requesting_user_id"]
                }
            }
        }
