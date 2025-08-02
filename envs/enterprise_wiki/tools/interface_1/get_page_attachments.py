import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageAttachments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        attachments = data.get("attachments", {})
        pages = data.get("pages", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        page_attachments = []
        for attachment_id, attachment in attachments.items():
            if str(attachment.get("page_id")) == str(page_id):
                page_attachments.append(attachment)
        
        return json.dumps(page_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_attachments",
                "description": "Get all attachments for a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page"
                        }
                    },
                    "required": ["page_id"]
                }
            }
        }
