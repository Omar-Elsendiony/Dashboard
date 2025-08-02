import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserGroups(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
        
        user_groups = data.get("user_groups", {})
        groups = data.get("groups", {})
        group_ids = [ug["group_id"] for ug in user_groups.values() if str(ug["user_id"]) == str(user_id)]
        # print(f"User ID: {user_id}, Group IDs: {group_ids}")
        return json.dumps([groups[str(gid)] for gid in group_ids if str(gid) in groups])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_groups",
                "description": "Get all groups a user belongs to",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
