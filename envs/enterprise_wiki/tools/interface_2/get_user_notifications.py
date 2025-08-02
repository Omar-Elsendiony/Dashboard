
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
        notifications = data.get("notifications", {})
        user_notifications = [
            notif for notif in notifications.values()
            if str(notif["user_id"]) == str(user_id)
        ]
        return json.dumps(user_notifications)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_notifications",
                "description": "Get all notifications for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "ID of the user"}
                    },
                    "required": ["user_id"]
                }
            }
        }

