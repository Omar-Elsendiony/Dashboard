import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AttachFile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], target_type: str, target_id: str, requesting_user_id: str,
               file_name: str, file_content: bytes, file_size_bytes: int) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        pages = data.get("pages", {})
        comments = data.get("comments", {})
        attachments = data.get("attachments", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        # Validate target type
        if target_type not in ["page", "comment"]:
            return json.dumps({"error": "Target type must be 'page' or 'comment'"})
        
        # Validate target exists and check permissions
        if target_type == "page":
            if str(target_id) not in pages:
                return json.dumps({"error": f"Page {target_id} not found"})
            
            page = pages[str(target_id)]
            space_id = page.get("space_id")
            
            # Check if user can edit the page
            has_permission = False
            
            # Check page permissions
            for perm in page_permissions.values():
                if (perm.get("page_id") == target_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["edit", "admin"]):
                    has_permission = True
                    break
            
            # Check space permissions
            if not has_permission:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") in ["contribute", "moderate"]):
                        has_permission = True
                        break
            
            if not has_permission:
                return json.dumps({"error": "Insufficient permissions to attach file to page"})
        
        elif target_type == "comment":
            if str(target_id) not in comments:
                return json.dumps({"error": f"Comment {target_id} not found"})
            
            comment = comments[str(target_id)]
            if comment.get("created_by_user_id") != requesting_user_id:
                return json.dumps({"error": "Can only attach files to your own comments"})
        
        # Create attachment
        attachment_id = generate_id(attachments)
        timestamp = "2025-10-01T00:00:00"
        
        new_attachment = {
            "attachment_id": attachment_id,
            "page_id": target_id if target_type == "page" else None,
            "comment_id": target_id if target_type == "comment" else None,
            "filename": file_name,
            "original_filename": file_name,
            "mime_type": "application/octet-stream",
            "file_size": file_size_bytes,
            "storage_path": f"/attachments/{attachment_id}/{file_name}",
            "storage_type": "local",
            "version": 1,
            "created_at": timestamp,
            "uploaded_by_user_id": requesting_user_id
        }
        
        attachments[str(attachment_id)] = new_attachment
        
        return json.dumps({"attachment_id": str(attachment_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "attach_file",
                "description": "Attach a file to a page or comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_type": {"type": "string", "description": "Type of target (page or comment)"},
                        "target_id": {"type": "string", "description": "ID of the page or comment"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user attaching the file"},
                        "file_name": {"type": "string", "description": "Name of the file"},
                        "file_content": {"type": "string", "description": "File content"},
                        "file_size_bytes": {"type": "integer", "description": "Size of file in bytes"}
                    },
                    "required": ["target_type", "target_id", "requesting_user_id", "file_name", "file_content", "file_size_bytes"]
                }
            }
        }
