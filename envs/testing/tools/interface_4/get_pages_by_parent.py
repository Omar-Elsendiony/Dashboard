import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByParent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], parent_page_id: str) -> str:
        
        pages = data.get("pages", {})
        
        # Validate parent page exists
        if str(parent_page_id) not in pages:
            return json.dumps({"error": f"Parent page {parent_page_id} not found"})
        
        # Find all child pages
        child_pages = []
        for page in pages.values():
            if page.get("parent_page_id") == parent_page_id:
                child_pages.append(page)
        
        return json.dumps(child_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_parent",
                "description": "Get all child pages of a parent page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_page_id": {"type": "string", "description": "ID of the parent page"}
                    },
                    "required": ["parent_page_id"]
                }
            }
        }
