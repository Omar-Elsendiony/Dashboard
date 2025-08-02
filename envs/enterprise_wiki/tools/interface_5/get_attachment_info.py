import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: str) -> str:
        attachments = data.get("attachments", {})
        attachment = attachments.get(attachment_id)
        if not attachment:
            raise ValueError("Attachment not found")
        return json.dumps(attachment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachment_info",
                "description": "Fetch information about a specific attachment given the ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "string", "description": "Attachment ID"},
                    },
                    "required": ["attachment_id"]
                }
            }
        }


