import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByFilters(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str = None,
        status: str = None,
        content_format: str = None,
        created_by: str = None,
        last_modified_by: str = None,
        space_id: str = None
    ) -> str:
        pages = data.get("pages", {}).values()

        if all(param is None for param in [title, status, content_format, created_by, last_modified_by, space_id]):
            raise ValueError("At least one filter must be provided")

        result = [
            page for page in pages
            if (title is None or title.lower() in page.get("title", "").lower())
            and (status is None or page.get("status") == status)
            and (content_format is None or page.get("content_format") == content_format)
            and (created_by is None or str(page.get("created_by")) == str(created_by))
            and (last_modified_by is None or str(page.get("last_modified_by")) == str(last_modified_by))
            and (space_id is None or str(page.get("space_id")) == str(space_id))
        ]

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_filters",
                "description": "Get pages filtered by title, status, content format, creator, or last modifier",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Filter pages whose title contains this text"},
                        "status": {"type": "string", "description": "Filter by exact page status"},
                        "content_format": {"type": "string", "description": "Filter by content format (e.g., markdown, html)"},
                        "created_by": {"type": "string", "description": "Filter by user ID who created the page"},
                        "last_modified_by": {"type": "string", "description": "Filter by user ID who last modified the page"},
                        "space_id": {"type": "string", "description": "Filter by space ID that contains the page"}
                    }
                },
                "required": []
            }
        }
