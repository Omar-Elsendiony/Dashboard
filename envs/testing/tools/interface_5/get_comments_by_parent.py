import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByParent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], parent_comment_id: str) -> str:
        
        comments = data.get("comments", {})
        
        # Validate parent comment exists
        if str(parent_comment_id) not in comments:
            return json.dumps({"error": f"Parent comment {parent_comment_id} not found"})
        
        # Find reply comments
        reply_comments = []
        for comment in comments.values():
            if comment.get("parent_comment_id") == parent_comment_id:
                reply_comments.append(comment)
        
        return json.dumps(reply_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_parent",
                "description": "Get all reply comments to a parent comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_comment_id": {"type": "string", "description": "ID of the parent comment to get replies for"}
                    },
                    "required": ["parent_comment_id"]
                }
            }
        }
