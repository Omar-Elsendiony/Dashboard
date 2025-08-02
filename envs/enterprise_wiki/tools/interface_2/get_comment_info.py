import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: int) -> str:
        comments = data.get("comments", {})
        comment = comments.get(str(comment_id))
        if not comment:
            raise ValueError("Comment not found")
        return json.dumps(comment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comment_info",
                "description": "Get comment information given the id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "integer", "description": "ID of the comment"}
                    },
                    "required": ["comment_id"]
                }
            }
        }
