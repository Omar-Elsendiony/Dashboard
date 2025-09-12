import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str, requesting_user_id: str) -> str:
        
        users = data.get("users", {})
        comments = data.get("comments", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": "Comment not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        comment = comments[str(comment_id)]
        requesting_user = users[str(requesting_user_id)]
        page_id = comment.get("page_id")
        
        # Check authority
        has_authority = False
        
        # Platform Owner can delete any comment
        if requesting_user.get("role") == "PlatformOwner":
            has_authority = True
        
        # Comment creator can delete their own comment
        elif comment.get("created_by_user_id") == requesting_user_id:
            has_authority = True
        
        # Page admin or space admin can delete comments on their pages
        elif page_id and str(page_id) in pages:
            page = pages[str(page_id)]
            space_id = page.get("space_id")
            
            # Check page admin permission
            for perm in page_permissions.values():
                if (perm.get("page_id") == page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "admin"):
                    has_authority = True
                    break
            
            # Check space admin permission
            if not has_authority:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_authority = True
                        break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to delete comment"})
        
        # Check for child comments
        child_comments = []
        for c in comments.values():
            if c.get("parent_comment_id") == comment_id:
                child_comments.append(c)
        
        if child_comments:
            return json.dumps({"error": "Cannot delete comment with replies. Delete child comments first"})
        
        # Delete the comment
        del comments[str(comment_id)]
        
        return json.dumps({"success": True, "message": "Comment deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_comment",
                "description": "Delete a comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user deleting the comment"}
                    },
                    "required": ["comment_id", "requesting_user_id"]
                }
            }
        }