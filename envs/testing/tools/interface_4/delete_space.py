import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteSpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, requesting_user_id: str,
               force_delete: bool = False) -> str:
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        labels = data.get("labels", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - only Platform Owner can delete spaces
        if requesting_user.get("role") != "PlatformOwner":
            return json.dumps({"error": "Only Platform Owner can delete spaces"})
        
        # Check for dependencies unless force_delete
        if not force_delete:
            # Check for pages in space
            space_pages = []
            for page in pages.values():
                if page.get("space_id") == space_id and page.get("status") != "deleted":
                    space_pages.append(page)
            
            if space_pages:
                return json.dumps({"error": f"Cannot delete space with {len(space_pages)} active pages. Use force_delete=True or remove pages first"})
        
        # Delete or mark pages as deleted
        pages_to_delete = []
        for page_id, page in pages.items():
            if page.get("space_id") == space_id:
                pages_to_delete.append(page_id)
        
        timestamp = "2025-10-01T00:00:00"
        
        if force_delete:
            # Mark all pages as deleted
            for page_id in pages_to_delete:
                pages[page_id]["status"] = "deleted"
                pages[page_id]["updated_at"] = timestamp
        
        # Remove space permissions
        space_perms_to_delete = []
        for perm_id, perm in space_permissions.items():
            if perm.get("space_id") == space_id:
                space_perms_to_delete.append(perm_id)
        
        for perm_id in space_perms_to_delete:
            del space_permissions[perm_id]
        
        # Remove page permissions for pages in this space
        page_perms_to_delete = []
        for perm_id, perm in page_permissions.items():
            page_id = perm.get("page_id")
            if page_id and str(page_id) in pages and pages[str(page_id)].get("space_id") == space_id:
                page_perms_to_delete.append(perm_id)
        
        for perm_id in page_perms_to_delete:
            del page_permissions[perm_id]
        
        # Remove labels in this space
        labels_to_delete = []
        for label_id, label in labels.items():
            if label.get("space_id") == space_id:
                labels_to_delete.append(label_id)
        
        for label_id in labels_to_delete:
            del labels[label_id]
        
        # Delete the space
        del spaces[str(space_id)]
        
        return json.dumps({"success": True, "message": "Space deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_space",
                "description": "Delete a space and all its content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user deleting the space"},
                        "force_delete": {"type": "boolean", "description": "Force delete despite dependencies (True/False)"}
                    },
                    "required": ["space_id", "requesting_user_id"]
                }
            }
        }