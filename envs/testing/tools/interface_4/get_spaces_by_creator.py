import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacesByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find spaces created by user
        matching_spaces = []
        for space_id, space in spaces.items():
            if space.get("created_by_user_id") == created_by_user_id:
                matching_spaces.append(space)
        
        return json.dumps(matching_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_creator",
                "description": "Get all spaces created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the spaces"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
