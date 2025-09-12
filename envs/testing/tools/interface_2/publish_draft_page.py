import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PublishDraftPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], draft_page_id: str, requesting_user_id: str,
               publish_confirmation: bool) -> str:
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate page exists
        if str(draft_page_id) not in pages:
            return json.dumps({"success": False, "error": f"Draft page {draft_page_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        draft_page = pages[str(draft_page_id)]
        user = users[str(requesting_user_id)]
        
        # Check if page is actually a draft
        if draft_page.get("status") != "draft":
            return json.dumps({"success": False, "error": "Page is not a draft"})
        
        # Validate confirmation
        if not publish_confirmation:
            return json.dumps({"success": False, "error": "Publish confirmation required"})
        
        space_id = draft_page.get("space_id")
        
        # Check permissions
        has_permission = False
        
        # Check if user is Platform Owner
        if user.get("role") == "PlatformOwner":
            has_permission = True
        
        # Check if user is the page creator
        elif draft_page.get("created_by_user_id") == requesting_user_id:
            has_permission = True
        
        # Check if user has edit permission on the page
        else:
            for perm in page_permissions.values():
                if (perm.get("page_id") == draft_page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["edit", "admin"]):
                    has_permission = True
                    break
        
        # Check space-level permissions if no page-level permissions
        if not has_permission and space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["contribute", "moderate"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to publish page"})
        
        # Update page status
        timestamp = "2025-10-01T00:00:00"
        draft_page["status"] = "current"
        draft_page["updated_at"] = timestamp
        draft_page["published_at"] = timestamp
        draft_page["last_modified_by_user_id"] = requesting_user_id
        
        return json.dumps({
            "success": True,
            "message": "Draft published",
            "page_id": draft_page_id,
            "status": "current"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "publish_draft_page",
                "description": "Publish a draft page to make it current",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "draft_page_id": {"type": "string", "description": "ID of the draft page to publish"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user publishing the page"},
                        "publish_confirmation": {"type": "boolean", "description": "Confirmation flag for publishing intent (True/False)"}
                    },
                    "required": ["draft_page_id", "requesting_user_id", "publish_confirmation"]
                }
            }
        }
