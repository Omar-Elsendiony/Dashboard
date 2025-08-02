import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveUserFromGroup(Tool):

    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, group_id: str) -> str:
        group_memberships = data.get("user_groups", {})
        key = f"{user_id}_{group_id}"

        if key not in group_memberships:
            raise ValueError("User is not a member of the specified group")

        removed_entry = group_memberships.pop(key)

        return json.dumps({
            "user_id": removed_entry["user_id"],
            "group_id": removed_entry["group_id"],
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_user_from_group",
                "description": "Remove a user from a group.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to remove"},
                        "group_id": {"type": "string", "description": "ID of the group"}
                    },
                    "required": ["user_id", "group_id"]
                }
            }
        }

