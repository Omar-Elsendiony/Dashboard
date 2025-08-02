import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SearchPageTemplateByName(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str) -> str:
        page_templates = data.get("page_templates", {})
        
        for template_id, template in page_templates.items():
            if str(template.get("name")) == str(name):
                return json.dumps(template)
        
        raise ValueError("Page template not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_page_template_by_name",
                "description": "Searches templates by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the template to search for"
                        }
                    },
                    "required": ["name"]
                }
            }
        }
