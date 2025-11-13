import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeleteAttachment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        attachment_id: str,
    ) -> str:
        """
        Removes an attachment record by setting its status to 'deleted'.
        """
        timestamp = "2025-11-13T12:00:00"
        attachments = data.get("attachments", {})

        # Validate required parameters
        if not attachment_id:
            return json.dumps(
                {"error": "Missing required parameter: attachment_id is required"}
            )

        # Check if attachment exists
        if attachment_id not in attachments:
            return json.dumps(
                {"error": f"Attachment with ID '{attachment_id}' not found"}
            )

        attachment_to_remove = attachments[attachment_id]

        # Mark as deleted
        attachment_to_remove["status"] = "deleted"
        attachment_to_remove["updated_at"] = timestamp

        return json.dumps(attachment_to_remove)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_attachment",
                "description": "Removes an attachment record by setting its status to 'deleted'. This is a soft delete operation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {
                            "type": "string",
                            "description": "ID of the attachment to remove (required)",
                        }
                    },
                    "required": ["attachment_id"],
                },
            },
        }
