import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageVersionsByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        page_versions = data.get("page_versions", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find all page versions created by the user
        user_versions = []
        for version in page_versions.values():
            if version.get("created_by_user_id") == created_by_user_id:
                user_versions.append(version)
        
        return json.dumps(user_versions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_versions_by_creator",
                "description": "Get all page versions created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the versions"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
