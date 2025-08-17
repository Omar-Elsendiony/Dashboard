import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubscribeInvestorToFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, amount: float,
               request_assigned_to: str, request_date: str, payment_id: Optional[str] = None,
               status: str = "pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate assigned user exists
        if str(request_assigned_to) not in users:
            raise ValueError(f"Assigned user {request_assigned_to} not found")
        
        # Validate status
        valid_statuses = ["pending", "approved", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00"
        
        new_subscription = {
            "subscription_id": str(subscription_id),
            "fund_id": str(fund_id),
            "investor_id": str(investor_id),
            "payment_id": str(payment_id) if payment_id else None,
            "amount": amount,
            "status": status,
            "request_assigned_to": str(request_assigned_to),
            "request_date": request_date,
            "approval_date": None,
            "updated_at": timestamp
        }
        
        subscriptions[str(subscription_id)] = new_subscription
        return json.dumps(new_subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "subscribe_investor_to_fund",
                "description": "Subscribe investor to fund for core revenue generation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "amount": {"type": "number", "description": "Subscription amount"},
                        "request_assigned_to": {"type": "string", "description": "ID of assigned user"},
                        "request_date": {"type": "string", "description": "Request date in YYYY-MM-DD format"},
                        "payment_id": {"type": "string", "description": "Payment ID (optional)"},
                        "status": {"type": "string", "description": "Status (pending, approved, cancelled), defaults to pending"}
                    },
                    "required": ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date"]
                }
            }
        }
