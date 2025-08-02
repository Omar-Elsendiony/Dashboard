import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateAttachmentInfo(Tool):

    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: str, **parameters_to_update) -> str:
        IMMUTABLE_FIELDS = {"id", "attachment_id"}
        attachments = data.get("attachments", {})

        if str(attachment_id) not in attachments:
            raise ValueError("Attachment not found")

        attachment = attachments[attachment_id]

        # Apply updates dynamically
        updated = False
        for key, value in parameters_to_update.items():
            if key in IMMUTABLE_FIELDS or value is None:
                continue  # skip immutable or null values
            if key in attachment:  # update only known keys
                attachment[key] = value
                updated = True

        if not updated:
            raise ValueError("No parameters to update")

        return json.dumps(attachment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_attachment_info",
                "description": "Update attachment metadata fields dynamically.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {
                            "type": "string",
                            "description": "The ID of the attachment to update."
                        },
                        "filename": {
                            "type": "string",
                            "description": "New filename."
                        },
                        "original_filename": {
                            "type": "string",
                            "description": "Original filename."
                        },
                        "mime_type": {
                            "type": "string",
                            "description": "MIME type (e.g., 'application/pdf')."
                        },
                        "file_size": {
                            "type": "integer",
                            "description": "File size in bytes."
                        },
                        "storage_path": {
                            "type": "string",
                            "description": "Path in storage."
                        },
                        "storage_type": {
                            "type": "string",
                            "description": "Storage type (e.g., local, S3)."
                        },
                        "image_width": {
                            "type": ["integer", "null"],
                            "description": "Width of the image if applicable."
                        },
                        "image_height": {
                            "type": ["integer", "null"],
                            "description": "Height of the image if applicable."
                        },
                        "version": {
                            "type": "integer",
                            "description": "Version number."
                        },
                        "uploaded_by": {
                            "type": "integer",
                            "description": "User ID of the uploader."
                        }
                    },
                    "required": ["attachment_id"]
                }
            }
        }
