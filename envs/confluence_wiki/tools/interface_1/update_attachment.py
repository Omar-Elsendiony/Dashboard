import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateAttachment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        attachment_id: str,
        file_name: Optional[str] = None,
        file_url: Optional[str] = None,
        host_page_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Updates an existing attachment record.
        """
        timestamp = "2025-11-13T12:00:00"
        attachments = data.get("attachments", {})
        pages = data.get("pages", {})

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

        # At least one optional field must be provided
        if not any([file_name, file_url, host_page_id is not None, status]):
            return json.dumps(
                {"error": "At least one field to update must be provided"}
            )

        attachment_to_update = attachments[attachment_id]

        # Validate host_page_id if provided
        if host_page_id and host_page_id not in pages:
            return json.dumps(
                {"error": f"Host page with ID '{host_page_id}' not found"}
            )

        # Validate status if provided
        valid_statuses = ["current", "archived", "deleted"]
        if status and status not in valid_statuses:
            return json.dumps(
                {
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                }
            )

        # Update fields if provided
        if file_name:
            attachment_to_update["file_name"] = file_name
        if file_url:
            attachment_to_update["file_url"] = file_url
        if host_page_id is not None:
            attachment_to_update["host_page_id"] = host_page_id
        if status:
            attachment_to_update["status"] = status

        attachment_to_update["updated_at"] = timestamp

        return json.dumps(attachment_to_update)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_attachment",
                "description": "Updates an existing attachment record. At least one optional field must be provided for update.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {
                            "type": "string",
                            "description": "ID of the attachment to update (required)",
                        },
                        "file_name": {
                            "type": "string",
                            "description": "New file name (optional)",
                        },
                        "file_url": {
                            "type": "string",
                            "description": "New file URL or path (optional)",
                        },
                        "host_page_id": {
                            "type": "string",
                            "description": "New host page ID (optional)",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status: 'current', 'archived', or 'deleted' (optional)",
                        },
                    },
                    "required": ["attachment_id"],
                },
            },
        }
