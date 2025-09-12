import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ReadPageHierarchy(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, space_id: str,
               root_page_id: Optional[str] = None, max_depth: Optional[int] = None) -> str:
        
        def build_hierarchy(parent_id: Optional[str], current_depth: int = 0) -> list:
            if max_depth and current_depth >= max_depth:
                return []
            
            children = []
            for page_id, page in pages.items():
                if page.get("parent_page_id") == parent_id and page.get("space_id") == space_id:
                    if page.get("status") == "current":  # Only show current pages
                        page_info = {
                            "page_id": page_id,
                            "title": page.get("title"),
                            "created_by_user_id": page.get("created_by_user_id"),
                            "created_at": page.get("created_at"),
                            "children": build_hierarchy(page_id, current_depth + 1)
                        }
                        children.append(page_info)
            
            return sorted(children, key=lambda x: x.get("title", ""))
        
        users = data.get("users", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Check if user has view permission to space
        has_permission = False
        
        # Platform Owner can view any space
        if requesting_user.get("role") == "PlatformOwner":
            has_permission = True
        else:
            # Check space permissions
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["view", "contribute", "moderate"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"error": "No permission to view space hierarchy"})
        
        # Build hierarchy starting from root_page_id or top-level pages
        hierarchy = {
            "space_id": space_id,
            "space_name": spaces[str(space_id)].get("name"),
            "hierarchy": build_hierarchy(root_page_id)
        }
        
        return json.dumps(hierarchy)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "read_page_hierarchy",
                "description": "Read page hierarchy for a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "space_id": {"type": "string", "description": "ID of the space"},
                        "root_page_id": {"type": "string", "description": "ID of root page (optional, shows all top-level if not provided)"},
                        "max_depth": {"type": "integer", "description": "Maximum depth to traverse"}
                    },
                    "required": ["requesting_user_id", "space_id"]
                }
            }
        }