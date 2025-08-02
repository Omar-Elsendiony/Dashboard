import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateCommentContent(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        comment_id: int,
        content: str,
        content_format: str = "markdown"
    ) -> str:
        comments = data.get("comments", {})
        comment = comments.get(str(comment_id))
        if not comment:
            raise ValueError("Comment not found")
        
        comment["content"] = content
        comment["content_format"] = content_format
        comment["updated_at"] = None
        
        return json.dumps(comment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_comment_content",
                "description": "Update comment content with the ability to change the format of the content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "integer", "description": "ID of the comment"},
                        "content": {"type": "string", "description": "New content for the comment"},
                        "content_format": {"type": "string", "description": "New format for the content"}
                    },
                    "required": ["comment_id", "content"]
                }
            }
        }
