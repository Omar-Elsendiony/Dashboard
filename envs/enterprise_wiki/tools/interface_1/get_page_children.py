import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageChildren(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        pages = data.get("pages", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        child_pages = []
        for pid, page in pages.items():
            if str(page.get("parent_id")) == str(page_id):
                child_pages.append(page)
        
        return json.dumps(child_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_children",
                "description": "Get child pages of a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the parent page"
                        }
                    },
                    "required": ["page_id"]
                }
            }
        }
