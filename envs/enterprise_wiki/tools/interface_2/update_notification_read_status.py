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

        return json.dumps({
            "status": "updated",
            "notification_id": notification_id,
            "is_read": is_read
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_notification_read_status",
                "description": "Update the read/unread status of a notification.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_id": {"type": "integer", "description": "ID of the notification to update"},
                        "is_read": {"type": "boolean", "description": "Whether the notification is marked as read"}
                    },
                    "required": ["notification_id", "is_read"]
                }
            }
        }
