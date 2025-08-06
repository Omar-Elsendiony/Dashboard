import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class email_user(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        email: str,
        type: str,
        class_: str,
        reference_id: str
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max((int(k) for k in table.keys()), default=0) + 1)

        notifications = data.setdefault("notifications", {})

        # Validate email
        if not email:
            raise ValueError("Email must be provided")

        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")

        # Validate class
        valid_classes = [
            "funds", "investors", "portfolios", "trades",
            "invoices", "reports", "documents", "subscriptions",
            "commitments", "tickets", "users", "portfolio_holdings"
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
            "sent_at": None,
            "created_at": timestamp
        }

        notifications[notification_id] = new_notification
        return json.dumps(new_notification)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "email_user",
                "description": (
                    "Create a notification by email directly. "
                    "Provide email, type, class, and reference_id."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "type": {
                            "type": "string",
                            "description": "Notification type (alert, report, reminder, subscription_update)"
                        },
                        "class_": {
                            "type": "string",
                            "description": (
                                "Entity class: funds, investors, portfolios, trades, "
                                "invoices, reports, documents, subscriptions, commitments, "
                                "tickets, users, or portfolio_holdings"
                            )
                        },
                        "reference_id": {
                            "type": "string",
                            "description": "ID of the related record"
                        }
                    },
                    "required": ["email", "type", "class_", "reference_id"]
                }
            }
        }

