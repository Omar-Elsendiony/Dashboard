import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrievePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        """
        Retrieve page details by ID.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        pages = data.get("pages", {})
        
        if page_id in pages:
            page_data = pages[page_id].copy()
            return json.dumps({
                "success": True,
                "page_data": page_data
            })
        else:
            return json.dumps({
                "success": False,
                "error": f"Page {page_id} not found"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_page",
                "description": "Retrieve page details by ID in the Confluence system. This tool fetches comprehensive page information including page ID, space ID, parent page ID, title, content format, current version, state, creator, editor, timestamps, and publication status. Essential for page verification, content management, version tracking, and validating page existence before performing operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "Unique identifier of the page (required)"
                        }
                    },
                    "required": ["page_id"]
                }
            }
        }
