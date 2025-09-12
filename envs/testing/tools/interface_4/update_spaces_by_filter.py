import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateSpacesByFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               filter_type: Optional[str] = None, filter_status: Optional[str] = None,
               filter_creator_id: Optional[str] = None, update_status: Optional[str] = None,
               update_anonymous_access: Optional[bool] = None) -> str:
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - Platform Owner or WikiProgramManager can update spaces
        if requesting_user.get("role") not in ["PlatformOwner", "WikiProgramManager"]:
            return json.dumps({"error": "Only Platform Owner or Wiki Program Manager can update spaces"})
        
        # Validate enum values
        if filter_type and filter_type not in ["global", "personal", "private"]:
            return json.dumps({"error": "Invalid filter_type. Must be one of: global, personal, private"})
        
        if filter_status and filter_status not in ["current", "archived"]:
            return json.dumps({"error": "Invalid filter_status. Must be one of: current, archived"})
        
        if update_status and update_status not in ["current", "archived"]:
            return json.dumps({"error": "Invalid update_status. Must be one of: current, archived"})
        
        updated_spaces = []
        timestamp = "2025-10-01T00:00:00"
        
        for space_id, space in spaces.items():
            # Apply filters
            if filter_type and space.get("type") != filter_type:
                continue
            if filter_status and space.get("status") != filter_status:
                continue
            if filter_creator_id and space.get("created_by_user_id") != filter_creator_id:
                continue
            
            # Apply updates
            if update_status:
                space["status"] = update_status
            if update_anonymous_access is not None:
                space["anonymous_access"] = update_anonymous_access
            
            space["updated_at"] = timestamp
            updated_spaces.append(space)
        
        return json.dumps(updated_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_spaces_by_filter",
                "description": "Update spaces based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "filter_type": {"type": "string", "description": "Filter by type (global, personal, private)"},
                        "filter_status": {"type": "string", "description": "Filter by status (current, archived)"},
                        "filter_creator_id": {"type": "string", "description": "Filter by creator ID"},
                        "update_status": {"type": "string", "description": "New status to set (current, archived)"},
                        "update_anonymous_access": {"type": "boolean", "description": "New anonymous access setting (True/False)"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }