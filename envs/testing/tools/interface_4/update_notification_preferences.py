import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateNotificationPreferences(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, new_delivery_method: str,
               filter_user_id: Optional[str] = None, filter_delivery_method: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        notifications = data.get("notifications", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Validate enum values
        if filter_delivery_method and filter_delivery_method not in ["web", "email", "both"]:
            return json.dumps({"error": "Invalid filter_delivery_method. Must be one of: web, email, both"})
        
        if new_delivery_method not in ["web", "email", "both"]:
            return json.dumps({"error": "Invalid new_delivery_method. Must be one of: web, email, both"})
        
        updated_notifications = []
        
        for notification_id, notification in notifications.items():
            # Apply filters
            if filter_user_id and notification.get("user_id") != filter_user_id:
                continue
            if filter_delivery_method and notification.get("delivery_method") != filter_delivery_method:
                continue
            
            # Check permissions - users can only update their own notifications, Platform Owner can update any
            has_permission = False
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            elif notification.get("user_id") == requesting_user_id:
                has_permission = True
            
            if not has_permission:
                continue
            
            # Apply update
            notification["delivery_method"] = new_delivery_method
            updated_notifications.append(notification)
        
        return json.dumps(updated_notifications)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_notification_preferences",
                "description": "Update notification delivery preferences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "new_delivery_method": {"type": "string", "description": "New delivery method (web, email, both)"},
                        "filter_user_id": {"type": "string", "description": "Filter by user ID"},
                        "filter_delivery_method": {"type": "string", "description": "Filter by current delivery method (web, email, both)"}
                    },
                    "required": ["requesting_user_id", "new_delivery_method"]
                }
            }
        }