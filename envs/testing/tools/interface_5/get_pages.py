import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPages(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: Optional[str] = None, space_id: Optional[str] = None,
               parent_page_id: Optional[str] = None, creator_id: Optional[str] = None,
               status: Optional[str] = None, template_id: Optional[str] = None) -> str:
        
        pages = data.get("pages", {})
        result = []
        
        for pid, page in pages.items():
            # Apply filters
            if page_id and str(page_id) != pid:
                continue
            if space_id and page.get("space_id") != space_id:
                continue
            if parent_page_id and page.get("parent_page_id") != parent_page_id:
                continue
            if creator_id and page.get("created_by_user_id") != creator_id:
                continue
            if status and page.get("status") != status:
                continue
            if template_id and page.get("template_id") != template_id:
                continue
            
            result.append({
                "page_id": pid,
                "space_id": page.get("space_id"),
                "title": page.get("title"),
                "content": page.get("content"),
                "content_format": page.get("content_format"),
                "parent_page_id": page.get("parent_page_id"),
                "position": page.get("position"),
                "status": page.get("status"),
                "version": page.get("version"),
                "template_id": page.get("template_id"),
                "created_at": page.get("created_at"),
                "updated_at": page.get("updated_at"),
                "published_at": page.get("published_at"),
                "created_by_user_id": page.get("created_by_user_id"),
                "last_modified_by_user_id": page.get("last_modified_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages",
                "description": "Get pages matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "space_id": {"type": "string", "description": "ID of the space containing the page"},
                        "parent_page_id": {"type": "string", "description": "ID of the parent page"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the page"},
                        "status": {"type": "string", "description": "Status of page (current, draft, deleted, historical)"},
                        "template_id": {"type": "string", "description": "ID of the template used for the page"}
                    },
                    "required": []
                }
            }
        }
