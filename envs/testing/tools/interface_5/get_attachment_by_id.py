import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: str) -> str:
        
        attachments = data.get("attachments", {})
        
        # Validate attachment exists
        if str(attachment_id) not in attachments:
            return json.dumps({"error": f"Attachment {attachment_id} not found"})
        
        attachment = attachments[str(attachment_id)]
        
        return json.dumps(attachment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachment_by_id",
                "description": "Get an attachment by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "string", "description": "ID of the attachment to retrieve"}
                    },
                    "required": ["attachment_id"]
                }
            }
        }
