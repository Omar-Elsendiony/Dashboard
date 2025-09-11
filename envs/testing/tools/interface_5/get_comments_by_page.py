import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        comments = data.get("comments", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find comments for the page
        page_comments = []
        for comment in comments.values():
            if comment.get("page_id") == page_id:
                page_comments.append(comment)
        
        return json.dumps(page_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_page",
                "description": "Get all comments on a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to get comments for"}
                    },
                    "required": ["page_id"]
                }
            }
        }
