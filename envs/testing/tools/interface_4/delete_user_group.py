import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteUserGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str, requesting_user_id: str) -> str:
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        user_groups = data.get("user_groups", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate group exists
        if str(group_id) not in groups:
            return json.dumps({"error": "Group not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        group = groups[str(group_id)]
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - only Platform Owner can delete groups
        if requesting_user.get("role") != "PlatformOwner":
            return json.dumps({"error": "Only Platform Owner can delete user groups"})
        
        # Check if group is system type
        if group.get("type") == "system":
            return json.dumps({"error": "Cannot delete system groups"})
        
        # Check if group has permissions assigned
        group_has_permissions = False
        
        for perm in page_permissions.values():
            if perm.get("group_id") == group_id:
                group_has_permissions = True
                break
        
        if not group_has_permissions:
            for perm in space_permissions.values():
                if perm.get("group_id") == group_id:
                    group_has_permissions = True
                    break
        
        if group_has_permissions:
            return json.dumps({"error": "Cannot delete group with active permissions. Remove permissions first"})
        
        # Remove all user-group associations
        user_groups_to_delete = []
        for ug_id, ug in user_groups.items():
            if ug.get("group_id") == group_id:
                user_groups_to_delete.append(ug_id)
        
        for ug_id in user_groups_to_delete:
            del user_groups[ug_id]
        
        # Delete the group
        del groups[str(group_id)]
        
        return json.dumps({"success": True, "message": "Group deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_user_group",
                "description": "Delete a user group and all its associations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user deleting the group"}
                    },
                    "required": ["group_id", "requesting_user_id"]
                }
            }
        }