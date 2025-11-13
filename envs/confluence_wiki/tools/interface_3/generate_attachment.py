import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GenerateAttachment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        content_id: str,
        content_type: str,
        file_name: str,
        file_url: str,
        uploaded_by: str,
        host_page_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Creates a new attachment record.
        """

        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-11-13T12:00:00"
        attachments = data.get("attachments", {})
        users = data.get("users", {})
        pages = data.get("pages", {})
        databases = data.get("databases", {})
        whiteboards = data.get("whiteboards", {})
        smart_links = data.get("smart_links", {})

        # Validate required parameters
        if not all([content_id, content_type, file_name, file_url, uploaded_by]):
            return json.dumps(
                {
                    "error": "Missing required parameters: content_id, content_type, file_name, file_url, and uploaded_by are required"
                }
            )

        # Validate content_type
        valid_content_types = ["page", "database", "whiteboard", "smart_link"]
        if content_type not in valid_content_types:
            return json.dumps(
                {
                    "error": f"Invalid content_type '{content_type}'. Must be one of: {', '.join(valid_content_types)}"
                }
            )

        # Validate content exists based on content_type
        if content_type == "page" and content_id not in pages:
            return json.dumps({"error": f"Page with ID '{content_id}' not found"})
        elif content_type == "database" and content_id not in databases:
            return json.dumps({"error": f"Database with ID '{content_id}' not found"})
        elif content_type == "whiteboard" and content_id not in whiteboards:
            return json.dumps({"error": f"Whiteboard with ID '{content_id}' not found"})
        elif content_type == "smart_link" and content_id not in smart_links:
            return json.dumps({"error": f"Smart link with ID '{content_id}' not found"})

        # Validate uploaded_by user exists
        if uploaded_by not in users:
            return json.dumps({"error": f"User with ID '{uploaded_by}' not found"})

        # Validate host_page_id if provided
        if host_page_id and host_page_id not in pages:
            return json.dumps(
                {"error": f"Parent page with ID '{host_page_id}' not found"}
            )

        # Validate status if provided
        valid_statuses = ["current", "archived", "deleted"]
        if status and status not in valid_statuses:
            return json.dumps(
                {
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                }
            )

        # Generate new attachment ID
        new_attachment_id = generate_id(attachments)

        # Create new attachment record
        new_attachment = {
            "attachment_id": new_attachment_id,
            "content_id": content_id,
            "content_type": content_type,
            "host_page_id": host_page_id,
            "file_name": file_name,
            "file_url": file_url,
            "status": status if status else "current",
            "uploaded_by": uploaded_by,
            "uploaded_at": timestamp,
            "updated_at": timestamp,
        }

        attachments[new_attachment_id] = new_attachment

        return json.dumps(new_attachment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_attachment",
                "description": "Creates a new attachment record for a content item (page, database, whiteboard, or smart_link).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content_id": {
                            "type": "string",
                            "description": "ID of the content item this attachment belongs to (required)",
                        },
                        "content_type": {
                            "type": "string",
                            "description": "Type of content: 'page', 'database', 'whiteboard', or 'smart_link' (required)",
                        },
                        "file_name": {
                            "type": "string",
                            "description": "Name of the attached file (required)",
                        },
                        "file_url": {
                            "type": "string",
                            "description": "URL or path to the attached file (required)",
                        },
                        "uploaded_by": {
                            "type": "string",
                            "description": "User ID of the person uploading the attachment (required)",
                        },
                        "host_page_id": {
                            "type": "string",
                            "description": "ID of the parent page if applicable (optional)",
                        },
                        "status": {
                            "type": "string",
                            "description": "Attachment status: 'current', 'archived', or 'deleted' (optional, defaults to 'current')",
                        },
                    },
                    "required": [
                        "content_id",
                        "content_type",
                        "file_name",
                        "file_url",
                        "uploaded_by",
                    ],
                },
            },
        }
