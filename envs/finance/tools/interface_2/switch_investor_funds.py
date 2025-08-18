import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SwitchInvestorFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, current_fund_id: str,
               target_fund_id: str, switch_amount: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        
        # Validate entities exist
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        if str(current_fund_id) not in funds:
            return json.dumps({"error": f"Current fund {current_fund_id} not found"})
        if str(target_fund_id) not in funds:
            return json.dumps({"error": f"Target fund {target_fund_id} not found"})
        
        # Find current subscription
        current_subscription = None
        for sub in subscriptions.values():
            if (sub.get("investor_id") == (investor_id) and # compare a string with string
                sub.get("target_fund_id") == (current_fund_id) and 
                sub.get("investor_status") == "approved"):
                current_subscription = sub
                break
        
        if not current_subscription:
            return json.dumps({"error": "No active subscription for this investor found in current fund"})
        
        if current_subscription.get("amount", 0) < switch_amount:
            return json.dumps({"error": "Insufficient balance in current fund"})
        
        timestamp = "2025-10-01T00:00:00"
        
        # Create redemption from current fund
        redemption_id = generate_id(redemptions)
        new_redemption = {
            "redemption_id": redemption_id,
            "investor_subscription_id": current_subscription["investor_subscription_id"],
            "request_date": timestamp.split("T")[0],
            "redemption_amount": switch_amount,
            "investor_status": "processed",
            "processed_date": timestamp.split("T")[0],
            "updated_at": timestamp,
            "redemption_fee": 0.0
        }
        redemptions[str(redemption_id)] = new_redemption
        
        # Update current subscription
        current_subscription["amount"] -= switch_amount
        current_subscription["updated_at"] = timestamp
        
        # Create new subscription in target fund
        investor_subscription_id = generate_id(subscriptions)
        new_subscription = {
            "investor_subscription_id": investor_subscription_id,
            "target_fund_id": int(target_fund_id),
            "investor_id": int(investor_id),
            "amount": switch_amount,
            "investor_status": "approved",
            "request_assigned_to": 1,  # Default admin
            "request_date": timestamp.split("T")[0],
            "approval_date": timestamp.split("T")[0],
            "updated_at": timestamp
        }
        subscriptions[str(investor_subscription_id)] = new_subscription
        
        return json.dumps({"success": True, "message": "Switch complete"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "investor_name": "switch_funds",
                "description": "Switch investor funds between two funds",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "current_fund_id": {"type": "string", "description": "ID of the current fund"},
                        "target_fund_id": {"type": "string", "description": "ID of the target fund"},
                        "switch_amount": {"type": "number", "description": "Amount to switch"}
                    },
                    "required": ["investor_id", "current_fund_id", "target_fund_id", "switch_amount"]
                }
            }
        }
