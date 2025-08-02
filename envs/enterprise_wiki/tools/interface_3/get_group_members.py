import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupMembers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: int) -> str:
        user_groups = data.get("user_groups", [])
        users = data.get("users", {})
        member_ids = [ug["user_id"] for ug in user_groups.values() if str(ug["group_id"]) == str(group_id)]
        return json.dumps([users[str(uid)] for uid in member_ids if str(uid) in users])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_group_members",
                "description": "Get all members of a group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "integer", "description": "Group ID"}
                    },
                    "required": ["group_id"]
                }
            }
        }
