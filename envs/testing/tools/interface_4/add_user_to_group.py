import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddUserToGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str, target_user_id: str, requesting_user_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        user_groups = data.get("user_groups", {})
        
        # Validate entities exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        if str(target_user_id) not in users:
            return json.dumps({"error": "Target user not found"})
        
        if str(group_id) not in groups:
            return json.dumps({"error": "Group not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - Platform Owner or WikiProgramManager can add users to groups
        if requesting_user.get("role") not in ["PlatformOwner", "WikiProgramManager"]:
            return json.dumps({"error": "Only Platform Owner or Wiki Program Manager can add users to groups"})
        
        # Check if user is already in group
        for ug in user_groups.values():
            if (ug.get("user_id") == target_user_id and 
                ug.get("group_id") == group_id):
                return json.dumps({"error": "User is already a member of this group"})
        
        # Add user to group
        user_group_id = generate_id(user_groups)
        timestamp = "2025-10-01T00:00:00"
        
        new_user_group = {
            "user_group_id": int(user_group_id),
            "user_id": target_user_id,
            "group_id": group_id,
            "added_by_user_id": requesting_user_id,
            "added_at": timestamp
        }
        
        user_groups[user_group_id] = new_user_group
        
        return json.dumps({
            "user_group_id": user_group_id,
            "success": True,
            "message": "User added to group"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_user_to_group",
                "description": "Add a user to a group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group"},
                        "target_user_id": {"type": "string", "description": "ID of the user to add"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"}
                    },
                    "required": ["group_id", "target_user_id", "requesting_user_id"]
                }
            }
        }