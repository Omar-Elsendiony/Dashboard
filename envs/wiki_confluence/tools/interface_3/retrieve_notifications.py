import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, status: Optional[str] = None,
               event_type: Optional[str] = None) -> str:
        """
        Retrieve notifications for a user, optionally filtered by status and event type.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        
        # Validate user exists
        if user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {user_id} not found"
            })
        
        # Find all notifications for the user
        matching_notifications = []
        for notification_id, notification in notifications.items():
            if notification.get("recipient_user_id") == user_id:
                # Apply filters if provided
                if status and notification.get("delivery_status") != status:
                    continue
                if event_type and notification.get("event_type") != event_type:
                    continue
                matching_notifications.append(notification.copy())
        
        # Sort by creation date descending (most recent first)
        matching_notifications.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return json.dumps({
            "success": True,
            "user_id": user_id,
            "count": len(matching_notifications),
            "notifications": matching_notifications
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_notifications",
                "description": "Retrieve notifications for a user in the Confluence system, optionally filtered by status and event type. This tool fetches user notifications with comprehensive details including notification IDs, event types, messages, related entities, sender information, delivery status, and timestamps. Supports filtering by delivery status (pending, sent, read) and event type. Returns notifications sorted by creation date with most recent first. Essential for notification management, user communication, and keeping users informed of system events.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user (required)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by delivery status (optional, e.g., 'pending', 'sent', 'read')"
                        },
                        "event_type": {
                            "type": "string",
                            "description": "Filter by event type (optional, e.g., 'system_alert', 'approval_update')"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
