import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, requesting_user_id: str) -> str:
        
        users = data.get("users", {})
        watchers = data.get("watchers", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        # Validate subscription exists
        if str(subscription_id) not in watchers:
            return json.dumps({"error": f"Subscription {subscription_id} not found"})
        
        subscription = watchers[str(subscription_id)]
        
        # Verify ownership - user can only remove their own subscriptions
        if subscription.get("user_id") != requesting_user_id:
            return json.dumps({"error": "Permission denied: User can only remove their own subscriptions"})
        
        # Remove the subscription
        del watchers[str(subscription_id)]
        
        return json.dumps({"success": True, "message": "Subscription removed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_subscription",
                "description": "Remove a subscription for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to remove"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user removing the subscription"}
                    },
                    "required": ["subscription_id", "requesting_user_id"]
                }
            }
        }
