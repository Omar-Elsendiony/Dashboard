import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentsByComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str) -> str:
        
        attachments = data.get("attachments", {})
        comments = data.get("comments", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        # Find attachments for the comment
        comment_attachments = []
        for attachment in attachments.values():
            if attachment.get("comment_id") == comment_id:
                comment_attachments.append(attachment)
        
        return json.dumps(comment_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments_by_comment",
                "description": "Get all attachments on a specific comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to get attachments for"}
                    },
                    "required": ["comment_id"]
                }
            }
        }
