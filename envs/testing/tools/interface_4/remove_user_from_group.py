import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveUserFromGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str, target_user_id: str, requesting_user_id: str) -> str:
        
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
        
        # Authority check - Platform Owner or WikiProgramManager can remove users from groups
        if requesting_user.get("role") not in ["PlatformOwner", "WikiProgramManager"]:
            return json.dumps({"error": "Only Platform Owner or Wiki Program Manager can remove users from groups"})
        
        # Find and remove user-group association
        user_group_to_remove = None
        for ug_id, ug in user_groups.items():
            if (ug.get("user_id") == target_user_id and 
                ug.get("group_id") == group_id):
                user_group_to_remove = ug_id
                break
        
        if not user_group_to_remove:
            return json.dumps({"error": "User is not a member of this group"})
        
        # Remove the association
        del user_groups[user_group_to_remove]
        
        return json.dumps({"success": True, "message": "User removed from group"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_user_from_group",
                "description": "Remove a user from a group",
		"parameters": {
                		"type": "object",
                    		"properties": {
                        	"group_id": {"type": "string", "description": "ID of the group"},
                        	"target_user_id": {"type": "string", "description": "ID of the user to remove"},
                        	"requesting_user_id": {"type": "string", "description": "ID of the user making the request"}
                    		},
                    	"required": ["group_id", "target_user_id", "requesting_user_id"]
                	}
            	   }
        	}