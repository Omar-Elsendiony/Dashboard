import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find all pages created by the user
        user_pages = []
        for page in pages.values():
            if page.get("created_by_user_id") == created_by_user_id:
                user_pages.append(page)
        
        return json.dumps(user_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_creator",
                "description": "Get all pages created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the pages"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
