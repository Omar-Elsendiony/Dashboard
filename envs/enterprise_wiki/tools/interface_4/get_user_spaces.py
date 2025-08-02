import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserSpaces(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
        result = []
        permissions = data.get("space_permissions", {})

        for perm in permissions.values():
            if perm.get("subject_type") == "user" and str(perm.get("subject_id")) == str(user_id):
                space = data.get("spaces", {}).get(str(perm.get("space_id")))
                if space:
                    result.append(space)

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_spaces",
                "description": "Return all spaces a user has access to.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer"}
                    },
                    "required": ["user_id"]
                }
            }
        }
