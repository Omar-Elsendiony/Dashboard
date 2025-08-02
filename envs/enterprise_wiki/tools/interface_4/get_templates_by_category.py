import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTemplatesByCategory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category: str) -> str:
        templates = data.get("page_templates", {})
        result = [tpl for tpl in templates.values() if tpl.get("category") == category]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_templates_by_category",
                "description": "Get page templates by category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Template category"},
                    },
                    "required": ["category"]
                }
            }
        }
