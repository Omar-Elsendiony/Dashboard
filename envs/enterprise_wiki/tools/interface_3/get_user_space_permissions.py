import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserSpacePermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int, space_id: int) -> str:
        space_permissions = data.get("space_permissions", [])
        return json.dumps([
            perm for perm in space_permissions.values()
            if str(perm.get("space_id")) == str(space_id) and
               perm.get("subject_type") == "user" and
               str(perm.get("subject_id")) == str(user_id)
        ])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_space_permissions",
                "description": "Get a user's permissions in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "User ID"},
                        "space_id": {"type": "integer", "description": "Space ID"}
                    },
                    "required": ["user_id", "space_id"]
                }
            }
        }
