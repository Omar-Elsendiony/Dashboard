import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], notification_id: Optional[str] = None, user_id: Optional[str] = None,
               type: Optional[str] = None, target_type: Optional[str] = None, target_id: Optional[str] = None,
               is_read: Optional[bool] = None) -> str:
        
        notifications = data.get("notifications", {})
        result = []
        
        for nid, notification in notifications.items():
            # Apply filters
            if notification_id and str(notification_id) != nid:
                continue
            if user_id and notification.get("user_id") != user_id:
                continue
            if type and notification.get("type") != type:
                continue
            if target_type and notification.get("target_type") != target_type:
                continue
            if target_id and notification.get("target_id") != target_id:
                continue
            if is_read is not None and notification.get("is_read") != is_read:
                continue
            
            result.append({
                "notification_id": nid,
                "user_id": notification.get("user_id"),
                "type": notification.get("type"),
                "title": notification.get("title"),
                "message": notification.get("message"),
                "target_type": notification.get("target_type"),
                "target_id": notification.get("target_id"),
                "is_read": notification.get("is_read"),
                "read_at": notification.get("read_at"),
                "delivery_method": notification.get("delivery_method"),
                "email_sent": notification.get("email_sent"),
                "created_at": notification.get("created_at"),
                "created_by_user_id": notification.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_notifications",
                "description": "Get notifications matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_id": {"type": "string", "description": "ID of the notification"},
                        "user_id": {"type": "string", "description": "ID of the user who received the notification"},
                        "type": {"type": "string", "description": "Type of notification (page_created, page_updated, page_deleted, comment_added, comment_replied, comment_resolved, attachment_uploaded, attachment_updated, attachment_deleted, label_added, label_removed, space_created, space_updated, space_archived, space_member_added, space_member_removed, user_mentioned, permission_granted, permission_revoked)"},
                        "target_type": {"type": "string", "description": "Type of target (space, page, comment)"},
                        "target_id": {"type": "string", "description": "ID of the target entity"},
                        "is_read": {"type": "boolean", "description": "Whether notification has been read (True/False)"}
                    },
                    "required": []
                }
            }
        }
