import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class modify_subscription(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        subscription_id: str,
        amount: Optional[str] = None,
        currency: Optional[str] = None,
        status: Optional[str] = None,
        request_assigned_to: Optional[str] = None
    ) -> str:
        subscriptions = data.get("subscriptions", {})
        users = data.get("users", {})

        # Validate subscription exists
        if subscription_id not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        subscription = subscriptions[subscription_id]

        # Validate currency if provided
        if currency is not None:
            valid_currencies = ["USD", "EUR", "GBP", "NGN"]
            if currency not in valid_currencies:
                raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
            subscription["currency"] = currency

        # Validate status if provided
        if status is not None:
            valid_statuses = ["pending", "approved", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            subscription["status"] = status
            if status == "approved":
                subscription["approval_date"] = datetime.now().strftime("%Y-%m-%d")

        # Validate and update request_assigned_to if provided
        if request_assigned_to is not None:
            if request_assigned_to not in users:
                raise ValueError(f"User {request_assigned_to} not found")
            user = users[request_assigned_to]
            if user.get("status") != "active":
                raise ValueError(f"User {request_assigned_to} must be active to assign subscription")
            subscription["request_assigned_to"] = request_assigned_to

        # Update amount if provided
        if amount is not None:
            subscription["amount"] = amount

        # Always update timestamp when any change occurs
        subscription["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_subscription",
                "description": "Modify an existing subscription; only provided fields will be changed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {
                            "type": "string",
                            "description": "ID of the subscription to modify"
                        },
                        "amount": {
                            "type": "string",
                            "description": "New subscription amount (optional)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "New currency (USD, EUR, GBP, NGN) (optional)"
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (pending, approved, cancelled) (optional)"
                        },
                        "request_assigned_to": {
                            "type": "string",
                            "description": "User ID to assign this subscription request to (must be active; optional)"
                        }
                    },
                    "required": ["subscription_id"]
                }
            }
        }