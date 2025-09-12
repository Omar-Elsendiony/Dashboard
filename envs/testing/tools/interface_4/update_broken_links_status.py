import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateBrokenLinksStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, new_is_broken_status: bool,
               filter_source_page_id: Optional[str] = None, filter_space_id: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        page_links = data.get("page_links", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        updated_links = []
        timestamp = "2025-10-01T00:00:00"
        
        for link_id, link in page_links.items():
            source_page_id = link.get("source_page_id")
            
            # Apply filters
            if filter_source_page_id and source_page_id != filter_source_page_id:
                continue
            
            # Filter by space_id
            if filter_space_id and source_page_id and str(source_page_id) in pages:
                page = pages[str(source_page_id)]
                if page.get("space_id") != filter_space_id:
                    continue
            
            # Check permissions for this link
            has_permission = False
            
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
            link["is_broken"] = new_is_broken_status
            link["last_checked_at"] = timestamp
            updated_links.append(link)
        
        return json.dumps(updated_links)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_broken_links_status",
                "description": "Update broken link status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "new_is_broken_status": {"type": "boolean", "description": "New broken status (True/False)"},
                        "filter_source_page_id": {"type": "string", "description": "Filter by source page ID"},
                        "filter_space_id": {"type": "string", "description": "Filter by space ID"}
                    },
                    "required": ["requesting_user_id", "new_is_broken_status"]
                }
            }
        }