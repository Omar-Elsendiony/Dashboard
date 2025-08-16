import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessRedemption(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, 
               amount_or_units: float, compliance_approval: bool, 
               finance_approval: bool) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"success": False, "message": "Investor not found"})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found"})
        
        # Check if fund is open
        if funds[str(fund_id)].get("status") != "open":
            return json.dumps({"success": False, "message": "Fund is not open for redemptions"})
        
        # Validate approvals
        if not compliance_approval or not finance_approval:
            return json.dumps({"success": False, "message": "Required approvals not obtained"})
        
        # Find ALL subscriptions and calculate total (OPTION 1)
        all_subscription_ids = []
        all_subscriptions = []
        total_subscription_amount = 0

        for sub_id, sub in subscriptions.items():
            if (sub.get("investor_id") == investor_id and 
                sub.get("fund_id") == fund_id and 
                sub.get("status") == "approved"):
                all_subscription_ids.append(sub.get("subscription_id"))
                all_subscriptions.append(sub)
                total_subscription_amount += float(sub.get("amount", 0))

        if not all_subscription_ids:
            return json.dumps({"success": False, "message": "No active subscription found for this investor and fund"})

        # Check existing redemptions against ALL subscriptions
        total_redeemed = 0
        for redemption in redemptions.values():
            if (redemption.get("subscription_id") in all_subscription_ids and
                redemption.get("status") in ["approved", "processed"]):
                total_redeemed += float(redemption.get("redemption_amount", 0))
        
        # Calculate available balance
        available_balance = total_subscription_amount - total_redeemed
        
        # Validate sufficient balance
        if available_balance < amount_or_units:
            return json.dumps({
                "success": False, 
                "message": f"Insufficient balance. Available: {available_balance}, Requested: {amount_or_units}"
            })
        
        # Additional validation: Check portfolio holdings if they exist
        investor_portfolio = None
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                investor_portfolio = portfolio
                break
        
        if investor_portfolio:
            # Check portfolio holdings for this fund
            fund_holdings = 0
            for holding in portfolio_holdings.values():
                if (holding.get("portfolio_id") == investor_portfolio.get("portfolio_id") and
                    holding.get("fund_id") == fund_id):
                    fund_holdings += float(holding.get("quantity", 0))
            
            # Validate against portfolio holdings if they exist
            if fund_holdings > 0 and fund_holdings < amount_or_units:
                return json.dumps({
                    "success": False, 
                    "message": f"Insufficient holdings in portfolio. Available: {fund_holdings}, Requested: {amount_or_units}"
                })
        
        redemption_id = generate_id(redemptions)
        timestamp = "2025-10-01T00:00:00"
        
        # Use the first subscription for the redemption record (or you could choose differently)
        primary_subscription = all_subscriptions[0]
        
        new_redemption = {
            "redemption_id": redemption_id,
            "subscription_id": primary_subscription.get("subscription_id"),
            "request_date": "2025-10-01",
            "redemption_amount": amount_or_units,
            "status": "approved",
            "processed_date": "2025-10-01",
            "updated_at": timestamp,
            "redemption_fee": round(amount_or_units * 0.01, 2)  # 1% fee
        }
        
        redemptions[str(redemption_id)] = new_redemption
        
        # Update portfolio holdings if they exist
        if investor_portfolio:
            for holding_id, holding in portfolio_holdings.items():
                if (holding.get("portfolio_id") == investor_portfolio.get("portfolio_id") and
                    holding.get("fund_id") == fund_id):
                    # Reduce the holding quantity
                    current_quantity = float(holding.get("quantity", 0))
                    new_quantity = max(0, current_quantity - amount_or_units)
                    holding["quantity"] = new_quantity
                    break
        
        return json.dumps({
            "success": True, 
            "message": "Redemption processed",
            "redemption_id": redemption_id,
            "remaining_balance": available_balance - amount_or_units,
            "debug_info": {
                "total_subscriptions_found": len(all_subscription_ids),
                "total_subscription_amount": total_subscription_amount,
                "total_redeemed_before": total_redeemed,
                "available_balance_before": available_balance
            }
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_redemption",
                "description": "Process a redemption request for an investor with balance validation across all subscriptions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount_or_units": {"type": "number", "description": "Amount or units to redeem"},
                        "compliance_approval": {"type": "boolean", "description": "Compliance approval flag (True for approved/False for rejected)"},
                        "finance_approval": {"type": "boolean", "description": "Finance approval flag (True for approved/False for rejected)"}
                    },
                    "required": ["investor_id", "fund_id", "amount_or_units", "compliance_approval", "finance_approval"]
                }
            }
        }