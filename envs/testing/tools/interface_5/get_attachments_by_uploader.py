import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentsByUploader(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], uploaded_by_user_id: str) -> str:
        
        attachments = data.get("attachments", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(uploaded_by_user_id) not in users:
            return json.dumps({"error": f"User {uploaded_by_user_id} not found"})
        
        # Find attachments uploaded by the user
        user_attachments = []
        for attachment in attachments.values():
            if attachment.get("uploaded_by_user_id") == uploaded_by_user_id:
                user_attachments.append(attachment)
        
        return json.dumps(user_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments_by_uploader",
                "description": "Get all attachments uploaded by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uploaded_by_user_id": {"type": "string", "description": "ID of the user to get attachments for"}
                    },
                    "required": ["uploaded_by_user_id"]
                }
            }
        }
