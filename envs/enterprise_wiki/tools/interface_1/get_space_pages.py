import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacePages(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        
        if space_id not in spaces:
            raise ValueError("Space not found")
        
        space_pages = []
        for page_id, page in pages.items():
            if str(page.get("space_id")) == str(space_id):
                space_pages.append(page)
        
        return json.dumps(space_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_pages",
                "description": "Get all pages in a space for navigation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "The ID of the space"
                        }
                    },
                    "required": ["space_id"]
                }
            }
        }
