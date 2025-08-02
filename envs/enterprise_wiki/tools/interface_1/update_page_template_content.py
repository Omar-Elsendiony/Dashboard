import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdatePageTemplateContent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str, content: str, content_format: str) -> str:
        page_templates = data.get("page_templates", {})
        
        if template_id not in page_templates:
            raise ValueError("Template not found")
        
        template = page_templates[template_id]
        template["content"] = content
        template["content_format"] = content_format
        
        return json.dumps(template)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_page_template_content",
                "description": "Update template content with the ability to change the format of the content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "description": "The ID of the template to update"
                        },
                        "content": {
                            "type": "string",
                            "description": "The new content"
                        },
                        "content_format": {
                            "type": "string",
                            "description": "The format of the content"
                        }
                    },
                    "required": ["template_id", "content"]
                }
            }
        }
