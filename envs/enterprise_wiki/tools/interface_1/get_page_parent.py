import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageParent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        pages = data.get("pages", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        page = pages[page_id]
        parent_id = str(page.get("parent_id"))
        print(f"Parent ID: {parent_id}")
        
        if not parent_id:
            raise ValueError("Page has no parent")
        
        if parent_id not in pages:
            raise ValueError("Parent page not found")
        
        return json.dumps(pages[parent_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_parent",
                "description": "Get parent page of a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the child page"
                        }
                    },
                    "required": ["page_id"]
                }
            }
        }   
