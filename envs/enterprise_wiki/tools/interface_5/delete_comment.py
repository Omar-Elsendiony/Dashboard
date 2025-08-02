

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: int) -> str:
        comments = data.get("comments", {})
        comment_key = str(comment_id)

        if comment_key not in comments:
            raise ValueError("Comment not found")

        deleted_comment = comments.pop(comment_key)
        return json.dumps({"status": "deleted", "deleted_comment": deleted_comment})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_comment",
                "description": "Delete a specific comment by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "integer", "description": "ID of the comment to delete"}
                    },
                    "required": ["comment_id"]
                }
            }
        }
