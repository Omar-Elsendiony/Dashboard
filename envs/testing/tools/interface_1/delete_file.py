import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteFile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: str, requesting_user_id: str,
               target_type: str, target_id: str) -> str:
        
        users = data.get("users", {})
        attachments = data.get("attachments", {})
        pages = data.get("pages", {})
        comments = data.get("comments", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        # Validate attachment exists
        if str(attachment_id) not in attachments:
            return json.dumps({"error": f"Attachment {attachment_id} not found"})
        
        attachment = attachments[str(attachment_id)]
        user = users[str(requesting_user_id)]
        
        # Check authority
        has_authority = False
        
        # Platform Owner can delete any file
        if user.get("role") == "PlatformOwner":
            has_authority = True
        
        # File uploader can delete their own file
        elif attachment.get("uploaded_by_user_id") == requesting_user_id:
            has_authority = True
        
        # Page owner or admin can delete files on their page
        elif target_type == "page" and str(target_id) in pages:
            page = pages[str(target_id)]
            space_id = page.get("space_id")
            
            # Check if user created the page
            if page.get("created_by_user_id") == requesting_user_id:
                has_authority = True
            
            # Check page admin permissions
            if not has_authority:
                for perm in page_permissions.values():
                    if (perm.get("page_id") == target_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "admin"):
                        has_authority = True
                        break
            
            # Check space admin permissions
            if not has_authority:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_authority = True
                        break
        
        # Comment owner can delete files on their comment
        elif target_type == "comment" and str(target_id) in comments:
            comment = comments[str(target_id)]
            if comment.get("created_by_user_id") == requesting_user_id:
                has_authority = True
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to delete file"})
        
        # Delete attachment
        del attachments[str(attachment_id)]
        
        return json.dumps({"success": True, "message": "File deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_file",
                "description": "Delete an attachment file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "string", "description": "ID of the attachment to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user deleting the file"},
                        "target_type": {"type": "string", "description": "Type of target (page or comment)"},
                        "target_id": {"type": "string", "description": "ID of the page or comment"}
                    },
                    "required": ["attachment_id", "requesting_user_id", "target_type", "target_id"]
                }
            }
        }
