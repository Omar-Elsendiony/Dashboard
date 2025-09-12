import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateGroupsByFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               filter_type: Optional[str] = None, filter_creator_id: Optional[str] = None,
               update_description: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Validate enum values
        if filter_type and filter_type not in ["system", "custom"]:
            return json.dumps({"error": "Invalid filter_type. Must be one of: system, custom"})
        
        # Authority check - only Platform Owner can update groups
        if requesting_user.get("role") != "PlatformOwner":
            return json.dumps({"error": "Only Platform Owner can update groups"})
        
        updated_groups = []
        
        for group_id, group in groups.items():
            # Apply filters
            if filter_type and group.get("type") != filter_type:
                continue
            if filter_creator_id and group.get("created_by_user_id") != filter_creator_id:
                continue
            
            # Apply updates
            if update_description is not None:
                group["description"] = update_description
            
            updated_groups.append(group)
        
        return json.dumps(updated_groups)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_groups_by_filter",
                "description": "Update groups based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "filter_type": {"type": "string", "description": "Filter by group type (system, custom)"},
                        "filter_creator_id": {"type": "string", "description": "Filter by creator ID"},
                        "update_description": {"type": "string", "description": "New description to set"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }