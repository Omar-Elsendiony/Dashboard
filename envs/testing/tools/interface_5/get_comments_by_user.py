import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        comments = data.get("comments", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find comments by the user
        user_comments = []
        for comment in comments.values():
            if comment.get("created_by_user_id") == created_by_user_id:
                user_comments.append(comment)
        
        return json.dumps(user_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_user",
                "description": "Get all comments created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user to get comments for"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
