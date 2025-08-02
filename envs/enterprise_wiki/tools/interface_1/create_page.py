import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreatePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, title: str, content: str, content_format: str, 
               created_by: str, parent_id: Optional[str] = None, template_id: Optional[str] = None) -> str:
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        users = data.get("users", {})
        
        if space_id not in spaces:
            raise ValueError("Space not found")
        
        if created_by not in users:
            raise ValueError("User not found")
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        page_id = str(generate_id(pages))
        new_page = {
            "id": int(page_id),
            "space_id": int(space_id),
            "title": title,
            "content": content,
            "content_format": content_format,
            "created_by": created_by,
            "parent_id": int(parent_id) if parent_id is not None else None,
            "template_id": template_id
        }
        
        pages[str(page_id)] = new_page
        
        return json.dumps(new_page)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_page",
                "description": "Create a new page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "The ID of the space"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the page"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content of the page"
                        },
                        "content_format": {
                            "type": "string",
                            "description": "The format of the content"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "The ID of the user creating the page"
                        },
                        "parent_id": {
                            "type": "string",
                            "description": "The ID of the parent page (optional)"
                        },
                        "template_id": {
                            "type": "string",
                            "description": "The ID of the template to use (optional)"
                        }
                    },
                    "required": ["space_id", "title", "content", "content_format", "created_by"]
                }
            }
        }
