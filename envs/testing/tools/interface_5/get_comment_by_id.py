import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str) -> str:
        
        comments = data.get("comments", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        comment = comments[str(comment_id)]
        
        return json.dumps(comment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comment_by_id",
                "description": "Get a comment by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to retrieve"}
                    },
                    "required": ["comment_id"]
                }
            }
        }
