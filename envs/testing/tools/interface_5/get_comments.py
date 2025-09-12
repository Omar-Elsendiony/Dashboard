import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetComments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: Optional[str] = None, page_id: Optional[str] = None,
               parent_comment_id: Optional[str] = None, creator_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        comments = data.get("comments", {})
        result = []
        
        for cid, comment in comments.items():
            # Apply filters
            if comment_id and str(comment_id) != cid:
                continue
            if page_id and comment.get("page_id") != page_id:
                continue
            if parent_comment_id and comment.get("parent_comment_id") != parent_comment_id:
                continue
            if creator_id and comment.get("created_by_user_id") != creator_id:
                continue
            if status and comment.get("status") != status:
                continue
            
            result.append({
                "comment_id": cid,
                "page_id": comment.get("page_id"),
                "parent_comment_id": comment.get("parent_comment_id"),
                "content": comment.get("content"),
                "content_format": comment.get("content_format"),
                "status": comment.get("status"),
                "thread_level": comment.get("thread_level"),
                "created_at": comment.get("created_at"),
                "updated_at": comment.get("updated_at"),
                "created_by_user_id": comment.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments",
                "description": "Get comments matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment"},
                        "page_id": {"type": "string", "description": "ID of the page containing the comment"},
                        "parent_comment_id": {"type": "string", "description": "ID of the parent comment"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the comment"},
                        "status": {"type": "string", "description": "Status of comment (active, deleted, resolved)"}
                    },
                    "required": []
                }
            }
        }
