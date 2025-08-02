import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateAttachment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filename: str, original_filename: str, 
               mime_type: str, file_size: int, storage_path: str, uploaded_by: str,
               storage_type: str = None, version: str = None, page_id: Optional[str] = None, 
               comment_id: Optional[str] = None) -> str:
        attachments = data.get("attachments", {})
        users = data.get("users", {})
        
        if uploaded_by not in users:
            raise ValueError("User not found")
        
        if page_id:
            pages = data.get("pages", {})
            if page_id not in pages:
                raise ValueError("Page not found")
        
        if comment_id:
            comments = data.get("comments", {})
            if comment_id not in comments:
                raise ValueError("Comment not found")
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return 1
            return (max(int(k) for k in table.keys()) + 1)
        
        attachment_id = generate_id(attachments)
        
        new_attachment = {
            "id": attachment_id,
            "page_id": page_id,
            "comment_id": comment_id,
            "filename": filename,
            "original_filename": original_filename,
            "mime_type": mime_type,
            "file_size": file_size,
            "storage_path": storage_path,
            "storage_type": storage_type,
            "version": version,
            "uploaded_by": uploaded_by,
            "created_at": "2025-07-01T00:00:00Z",
        }
        
        attachments[str(attachment_id)] = new_attachment
        
        return json.dumps({"attachment_id": attachment_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_attachment",
                "description": "Create a new attachment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page (optional)"
                        },
                        "comment_id": {
                            "type": "string",
                            "description": "The ID of the comment (optional)"
                        },
                        "filename": {
                            "type": "string",
                            "description": "The filename of the attachment"
                        },
                        "original_filename": {
                            "type": "string",
                            "description": "The original filename"
                        },
                        "mime_type": {
                            "type": "string",
                            "description": "The MIME type of the file"
                        },
                        "file_size": {
                            "type": "integer",
                            "description": "The size of the file in bytes"
                        },
                        "storage_path": {
                            "type": "string",
                            "description": "The storage path of the file"
                        },
                        "storage_type": {
                            "type": "string",
                            "description": "The type of storage (optional)"
                        },
                        "version": {
                            "type": "string",
                            "description": "The version of the attachment"
                        },
                        "uploaded_by": {
                            "type": "string",
                            "description": "The ID of the user uploading the attachment"
                        }
                    },
                    "required": ["filename", "original_filename", "mime_type", "file_size", "storage_path", "uploaded_by"]
                }
            }
        }
