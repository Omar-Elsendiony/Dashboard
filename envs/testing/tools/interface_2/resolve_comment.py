import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ResolveComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str, requesting_user_id: str,
               resolution_note: Optional[str] = None, content_owner_approval: Optional[bool] = None,
               space_administrator_approval: Optional[bool] = None) -> str:
        
        comments = data.get("comments", {})
        users = data.get("users", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        comment = comments[str(comment_id)]
        page_id = comment.get("page_id")
        
        # Get page and space info
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        page = pages[str(page_id)]
        space_id = page.get("space_id")
        user = users[str(requesting_user_id)]
        
        # Check authority
        has_authority = False
        
        # Platform Owner can resolve any comment
        if user.get("role") == "PlatformOwner":
            has_authority = True
        
        # Content Owner (page creator or admin permission) can resolve
        elif page.get("created_by_user_id") == requesting_user_id:
            has_authority = content_owner_approval if content_owner_approval is not None else True
        else:
            # Check if user has admin permission on the page
            for perm in page_permissions.values():
                if (perm.get("page_id") == page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "admin"):
                    has_authority = content_owner_approval if content_owner_approval is not None else True
                    break
        
        # Space Administrator can resolve
        if not has_authority:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "moderate"):
                    has_authority = space_administrator_approval if space_administrator_approval is not None else True
                    break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to resolve comment"})
        
        # Update comment status
        comment["status"] = "resolved"
        comment["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Comment resolved", "status": "resolved"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "resolve_comment",
                "description": "Resolve a comment on a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to resolve"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user resolving the comment"},
                        "resolution_note": {"type": "string", "description": "Note about resolution"},
                        "content_owner_approval": {"type": "boolean", "description": "Content Owner approval if user is Content Owner (True/False)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"}
                    },
                    "required": ["comment_id", "requesting_user_id"]
                }
            }
        }
