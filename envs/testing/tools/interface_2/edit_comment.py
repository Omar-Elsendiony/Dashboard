import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EditComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str, requesting_user_id: str,
               new_comment_text: str) -> str:
        
        comments = data.get("comments", {})
        users = data.get("users", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        comment = comments[str(comment_id)]
        
        # Check ownership
        if comment.get("created_by_user_id") != requesting_user_id:
            return json.dumps({"error": "Only comment author can edit comment"})
        
        
        # Update comment
        comment["content"] = new_comment_text
        comment["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Comment edited", "edited_flag": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "edit_comment",
                "description": "Edit a comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to edit"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user editing the comment"},
                        "new_comment_text": {"type": "string", "description": "New comment content"},
                    },
                    "required": ["comment_id", "requesting_user_id", "new_comment_text"]
                }
            }
        }
