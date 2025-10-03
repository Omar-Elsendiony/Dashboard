import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdatePagesByFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               filter_space_id: Optional[str] = None, filter_status: Optional[str] = None,
               filter_template_id: Optional[str] = None, update_status: Optional[str] = None,
               update_content_format: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Validate enum values
        if filter_status and filter_status not in ["current", "draft", "deleted", "historical"]:
            return json.dumps({"error": "Invalid filter_status. Must be one of: current, draft, deleted, historical"})
        
        if update_status and update_status not in ["current", "draft", "deleted", "historical"]:
            return json.dumps({"error": "Invalid update_status. Must be one of: current, draft, deleted, historical"})
        
        if update_content_format and update_content_format not in ["wiki", "markdown", "html"]:
            return json.dumps({"error": "Invalid update_content_format. Must be one of: wiki, markdown, html"})
        
        updated_pages = []
        timestamp = "2025-10-01T00:00:00"
        
        for page_id, page in pages.items():
            # Apply filters
            if filter_space_id and page.get("space_id") != filter_space_id:
                continue
            if filter_status and page.get("status") != filter_status:
                continue
            if filter_template_id and page.get("template_id") != filter_template_id:
                continue
            
            # Check permissions for this page
            has_permission = False
            space_id = page.get("space_id")
            
            # Platform Owner can update any page
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            # Check page admin permission
            else:
                for perm in page_permissions.values():
                    if (perm.get("page_id") == page_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "admin"):
                        has_permission = True
                        break
                
                # Check space admin permission
                if not has_permission:
                    for perm in space_permissions.values():
                        if (perm.get("space_id") == space_id and 
                            perm.get("user_id") == requesting_user_id and 
                            perm.get("permission_type") == "moderate"):
                            has_permission = True
                            break
            
            if not has_permission:
                continue
            
            # Apply updates
            if update_status:
                page["status"] = update_status
            if update_content_format:
                page["content_format"] = update_content_format
            
            page["updated_at"] = timestamp
            updated_pages.append(page)
        
        return json.dumps(updated_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_pages_by_filter",
                "description": "Update pages based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "filter_space_id": {"type": "string", "description": "Filter by space ID"},
                        "filter_status": {"type": "string", "description": "Filter by status (current, draft, deleted, historical)"},
                        "filter_template_id": {"type": "string", "description": "Filter by template ID"},
                        "update_status": {"type": "string", "description": "New status to set (current, draft, deleted, historical)"},
                        "update_content_format": {"type": "string", "description": "New content format to set (wiki, markdown, html)"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }