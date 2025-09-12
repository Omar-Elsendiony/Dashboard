import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, requesting_user_id: str,
               comment_text: str, parent_comment_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        comments = data.get("comments", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"success": False, "error": f"Page {page_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        # Validate parent comment if provided
        if parent_comment_id and str(parent_comment_id) not in comments:
            return json.dumps({"success": False, "error": f"Parent comment {parent_comment_id} not found"})
        
        page = pages[str(page_id)]
        user = users[str(requesting_user_id)]
        space_id = page.get("space_id")
        
        # Check permissions - user needs view permission to comment
        has_permission = False
        
        # Check if user is Platform Owner
        if user.get("role") == "PlatformOwner":
            has_permission = True
        
        # Check page-level permissions
        else:
            for perm in page_permissions.values():
                if (perm.get("page_id") == page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["view", "edit", "admin"]):
                    has_permission = True
                    break
        
        # Check space-level permissions if no page-level permissions
        if not has_permission and space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["view", "contribute", "moderate"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to comment on page"})
        
        # Calculate thread level
        thread_level = 0
        if parent_comment_id:
            parent_comment = comments[str(parent_comment_id)]
            thread_level = parent_comment.get("thread_level", 0) + 1
        
        # Create comment
        comment_id = str(generate_id(comments))
        timestamp = "2025-10-01T00:00:00"
        
        new_comment = {
            "comment_id": int(comment_id),
            "page_id": page_id,
            "parent_comment_id": parent_comment_id,
            "content": comment_text,
            "content_format": "wiki",
            "status": "active",
            "thread_level": thread_level,
            "created_at": timestamp,
            "updated_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        comments[comment_id] = new_comment
        
        return json.dumps({
            "comment_id": comment_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_comment",
                "description": "Add a comment to a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to comment on"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user adding the comment"},
                        "comment_text": {"type": "string", "description": "Content of the comment"},
                        "parent_comment_id": {"type": "string", "description": "ID of parent comment if replying (optional)"}
                    },
                    "required": ["page_id", "requesting_user_id", "comment_text"]
                }
            }
        }
