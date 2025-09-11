import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        
        comments = data.get("comments", {})
        
        # Validate status
        valid_statuses = ['active', 'deleted', 'resolved']
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find comments with the specified status
        status_comments = []
        for comment in comments.values():
            if comment.get("status") == status:
                status_comments.append(comment)
        
        return json.dumps(status_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_status",
                "description": "Get all comments with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Status of comments to retrieve (active, deleted, resolved)"}
                    },
                    "required": ["status"]
                }
            }
        }
