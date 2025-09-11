import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        attachments = data.get("attachments", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find attachments for the page
        page_attachments = []
        for attachment in attachments.values():
            if attachment.get("page_id") == page_id:
                page_attachments.append(attachment)
        
        return json.dumps(page_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments_by_page",
                "description": "Get all attachments on a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to get attachments for"}
                    },
                    "required": ["page_id"]
                }
            }
        }
