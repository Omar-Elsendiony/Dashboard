import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateWatchersStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, new_watch_type: str,
               filter_user_id: Optional[str] = None, filter_target_type: Optional[str] = None,
               filter_target_id: Optional[str] = None, new_notifications_enabled: Optional[bool] = None) -> str:
        
        users = data.get("users", {})
        watchers = data.get("watchers", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Validate enum values
        if filter_target_type and filter_target_type not in ["space", "page", "user"]:
            return json.dumps({"error": "Invalid filter_target_type. Must be one of: space, page, user"})
        
        if new_watch_type not in ["watching", "not_watching"]:
            return json.dumps({"error": "Invalid new_watch_type. Must be one of: watching, not_watching"})
        
        updated_watchers = []
        
        for watcher_id, watcher in watchers.items():
            # Apply filters
            if filter_user_id and watcher.get("user_id") != filter_user_id:
                continue
            if filter_target_type and watcher.get("target_type") != filter_target_type:
                continue
            if filter_target_id and watcher.get("target_id") != filter_target_id:
                continue
            
            # Check permissions - users can only update their own watchers, Platform Owner can update any
            has_permission = False
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            elif watcher.get("user_id") == requesting_user_id:
                has_permission = True
            
            if not has_permission:
                continue
            
            # Apply updates
            watcher["watch_type"] = new_watch_type
            if new_notifications_enabled is not None:
                watcher["notifications_enabled"] = new_notifications_enabled
            
            updated_watchers.append(watcher)
        
        return json.dumps(updated_watchers)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_watchers_status",
                "description": "Update watcher status and notification preferences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "new_watch_type": {"type": "string", "description": "New watch type (watching, not_watching)"},
                        "filter_user_id": {"type": "string", "description": "Filter by user ID"},
                        "filter_target_type": {"type": "string", "description": "Filter by target type (space, page, user)"},
                        "filter_target_id": {"type": "string", "description": "Filter by target ID"},
                        "new_notifications_enabled": {"type": "boolean", "description": "New notifications setting (True/False)"}
                    },
                    "required": ["requesting_user_id", "new_watch_type"]
                }
            }
        }