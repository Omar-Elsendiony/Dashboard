import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, changes: Dict[str, Any],
               fund_manager_approval: bool, compliance_review_required: Optional[bool] = None,
               compliance_officer_approval: Optional[bool] = None) -> str:
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        if compliance_review_required and not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required for this change. Process halted."})
        
        funds = data.get("funds", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Find active subscription
        active_subscription = None
        for sub in subscriptions.values():
            if (sub.get("investor_id") == int(investor_id) and 
                sub.get("fund_id") == int(fund_id) and 
                sub.get("status") == "approved"):
                active_subscription = sub
                break
        
        if not active_subscription:
            return json.dumps({"error": "No active subscription found for this investor in the fund"})
        
        if active_subscription.get("amount", 0) < amount_or_units:
            return json.dumps({"error": "Insufficient balance for redemption"})
        
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Create redemption record
        redemption_id = generate_id(redemptions)
        new_redemption = {
            "redemption_id": redemption_id,
            "subscription_id": active_subscription["subscription_id"],
            "request_date": timestamp.split("T")[0],
            "redemption_amount": amount_or_units,
            "status": "processed",
            "processed_date": timestamp.split("T")[0],
            "updated_at": timestamp,
            "redemption_fee": amount_or_units * 0.01  # 1% redemption fee
        }
        redemptions[str(redemption_id)] = new_redemption
        
        # Update subscription amount
        active_subscription["amount"] -= amount_or_units
        active_subscription["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Redemption processed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_redemption",
                "description": "Process investor redemption with required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount_or_units": {"type": "number", "description": "Amount or units to redeem"},
                        "reason": {"type": "string", "description": "Reason for redemption"},
                        "compliance_approval": {"type": "boolean", "description": "Compliance approval flag"},
                        "finance_approval": {"type": "boolean", "description": "Finance approval flag"}
                    },
                    "required": ["investor_id", "fund_id", "amount_or_units", "reason", "compliance_approval", "finance_approval"]
                }
            }
        }
