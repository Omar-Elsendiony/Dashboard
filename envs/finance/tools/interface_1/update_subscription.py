import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_subscription(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        subscription_id: str,
        amount: str = None,
        status: str = None,
        request_assigned_to: str = None
    ) -> str:
        users = data.get("users", {})
        subscriptions = data.get("subscriptions", {})

        if str(subscription_id) not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        subscription = subscriptions[str(subscription_id)]

        if amount is not None:
            subscription["amount"] = amount

        if status is not None:
            valid_statuses = ["pending", "approved", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            subscription["status"] = status
            if status == "approved":
                date_str = datetime.now().strftime("%Y-%m-%d")
                subscription["approval_date"] = date_str

        if request_assigned_to is not None:
            if str(request_assigned_to) not in users:
                raise ValueError(f"User {request_assigned_to} not found")
            user = users[str(request_assigned_to)]
            if user.get("status") != "active":
                raise ValueError(f"User {request_assigned_to} must be active to assign subscription")
            subscription["request_assigned_to"] = request_assigned_to

        subscription["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subscription",
                "description": "Update subscription fields; only provided fields will be changed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription"},
                        "amount": {"type": "string", "description": "New subscription amount"},
                        "status": {"type": "string", "description": "New subscription status"},
                        "request_assigned_to": {"type": "string", "description": "User ID to assign the subscription request to (must be active)"}
                    },
                    "required": ["subscription_id"]
                }
            }
        }
