import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        pages = data.get("pages", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        return json.dumps(pages[page_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_info",
                "description": "Get page information by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page"
                        }
                    },
                    "required": ["page_id"]
                }
            }
        }
