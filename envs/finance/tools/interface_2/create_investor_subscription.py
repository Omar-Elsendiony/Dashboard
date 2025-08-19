import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateInvestorSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, amount: float,
               compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # if not compliance_officer_approval:
        #     return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate entities exist
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Check if fund is open
        if funds[str(fund_id)].get("status") != "open":
            return json.dumps({"error": "Fund is not open for subscriptions"})
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00"
        
        # Determine status based on payment details
        status = "pending" if not compliance_officer_approval else "approved"
        
        new_subscription = {
            "subscription_id": str(subscription_id),
            "fund_id": fund_id,
            "investor_id": investor_id,
            "amount": amount,
            "status": status,
            "request_assigned_to": "6",  # Default admin
            "request_date": timestamp.split("T")[0],
            "approval_date": timestamp.split("T")[0] if status == "approved" else None,
            "updated_at": timestamp
        }
        
        subscriptions[str(subscription_id)] = new_subscription
        
        #return_status = "active" if status == "approved" else "funds_pending"
        return json.dumps(new_subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_investor_subscription",
                "description": "Create a new fund subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount": {"type": "number", "description": "Subscription amount"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag (True/False)"}
                    },
                    "required": ["investor_id", "fund_id", "amount", "compliance_officer_approval"]
                }
            }
        }