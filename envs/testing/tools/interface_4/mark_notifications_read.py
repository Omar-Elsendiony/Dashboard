import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class MarkNotificationsRead(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               notification_ids: Optional[List[str]] = None, mark_all_read: bool = False) -> str:
        
        users = data.get("users", {})
        notifications = data.get("notifications", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        if not notification_ids and not mark_all_read:
            return json.dumps({"error": "Must specify notification_ids or set mark_all_read=True"})
        
        timestamp = "2025-10-01T00:00:00"
        marked_count = 0
        
        for notification_id, notification in notifications.items():
            # Only process user's own notifications
            if notification.get("user_id") != requesting_user_id:
                continue
            
            # Skip already read notifications
            if notification.get("is_read"):
                continue
            
            # Check if we should mark this notification
            should_mark = False
            if mark_all_read:
                should_mark = True
            elif notification_ids and notification_id in notification_ids:
                should_mark = True
            
            if should_mark:
                notification["is_read"] = True
                notification["read_at"] = timestamp
                marked_count += 1
        
        return json.dumps({
            "success": True,
            "marked_count": marked_count,
            "message": f"Marked {marked_count} notifications as read"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "mark_notifications_read",
                "description": "Mark notifications as read",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user marking notifications"},
                        "notification_ids": {"type": "array", "items": {"type": "string"}, "description": "List of notification IDs to mark as read"},
                        "mark_all_read": {"type": "boolean", "description": "Mark all user's notifications as read"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }