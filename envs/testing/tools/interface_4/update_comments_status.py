import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateCommentsStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, new_status: str,
               filter_page_id: Optional[str] = None, filter_creator_id: Optional[str] = None,
               filter_current_status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        comments = data.get("comments", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Validate enum values
        if filter_current_status and filter_current_status not in ["active", "deleted", "resolved"]:
            return json.dumps({"error": "Invalid filter_current_status. Must be one of: active, deleted, resolved"})
        
        if new_status not in ["active", "deleted", "resolved"]:
            return json.dumps({"error": "Invalid new_status. Must be one of: active, deleted, resolved"})
        
        updated_comments = []
        timestamp = "2025-10-01T00:00:00"
        
        for comment_id, comment in comments.items():
            # Apply filters
            if filter_page_id and comment.get("page_id") != filter_page_id:
                continue
            if filter_creator_id and comment.get("created_by_user_id") != filter_creator_id:
                continue
            if filter_current_status and comment.get("status") != filter_current_status:
                continue
            
            # Check permissions for this comment
            has_permission = False
            page_id = comment.get("page_id")
            
            # Platform Owner can update any comment
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            # Comment creator can update their own comment
            elif comment.get("created_by_user_id") == requesting_user_id:
                has_permission = True
            # Page admin or space admin can moderate comments
            elif page_id and str(page_id) in pages:
                page = pages[str(page_id)]
                space_id = page.get("space_id")
                
                # Check page admin permission
                for perm in page_permissions.values():
                    if (perm.get("page_id") == page_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "admin"):
                        has_permission = True
                        break
                
                # Check space admin permission
                if not has_permission:
                    for perm in space_permissions.values():
                        if (perm.get("space_id") == space_id and 
                            perm.get("user_id") == requesting_user_id and 
                            perm.get("permission_type") == "moderate"):
                            has_permission = True
                            break
            
            if not has_permission:
                continue
            
            # Apply update
            comment["status"] = new_status
            comment["updated_at"] = timestamp
            updated_comments.append(comment)
        
        return json.dumps(updated_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_comments_status",
                "description": "Update comment status based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "new_status": {"type": "string", "description": "New status to set (active, deleted, resolved)"},
                        "filter_page_id": {"type": "string", "description": "Filter by page ID"},
                        "filter_creator_id": {"type": "string", "description": "Filter by creator ID"},
                        "filter_current_status": {"type": "string", "description": "Filter by current status (active, deleted, resolved)"}
                    },
                    "required": ["requesting_user_id", "new_status"]
                }
            }
        }