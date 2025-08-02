import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGlobalTemplates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        templates = data.get("page_templates", {})
        global_templates = [tpl for tpl in templates.values() if tpl.get("is_global")]
        return json.dumps(global_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_global_templates",
                "description": "Get all global page templates",
                "parameters": {"type": "object", "properties": {}},
                "required": []
            }
        }
    