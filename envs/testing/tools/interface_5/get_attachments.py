import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAttachments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: Optional[str] = None, page_id: Optional[str] = None,
               comment_id: Optional[str] = None, uploader_id: Optional[str] = None,
               mime_type: Optional[str] = None) -> str:
        
        attachments = data.get("attachments", {})
        result = []
        
        for aid, attachment in attachments.items():
            # Apply filters
            if attachment_id and str(attachment_id) != aid:
                continue
            if page_id and attachment.get("page_id") != page_id:
                continue
            if comment_id and attachment.get("comment_id") != comment_id:
                continue
            if uploader_id and attachment.get("uploaded_by_user_id") != uploader_id:
                continue
            if mime_type and attachment.get("mime_type") != mime_type:
                continue
            
            result.append({
                "attachment_id": aid,
                "page_id": attachment.get("page_id"),
                "comment_id": attachment.get("comment_id"),
                "filename": attachment.get("filename"),
                "original_filename": attachment.get("original_filename"),
                "mime_type": attachment.get("mime_type"),
                "file_size": attachment.get("file_size"),
                "storage_path": attachment.get("storage_path"),
                "storage_type": attachment.get("storage_type"),
                "image_width": attachment.get("image_width"),
                "image_height": attachment.get("image_height"),
                "version": attachment.get("version"),
                "created_at": attachment.get("created_at"),
                "uploaded_by_user_id": attachment.get("uploaded_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments",
                "description": "Get attachments matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "string", "description": "ID of the attachment"},
                        "page_id": {"type": "string", "description": "ID of the page containing the attachment"},
                        "comment_id": {"type": "string", "description": "ID of the comment containing the attachment"},
                        "uploader_id": {"type": "string", "description": "ID of the user who uploaded the attachment"},
                        "mime_type": {"type": "string", "description": "MIME type of the attachment"}
                    },
                    "required": []
                }
            }
        }
