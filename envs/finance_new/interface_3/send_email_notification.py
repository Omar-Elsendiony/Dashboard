import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SendEmailNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str, notification_type: str, 
               notification_class: str, reference_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        
        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if notification_type not in valid_types:
            raise ValueError(f"Invalid notification type. Must be one of {valid_types}")
        
        # Validate notification class
        valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", 
                        "reports", "documents", "subscriptions", "commitments"]
        if notification_class not in valid_classes:
            raise ValueError(f"Invalid notification class. Must be one of {valid_classes}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": notification_id,
            "email": email,
            "type": notification_type,
            "class": notification_class,
            "reference_id": reference_id,
            "status": "pending",
            "sent_at": None,
            "created_at": timestamp
        }
        
        notifications[str(notification_id)] = new_notification
        return json.dumps({"notification_id": notification_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_email_notification",
                "description": "Send email notification for client communication",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Recipient email address"},
                        "notification_type": {"type": "string", "description": "Notification type (alert, report, reminder, subscription_update)"},
                        "notification_class": {"type": "string", "description": "Notification class (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                        "reference_id": {"type": "string", "description": "Reference ID for related entity (optional)"}
                    },
                    "required": ["email", "notification_type", "notification_class"]
                }
            }
        }
