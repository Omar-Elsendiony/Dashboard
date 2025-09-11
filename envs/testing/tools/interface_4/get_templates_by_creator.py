import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTemplatesByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        templates = data.get("page_templates", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find all templates created by the user
        user_templates = []
        for template in templates.values():
            if template.get("created_by_user_id") == created_by_user_id:
                user_templates.append(template)
        
        return json.dumps(user_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_templates_by_creator",
                "description": "Get all templates created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the templates"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
