import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNotification(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        created_by: int,
        target_type: str,
        target_id: int,
        delivery_method: str = "web"  # <-- add this
    ) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        # Validate user
        users = data.get("users", {})
        if str(user_id) not in users:
            raise ValueError("User not found")
        
        # Validate created_by
        if str(created_by) not in users:
            raise ValueError("Created_by user not found")
        
        # Create notification
        notifications = data.setdefault("notifications", {})
        new_id = generate_id(notifications)
        
        
        created_at = "2025-07-01T00:00:00Z"

        
        new_notification = {
            "id": new_id,
            "user_id": user_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "target_type": target_type,
            "target_id": target_id,
            "is_read": False,
            "read_at": None,
            "delivery_method": "web",
            "email_sent": False,
            "created_at": created_at,
            "created_by": created_by
        }
        
        notifications[str(new_id)] = new_notification
        return json.dumps(new_notification)


    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_notification",
                "description": "Create a new notification",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "ID of the user to notify"},
                        "notification_type": {"type": "string", "description": "Type of notification ('page_created', 'page_updated', 'comment_replied', 'user_mentioned', 'space_added')"},
                        "title": {"type": "string", "description": "Title of the notification"},
                        "message": {"type": "string", "description": "Message content"},
                        "created_by": {"type": "integer", "description": "ID of the user creating the notification"},
                        "target_type": {"type": "string", "description": "Type of target (space/page/comment)"},
                        "target_id": {"type": "integer", "description": "ID of the target"},
                        "delivery_method": {
                            "type": "string",
                            "description": "How the notification is delivered (e.g., 'web', 'email', 'sms')",
                            "enum": ["web", "email", "sms"]
                        }
                    },
                    "required": ["user_id", "notification_type", "title", "message", "created_by", "target_type", "target_id"]
                }
            }
        }

