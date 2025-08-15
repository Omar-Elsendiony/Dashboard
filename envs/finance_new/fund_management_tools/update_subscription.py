import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, changes: Dict[str, Any],
               compliance_officer_approval: bool, finance_officer_approval: bool) -> str:
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        if not finance_officer_approval:
            return json.dumps({"error": "Finance Officer approval required. Process halted."})
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            return json.dumps({"error": f"Subscription {subscription_id} not found"})
        
        subscription = subscriptions[str(subscription_id)]
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Apply changes
        for key, value in changes.items():
            if key in ["amount", "status"]:
                subscription[key] = value
        
        subscription["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Subscription updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subscription",
                "description": "Update subscription details with required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to update"},
                        "changes": {"type": "object", "description": "Dictionary of changes"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"},
                        "finance_officer_approval": {"type": "boolean", "description": "Finance Officer approval flag"}
                    },
                    "required": ["subscription_id", "changes", "compliance_officer_approval", "finance_officer_approval"]
                }
            }
        }
