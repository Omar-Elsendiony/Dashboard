import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTemplateById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str) -> str:
        
        templates = data.get("page_templates", {})
        
        # Validate template exists
        if str(template_id) not in templates:
            return json.dumps({"error": f"Template {template_id} not found"})
        
        template = templates[str(template_id)]
        
        return json.dumps(template)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_template_by_id",
                "description": "Get a single template record by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template to retrieve"}
                    },
                    "required": ["template_id"]
                }
            }
        }
