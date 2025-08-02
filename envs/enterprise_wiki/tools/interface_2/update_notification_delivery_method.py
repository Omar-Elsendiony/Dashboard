import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateNotificationReadStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], notification_id: int, is_read: bool) -> str:
        notifications = data.get("notifications", {})
        notification = notifications.get(str(notification_id))
        if not notification:
            raise ValueError("Notification not found")
        
        notification["is_read"] = is_read
        notification["read_at"] = "NOW()" if is_read else None
        return json.dumps({"success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_notification_read_status",
                "description": "Mark notification as read/unread",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_id": {"type": "integer", "description": "ID of the notification"},
                        "is_read": {"type": "boolean", "description": "Read status (true/false)"}
                    },
                    "required": ["notification_id", "is_read"]
                }
            }
        }

# 9. Update Notification Delivery Method
class UpdateNotificationDeliveryMethod(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], notification_id: int, delivery_method: str) -> str:
        notifications = data.get("notifications", {})
        notification = notifications.get(str(notification_id))
        if not notification:
            raise ValueError("Notification not found")
        
        valid_methods = ["web", "email", "both"]
        if delivery_method not in valid_methods:
            raise ValueError(f"Invalid delivery method. Must be one of {valid_methods}")
        
        notification["delivery_method"] = delivery_method
        return json.dumps({"success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_notification_delivery_method",
                "description": "Update notification delivery method",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_id": {"type": "integer", "description": "ID of the notification"},
                        "delivery_method": {"type": "string", "description": "Delivery method (web/email/both)"}
                    },
                    "required": ["notification_id", "delivery_method"]
                }
            }
        }

