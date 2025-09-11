import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSpaceInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: Optional[str] = None, 
               space_name: Optional[str] = None, owner_id: Optional[str] = None) -> str:
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        results = []
        
        # Filter spaces based on criteria
        for space in spaces.values():
            if space_id and str(space.get("space_id")) != str(space_id):
                continue
            if space_name and space_name.lower() not in space.get("name", "").lower():
                continue
            if owner_id and str(space.get("created_by_user_id")) != str(owner_id):
                continue
            
            # Get space owner info
            owner = users.get(str(space.get("created_by_user_id")), {})
            
            # Count pages in space
            page_count = 0
            for page in pages.values():
                if (str(page.get("space_id")) == str(space.get("space_id")) and 
                    page.get("status") == "current"):
                    page_count += 1
            
            # Get homepage info
            homepage_info = None
            if space.get("homepage_id"):
                homepage = pages.get(str(space.get("homepage_id")))
                if homepage:
                    homepage_info = {
                        "page_id": space.get("homepage_id"),
                        "title": homepage.get("title")
                    }
            
            # Get space permissions summary
            permissions_summary = {
                "view_permissions": 0,
                "contribute_permissions": 0,
                "moderate_permissions": 0
            }
            
            for perm in space_permissions.values():
                if str(perm.get("space_id")) == str(space.get("space_id")):
                    perm_type = perm.get("permission_type")
                    if perm_type == "view":
                        permissions_summary["view_permissions"] += 1
                    elif perm_type == "contribute":
                        permissions_summary["contribute_permissions"] += 1
                    elif perm_type == "moderate":
                        permissions_summary["moderate_permissions"] += 1
            
            space_info = {
                "space_id": space.get("space_id"),
                "space_key": space.get("space_key"),
                "name": space.get("name"),
                "description": space.get("description"),
                "type": space.get("type"),
                "status": space.get("status"),
                "anonymous_access": space.get("anonymous_access"),
                "public_signup": space.get("public_signup"),
                "theme": space.get("theme"),
                "logo_url": space.get("logo_url"),
                "homepage": homepage_info,
                "page_count": page_count,
                "owner": {
                    "user_id": space.get("created_by_user_id"),
                    "username": owner.get("username", "Unknown"),
                    "display_name": owner.get("display_name", "Unknown")
                },
                "permissions_summary": permissions_summary,
                "created_at": space.get("created_at"),
                "updated_at": space.get("updated_at")
            }
            
            results.append(space_info)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_info",
                "description": "Get space information with configuration and permissions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "Filter by space ID"},
                        "space_name": {"type": "string", "description": "Filter by space name"},
                        "owner_id": {"type": "string", "description": "Filter by space owner ID"}
                    },
                    "required": []
                }
            }
        }
