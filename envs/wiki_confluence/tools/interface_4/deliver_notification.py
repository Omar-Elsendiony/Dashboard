import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DeliverNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], recipient_user_id: str, event_type: str,
               message: str, sender_user_id: Optional[str] = None,
               channel: Optional[str] = None, related_entity_type: Optional[str] = None,
               related_entity_id: Optional[str] = None, metadata: Optional[str] = None) -> str:
        """
        Send a system alert, email, or custom message to a specified user account.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        
        # Validate recipient exists
        if recipient_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"Recipient user {recipient_user_id} not found"
            })
        
        # Validate sender if provided
        if sender_user_id and sender_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"Sender user {sender_user_id} not found"
            })
        
        # Generate new notification ID
        new_notification_id = generate_id(notifications)
        timestamp = "2025-10-01T12:00:00"
        
        new_notification = {
            "notification_id": str(new_notification_id),
            "recipient_user_id": recipient_user_id,
            "event_type": event_type,
            "message": message,
            "related_entity_type": related_entity_type,
            "related_entity_id": related_entity_id,
            "sender_user_id": sender_user_id,
            "channel": channel if channel else "system",
            "delivery_status": "pending",
            "created_at": timestamp,
            "sent_at": None,
            "read_at": None,
            "metadata": metadata
        }
        
        notifications[str(new_notification_id)] = new_notification
        
        return json.dumps({
            "success": True,
            "notification_id": str(new_notification_id),
            "message": f"Notification sent to user {recipient_user_id}",
            "notification_data": new_notification
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "deliver_notification",
                "description": "Send a system alert, email, or custom message to a specified user account in the Confluence system. This tool creates and dispatches notifications to users for various events including system alerts, approval updates, content changes, and custom messages. Supports multiple delivery channels, sender attribution, entity references, and custom metadata. Tracks delivery status and timestamps. Essential for user communication, event notifications, workflow updates, and keeping stakeholders informed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient_user_id": {
                            "type": "string",
                            "description": "User ID of the notification recipient (required)"
                        },
                        "event_type": {
                            "type": "string",
                            "description": "Type of event triggering the notification (required, e.g., 'system_alert', 'approval_update', 'content_change')"
                        },
                        "message": {
                            "type": "string",
                            "description": "Notification message content (required)"
                        },
                        "sender_user_id": {
                            "type": "string",
                            "description": "User ID of the notification sender (optional)"
                        },
                        "channel": {
                            "type": "string",
                            "description": "Notification channel (optional, defaults to 'system')"
                        },
                        "related_entity_type": {
                            "type": "string",
                            "description": "Type of related entity (optional, e.g., 'page', 'space')"
                        },
                        "related_entity_id": {
                            "type": "string",
                            "description": "ID of related entity (optional)"
                        },
                        "metadata": {
                            "type": "string",
                            "description": "Additional metadata as JSON string (optional)"
                        }
                    },
                    "required": ["recipient_user_id", "event_type", "message"]
                }
            }
        }
