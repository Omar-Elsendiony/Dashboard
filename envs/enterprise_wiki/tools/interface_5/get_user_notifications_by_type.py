import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserNotificationsByType(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int, type: str) -> str:
        notifications = data.get("notifications", {}).values()
        result = [
            n for n in notifications
            if str(n.get("user_id")) == str(user_id) and n.get("type") == type
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_notifications_by_type",
                "description": "Get user notifications filtered by type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "User ID"},
                        "type": {"type": "string", "description": "Notification type (e.g., page_created, page_updated , page_commnted, mentioned, space_added)"}
                    },
                    "required": ["user_id", "type"]
                }
            }
        }
