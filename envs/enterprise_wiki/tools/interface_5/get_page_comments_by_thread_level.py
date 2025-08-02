import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageCommentsByThreadLevel(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: int, thread_level: int) -> str:
        comments = data.get("comments", {}).values()
        result = [
            c for c in comments
            if str(c.get("page_id")) == str(page_id) and c.get("thread_level", 0) == thread_level
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_comments_by_thread_level",
                "description": "Get comments on a page filtered by thread level",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "integer", "description": "Page ID"},
                        "thread_level": {"type": "integer", "description": "Comment thread level (e.g. 0 for top-level)"}
                    },
                    "required": ["page_id", "thread_level"]
                }
            }
        }
