import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddUserToGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, group_id: str, added_by: str):
        users = data.get("users", {})
        groups = data.get("groups", {})
        group_memberships = data.get("user_groups", {})

        if user_id not in users:
            raise ValueError("User not found")
        if group_id not in groups:
            raise ValueError("Group not found")
        
        if str(user_id)+"_"+str(group_id) in group_memberships:
            raise ValueError("User is already a member of the specified group")

        group_memberships[str(user_id)+"_"+str(group_id)] = {
            "user_id": user_id,
            "group_id": group_id,
            "added_at": "2025-07-01T00:00:00Z",
            "added_by": added_by
        }
        
        return json.dumps({
            "user_id": user_id,
            "group_id": group_id,
            "added_at": "2025-07-01T00:00:00Z",
            "added_by": added_by
        })
               

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_user_to_group",
                "description": "Add a user to a group.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to add"},
                        "group_id": {"type": "string", "description": "ID of the group"},
                        "added_by": {"type": "string", "description": "ID of the admin or user performing the addition"}
                    },
                    "required": ["user_id", "group_id", "added_by"]
                }
            }
        }


