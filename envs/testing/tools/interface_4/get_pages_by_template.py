import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str) -> str:
        
        pages = data.get("pages", {})
        templates = data.get("page_templates", {})
        
        # Validate template exists
        if str(template_id) not in templates:
            return json.dumps({"error": f"Template {template_id} not found"})
        
        # Find all pages using the template
        template_pages = []
        for page in pages.values():
            if page.get("template_id") == template_id:
                template_pages.append(page)
        
        return json.dumps(template_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_template",
                "description": "Get all pages using a specific template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template"}
                    },
                    "required": ["template_id"]
                }
            }
        }
