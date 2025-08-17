import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: Optional[str] = None,
               notification_type: Optional[str] = None, status: Optional[str] = None,
               notification_class: Optional[str] = None) -> str:
        notifications = data.get("notifications", {})
        results = []
        
        for notification in notifications.values():
            if email and notification.get("email") != email:
                continue
            if notification_type and notification.get("type") != notification_type:
                continue
            if status and notification.get("status") != status:
                continue
            if notification_class and notification.get("class") != notification_class:
                continue
            results.append(notification)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_notifications",
                "description": "Get notifications for message management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Filter by email address"},
                        "notification_type": {"type": "string", "description": "Filter by notification type (alert, report, reminder, subscription_update)"},
                        "status": {"type": "string", "description": "Filter by status (pending, sent, failed)"},
                        "notification_class": {"type": "string", "description": "Filter by notification class"}
                    },
                    "required": []
                }
            }
        }
