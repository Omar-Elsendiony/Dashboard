import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGlobalTemplates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        
        templates = data.get("page_templates", {})
        
        # Find all global templates
        global_templates = []
        for template in templates.values():
            if template.get("is_global") is True:
                global_templates.append(template)
        
        return json.dumps(global_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_global_templates",
                "description": "Get all global templates",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
