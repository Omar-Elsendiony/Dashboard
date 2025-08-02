import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageComments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: int) -> str:
        comments = data.get("comments", {})
        print(type(comments))
        return json.dumps([c["id"] for c in comments.values() if c["page_id"] == int(page_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_comments",
                "description": "Get all comment IDs for a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "integer",
                            "description": "ID of the page"
                        }
                    },
                    "required": ["page_id"]
                }
            }
        }
