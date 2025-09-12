import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, target_user_id: str,
               notification_type: str, title: str, message: Optional[str] = None,
               target_type: Optional[str] = None, target_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        notifications = data.get("notifications", {})
        
        # Validate users exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        if str(target_user_id) not in users:
            return json.dumps({"error": "Target user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Authority check - Platform Owner or system can create notifications
        if requesting_user.get("role") not in ["PlatformOwner", "WikiProgramManager"]:
            return json.dumps({"error": "Insufficient authority to create notifications"})
        
        # Validate enum values
        valid_types = [
            'page_created', 'page_updated', 'page_deleted', 'comment_added', 'comment_replied',
            'comment_resolved', 'attachment_uploaded', 'attachment_updated', 'attachment_deleted',
            'label_added', 'label_removed', 'space_created', 'space_updated', 'space_archived',
            'space_member_added', 'space_member_removed', 'user_mentioned', 'permission_granted',
            'permission_revoked'
        ]
        
        if notification_type not in valid_types:
            return json.dumps({"error": f"Invalid notification_type. Must be one of: {', '.join(valid_types)}"})
        
        if target_type and target_type not in ["space", "page", "comment"]:
            return json.dumps({"error": "Invalid target_type. Must be one of: space, page, comment"})
        
        # Create notification
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": int(notification_id),
            "user_id": target_user_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "target_type": target_type,
            "target_id": target_id,
            "is_read": False,
            "read_at": None,
            "delivery_method": "web",
            "email_sent": False,
            "created_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        notifications[notification_id] = new_notification
        
        return json.dumps({
            "notification_id": notification_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_notification",
                "description": "Create a new notification for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the notification"},
                        "target_user_id": {"type": "string", "description": "ID of the user to notify"},
                        "notification_type": {"type": "string", "description": "Type of notification (page_created, page_updated, page_deleted, comment_added, comment_replied, comment_resolved, attachment_uploaded, attachment_updated, attachment_deleted, label_added, label_removed, space_created, space_updated, space_archived, space_member_added, space_member_removed, user_mentioned, permission_granted, permission_revoked)"},
                        "title": {"type": "string", "description": "Notification title"},
                        "message": {"type": "string", "description": "Notification message"},
                        "target_type": {"type": "string", "description": "Target type (space, page, comment)"},
                        "target_id": {"type": "string", "description": "Target ID"}
                    },
                    "required": ["requesting_user_id", "target_user_id", "notification_type", "title"]
                }
            }
        }