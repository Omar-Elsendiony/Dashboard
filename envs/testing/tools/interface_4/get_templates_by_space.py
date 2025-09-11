import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTemplatesBySpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        
        templates = data.get("page_templates", {})
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find all templates in the space
        space_templates = []
        for template in templates.values():
            if template.get("space_id") == space_id:
                space_templates.append(template)
        
        return json.dumps(space_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_templates_by_space",
                "description": "Get all templates in a specific space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"}
                    },
                    "required": ["space_id"]
                }
            }
        }
