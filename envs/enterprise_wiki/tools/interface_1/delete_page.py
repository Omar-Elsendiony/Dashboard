import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeletePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, deleted_by: str) -> str:
        pages = data.get("pages", {})
        users = data.get("users", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        if deleted_by not in users:
            raise ValueError("User not found")
        
        # Remove the page
        del pages[page_id]
        
        return json.dumps({"success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_page",
                "description": "Delete a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page to delete"
                        },
                        "deleted_by": {
                            "type": "string",
                            "description": "The ID of the user deleting the page"
                        }
                    },
                    "required": ["page_id", "deleted_by"]
                }
            }
        }
