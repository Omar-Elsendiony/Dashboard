import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdatePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, requesting_user_id: str,
               content_changes: Optional[Dict[str, Any]] = None,
               label_changes: Optional[Dict[str, Any]] = None,
               ownership_changes: Optional[Dict[str, Any]] = None,
               title_change: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        page_versions = data.get("page_versions", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": "Page not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        page = pages[str(page_id)]
        
        # Check user permissions - need edit or admin permission
        has_permission = False
        for perm in page_permissions.values():
            if (perm.get("page_id") == page_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") in ["edit", "admin"]):
                has_permission = True
                break
        
        if not has_permission:
            return json.dumps({"error": "Insufficient permissions to update page"})
        
        timestamp = "2025-10-01T00:00:00"
        
        # Create version history entry
        version_id = generate_id(page_versions)
        page_version = {
            "page_version_id": version_id,
            "page_id": page_id,
            "version_number": page.get("version", 1),
            "title": page.get("title"),
            "content": page.get("content"),
            "content_format": page.get("content_format", "wiki"),
            "change_type": "major",
            "created_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        page_versions[version_id] = page_version
        
        # Apply content changes
        if content_changes:
            for key, value in content_changes.items():
                if key in ["content", "content_format"]:
                    page[key] = value
        
        # Apply title change
        if title_change:
            page["title"] = title_change
        
        # Update metadata
        page["version"] = page.get("version", 1) + 1
        page["updated_at"] = timestamp
        page["last_modified_by_user_id"] = requesting_user_id
        
        return json.dumps({"success": True, "message": "Page updated", "page_id": page_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_page",
                "description": "Update page content, labels, ownership, or title",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to update"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user updating the page"},
                        "content_changes": {"type": "object", "description": "Content updates"},
                        "label_changes": {"type": "object", "description": "Label additions/removals"},
                        "ownership_changes": {"type": "object", "description": "Ownership modifications"},
                        "title_change": {"type": "string", "description": "New page title"}
                    },
                    "required": ["page_id", "requesting_user_id"]
                }
            }
        }
