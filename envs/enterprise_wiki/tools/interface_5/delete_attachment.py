import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteAttachment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: int) -> str:
        attachments = data.get("attachments", {})
        attachment_key = str(attachment_id)

        if attachment_key not in attachments:
            raise ValueError("Attachment not found")

        deleted_attachment = attachments.pop(attachment_key)
        return json.dumps({"status": "deleted", "deleted_attachment": deleted_attachment})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_attachment",
                "description": "Delete an attachment by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "integer", "description": "ID of the attachment to delete"}
                    },
                    "required": ["attachment_id"]
                }
            }
        }
