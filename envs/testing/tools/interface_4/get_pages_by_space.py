import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesBySpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find all pages in the space
        space_pages = []
        for page in pages.values():
            if page.get("space_id") == space_id:
                space_pages.append(page)
        
        return json.dumps(space_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_space",
                "description": "Get all pages in a specific space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"}
                    },
                    "required": ["space_id"]
                }
            }
        }
