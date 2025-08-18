import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CancelInvestorSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_subscription_id: str) -> str:
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(investor_subscription_id) not in subscriptions:
            return json.dumps({"error": f"Subscription {investor_subscription_id} not found"})
        
        subscription = subscriptions[str(investor_subscription_id)]
        timestamp = "2025-10-01T00:00:00"
        
        # Update subscription investor_status
        subscription["status"] = "cancelled"
        subscription["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Cancellation complete"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_investor_subscription",
                "description": "Cancel a subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_subscription_id": {
                            "type": "string",
                            "description": "ID of the investor subscription to cancel"
                        }
                    },
                    "required": ["investor_subscription_id"]
                }
            }
        }
