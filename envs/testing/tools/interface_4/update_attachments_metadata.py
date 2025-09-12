import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateAttachmentsMetadata(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               filter_page_id: Optional[str] = None, filter_uploader_id: Optional[str] = None,
               filter_mime_type: Optional[str] = None, update_filename: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        attachments = data.get("attachments", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        updated_attachments = []
        
        for attachment_id, attachment in attachments.items():
            # Apply filters
            if filter_page_id and attachment.get("page_id") != filter_page_id:
                continue
            if filter_uploader_id and attachment.get("uploaded_by_user_id") != filter_uploader_id:
                continue
            if filter_mime_type and attachment.get("mime_type") != filter_mime_type:
                continue
            
            # Check permissions for this attachment
            has_permission = False
            
            # Platform Owner can update any attachment
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            # Uploader can update their own attachment
            elif attachment.get("uploaded_by_user_id") == requesting_user_id:
                has_permission = True
            # Page admin or space admin can update attachments on their pages
            elif attachment.get("page_id"):
                page_id = attachment.get("page_id")
                if str(page_id) in pages:
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
            
            # Apply updates
            if update_filename:
                attachment["filename"] = update_filename
            
            updated_attachments.append(attachment)
        
        return json.dumps(updated_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_attachments_metadata",
                "description": "Update attachment metadata based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "filter_page_id": {"type": "string", "description": "Filter by page ID"},
                        "filter_uploader_id": {"type": "string", "description": "Filter by uploader ID"},
                        "filter_mime_type": {"type": "string", "description": "Filter by MIME type"},
                        "update_filename": {"type": "string", "description": "New filename to set"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }