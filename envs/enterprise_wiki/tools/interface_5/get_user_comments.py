import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserComments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
        comments = data.get("comments", {}).values()
        result = [c.get("id") for c in comments if str(c.get("created_by")) == str(user_id)]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_comments",
                "description": "Get all comment ids made by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "User ID"}
                    },
                    "required": ["user_id"]
                }
            }
        }
