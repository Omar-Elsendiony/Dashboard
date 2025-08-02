import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreatePageTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, description: str, content: str, 
               content_format: str, space_id: str, category: str, created_by: str) -> str:
        page_templates = data.get("page_templates", {})
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        if space_id not in spaces:
            raise ValueError("Space not found")
        
        if created_by not in users:
            raise ValueError("User not found")
        
        # template_id = str(uuid.uuid4())
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return 1
            return (max(int(k) for k in table.keys()) + 1)
        
        template_id = generate_id(page_templates)
        
        new_template = {
            "id": template_id,
            "name": name,
            "description": description,
            "content": content,
            "content_format": content_format,
            "space_id": space_id,
            "category": category,
            "created_by": created_by
        }
        
        page_templates[str(template_id)] = new_template
        
        return json.dumps(new_template)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_page_template",
                "description": "Create a new page template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the template"
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the template"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content of the template"
                        },
                        "content_format": {
                            "type": "string",
                            "description": "The format of the content"
                        },
                        "space_id": {
                            "type": "string",
                            "description": "The ID of the space"
                        },
                        "category": {
                            "type": "string",
                            "description": "The category of the template"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "The ID of the user creating the template"
                        }
                    },
                    "required": ["name", "description", "content", "content_format", "space_id", "category", "created_by"]
                }
            }
        }
