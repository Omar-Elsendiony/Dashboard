import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpaceTemplates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        page_templates = data.get("page_templates", {})
        spaces = data.get("spaces", {})
        
        if space_id not in spaces:
            raise ValueError("Space not found")
        
        space_templates = []
        for template_id, template in page_templates.items():
            if str(template.get("space_id")) == str(space_id):
                space_templates.append(template)
        
        return json.dumps(space_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_templates",
                "description": "Get all templates in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "The ID of the space"
                        }
                    },
                    "required": ["space_id"]
                }
            }
        }
