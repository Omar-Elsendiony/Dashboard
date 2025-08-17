import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, 
               status: Optional[str] = None, approval_date: Optional[str] = None,
               amount: Optional[str] = None, payment_id: Optional[str] = None) -> str:
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        
        subscription = subscriptions[str(subscription_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["pending", "approved", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            subscription["status"] = status
        
        # Update fields if provided
        if approval_date:
            subscription["approval_date"] = approval_date
        if amount:
            subscription["amount"] = amount
        if payment_id:
            subscription["payment_id"] = payment_id
        
        # Update timestamp
        subscription["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subscription",
                "description": "Update a subscription record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to update"},
                        "status": {"type": "string", "description": "New status (pending, approved, cancelled)"},
                        "approval_date": {"type": "string", "description": "Date of approval"},
                        "amount": {"type": "string", "description": "New subscription amount"},
                        "payment_id": {"type": "string", "description": "ID of associated payment"}
                    },
                    "required": ["subscription_id"]
                }
            }
        }
