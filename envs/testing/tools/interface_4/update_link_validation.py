import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateLinkValidation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, mark_as_checked: bool,
               filter_link_type: Optional[str] = None, filter_last_checked_before_date: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        page_links = data.get("page_links", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Validate enum values
        if filter_link_type and filter_link_type not in ["internal", "external"]:
            return json.dumps({"error": "Invalid filter_link_type. Must be one of: internal, external"})
        
        updated_links = []
        timestamp = "2025-10-01T00:00:00"
        
        for link_id, link in page_links.items():
            # Apply filters
            if filter_link_type and link.get("link_type") != filter_link_type:
                continue
            
            # Filter by last checked date (simplified - just check if exists)
            if filter_last_checked_before_date:
                last_checked = link.get("last_checked_at")
                if not last_checked or last_checked >= filter_last_checked_before_date:
                    continue
            
            # Check permissions for this link
            has_permission = False
            source_page_id = link.get("source_page_id")
            
            # Platform Owner can update any link
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            # Check permissions based on source page
            elif source_page_id and str(source_page_id) in pages:
                page = pages[str(source_page_id)]
                space_id = page.get("space_id")
                
                # Check page admin permission
                for perm in page_permissions.values():
                    if (perm.get("page_id") == source_page_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") in ["edit", "admin"]):
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
            
            # Apply update
            if mark_as_checked:
                link["last_checked_at"] = timestamp
            
            updated_links.append(link)
        
        return json.dumps(updated_links)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_link_validation",
                "description": "Update link validation status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "mark_as_checked": {"type": "boolean", "description": "Mark links as checked (True/False)"},
                        "filter_link_type": {"type": "string", "description": "Filter by link type (internal, external)"},
                        "filter_last_checked_before_date": {"type": "string", "description": "Filter by last checked before date (YYYY-MM-DD format)"}
                    },
                    "required": ["requesting_user_id", "mark_as_checked"]
                }
            }
        }