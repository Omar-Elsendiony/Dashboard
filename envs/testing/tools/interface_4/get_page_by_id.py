import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        page = pages[str(page_id)]
        
        return json.dumps(page)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_by_id",
                "description": "Get a single page record by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to retrieve"}
                    },
                    "required": ["page_id"]
                }
            }
        }
