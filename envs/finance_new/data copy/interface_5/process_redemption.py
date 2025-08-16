import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessRedemption(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, 
               amount_or_units: float, reason: str, compliance_approval: bool, 
               finance_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"success": False, "message": "Investor not found", "halt": True})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found", "halt": True})
        
        # Check if fund is open
        if funds[str(fund_id)].get("status") != "open":
            return json.dumps({"success": False, "message": "Fund is not open for redemptions", "halt": True})
        
        # Validate approvals
        if not compliance_approval or not finance_approval:
            return json.dumps({"success": False, "message": "Required approvals not obtained", "halt": True})
        
        # Find existing subscription
        subscription_id = None
        for sub_id, sub in subscriptions.items():
            if sub.get("investor_id") == investor_id and sub.get("fund_id") == fund_id:
                subscription_id = sub_id
                break
        
        if not subscription_id:
            return json.dumps({"success": False, "message": "No subscription found for this investor and fund", "halt": True})
        
        redemption_id = generate_id(redemptions)
        timestamp = "2025-10-01T00:00:00"
        
        new_redemption = {
            "redemption_id": redemption_id,
            "subscription_id": subscription_id,
            "request_date": "2025-10-01",
            "redemption_amount": amount_or_units,
            "status": "approved",
            "processed_date": "2025-10-01",
            "updated_at": timestamp,
            "redemption_fee": round(amount_or_units * 0.01, 2)  # 1% fee
        }
        
        redemptions[str(redemption_id)] = new_redemption
        return json.dumps({"success": True, "message": "Redemption processed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_redemption",
                "description": "Process a redemption request for an investor",
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
