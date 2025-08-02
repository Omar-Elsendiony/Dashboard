import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateCommentStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: int, status: str) -> str:
        comments = data.get("comments", {})
        comment = comments.get(str(comment_id))
        if not comment:
            raise ValueError("Comment not found")
        
        valid_statuses = ["active", "deleted", "resolved"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        comment["status"] = status
        # set_updated_at("comments", comment_id, data)
        comment["updated_at"] = None
        return json.dumps(comment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_comment_status",
                "description": "Update comment status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "integer", "description": "ID of the comment"},
                        "status": {"type": "string", "description": "New status for the comment"}
                    },
                    "required": ["comment_id", "status"]
                }
            }
        }
