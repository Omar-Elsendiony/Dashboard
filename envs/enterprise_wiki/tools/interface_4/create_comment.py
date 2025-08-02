import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateComment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: int,
        content: str,
        created_by: int,
        content_format: str = "markdown",
        parent_id: Optional[int] = None
    ) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Validate page
        pages = data.get("pages", {})
        if str(page_id) not in pages:
            raise ValueError("Page not found")
        
        # Validate user
        users = data.get("users", {})
        if str(created_by) not in users:
            raise ValueError("User not found")
        
        # Validate parent comment if exists
        if parent_id:
            comments = data.get("comments", {})
            if str(parent_id) not in comments:
                raise ValueError("Parent comment not found")
        
        # Create new comment
        comments = data.setdefault("comments", {})
        new_id = generate_id(comments)
        
        thread_level = 0
        if parent_id:
            # Calculate thread level based on parent
            parent = comments[str(parent_id)]
            thread_level = parent.get("thread_level", 0) + 1

        created_at = updated_at = "2025-07-01T00:00:00Z"


        new_comment = {
            "id": new_id,
            "page_id": page_id,
            "parent_id": parent_id,
            "content": content,
            "content_format": content_format,
            "status": "active",
            "thread_level": thread_level,
            "created_at": created_at,
            "updated_at": updated_at,
            "created_by": created_by
        }
        
        comments[str(new_id)] = new_comment
        return json.dumps(new_comment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_comment",
                "description": "Create a new comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "integer", "description": "ID of the page"},
                        "content": {"type": "string", "description": "Content of the comment"},
                        "created_by": {"type": "integer", "description": "ID of the user creating the comment"},
                        "content_format": {"type": "string", "description": "Format of the content which can be only (markdown, html, wiki)"},
                        "parent_id": {"type": "integer", "description": "ID of the parent comment if replying"}
                    },
                    "required": ["page_id", "content", "created_by"]
                }
            }
        }
