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
        
        # Validate space_id format and existence
        try:
            space_id_int = int(space_id)
        except ValueError:
            raise ValueError("Invalid space_id format")
        
        if space_id not in spaces:
            raise ValueError("Space not found")
        
        if created_by not in users:
            raise ValueError("User not found")
        
        # Validate parent_id if provided
        parent_id_int = None
        if parent_id is not None:
            try:
                parent_id_int = int(parent_id)
            except ValueError:
                raise ValueError("Invalid parent_id format")
            
            if parent_id not in pages:
                raise ValueError("Parent page not found")
        
        # Validate template_id if provided
        template_id_int = None
        if template_id is not None:
            try:
                template_id_int = int(template_id)
            except ValueError:
                raise ValueError("Invalid template_id format")
        
        # Validate content_format
        valid_formats = ["markdown", "html", "plain_text", "wiki"]
        if content_format not in valid_formats:
            raise ValueError(f"Invalid content_format. Must be one of: {', '.join(valid_formats)}")
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        page_id = str(generate_id(pages))
        new_page = {
            "id": int(page_id),
            "space_id": space_id_int,
            "title": title,
            "content": content,
            "content_format": content_format,
            "created_by": created_by,
            "parent_id": parent_id_int,
            "template_id": template_id_int
        }
        
        pages[str(page_id)] = new_page
        
        return json.dumps(new_page)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_page",
                "description": "Create a new page in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "The ID of the space (must be a valid integer as string)"
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
                            "description": "The format of the content (markdown, html, plain_text, or wiki)"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "The ID of the user creating the page"
                        },
                        "parent_id": {
                            "type": "string",
                            "description": "The ID of the parent page (optional, must be a valid integer as string)"
                        },
                        "template_id": {
                            "type": "string",
                            "description": "The ID of the template to use (optional, must be a valid integer as string)"
                        }
                    },
                    "required": ["space_id", "title", "content", "content_format", "created_by"]
                }
            }
        }
