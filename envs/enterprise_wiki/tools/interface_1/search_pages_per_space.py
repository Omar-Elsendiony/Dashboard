import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SearchPagesPerSpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, title: Optional[str] = None, page_template_id: Optional[str] = None) -> str:
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        
        if space_id not in spaces:
            raise ValueError("Space not found")
        
        matching_pages = []
        for page_id, page in pages.items():
            if str(page.get("space_id")) != str(space_id):
                continue
            
            match = True
            
            if title is not None and page.get("title") != title:
                match = False
            
            if page_template_id is not None and page.get("template_id") != page_template_id:
                match = False
            
            if match:
                matching_pages.append(page)
        
        return json.dumps(matching_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_pages_per_space",
                "description": "Search pages by filtering using either the title or the template_id or both",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "The ID of the space to search in"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title to search for (optional)"
                        },
                        "page_template_id": {
                            "type": "string",
                            "description": "The template ID to filter by (optional)"
                        }
                    },
                    "required": ["space_id"]
                }
            }
        }
