import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class send_notification(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        type: str,
        class_: str,
        reference_id: str,
        email: str
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            return str(max((int(k) for k in table.keys()), default=0) + 1)

        notifications = data.setdefault("notifications", {})

        # Validate email
        if not email:
            raise ValueError("Email must be provided")

        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if type not in valid_types:
            raise ValueError(f"Invalid notification type. Must be one of {valid_types}")

        # Validate class
        valid_classes = [
            "funds","investors","portfolios","trades",
            "invoices","reports","documents","subscriptions",
            "commitments","tickets","users","portfolio_holdings"
        ]
        if class_ not in valid_classes:
            raise ValueError(f"Invalid class. Must be one of {valid_classes}")

        notification_id = generate_id(notifications)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        new_notification = {
            "notification_id": notification_id,
            "email": email,
            "type": type,
            "class": class_,
            "reference_id": reference_id,
            "status": "pending",
            "sent_at": timestamp,
            "created_at": timestamp
        }

        notifications[str(notification_id)] = new_notification
        return json.dumps(new_notification)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_notification",
                "description": "Create a notification record. 'email', 'type', 'class', and 'reference_id' are required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "Notification type: alert, report, reminder, or subscription_update"
                        },
                        "class_": {
                            "type": "string",
                            "description": "Entity class this notification relates to"
                        },
                        "reference_id": {
                            "type": "string",
                            "description": "ID of the related record"
                        },
                        "email": {
                            "type": "string",
                            "description": "Recipient email address"
                        }
                    },
                    "required": ["type", "class_", "reference_id", "email"]
                }
            }
        }