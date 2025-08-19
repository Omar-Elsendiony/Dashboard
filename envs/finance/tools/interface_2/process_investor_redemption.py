import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessInvestorRedemption(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str,
               holding_units: float, compliance_approval: bool,
               finance_approval: bool) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        subscriptions = data.get("subscriptions", {})
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        redemptions = data.get("redemptions", {})

        # --- Validate approvals ---
        if not compliance_approval or not finance_approval:
            return json.dumps({"success": False, "message": "Required approvals not obtained"})

        # --- Validate subscription ---
        subscription = subscriptions.get(str(subscription_id))
        if not subscription:
            return json.dumps({"success": False, "message": "Subscription not found"})
        if subscription.get("status") != "approved":
            return json.dumps({"success": False, "message": "Subscription is not active/approved"})

        investor_id = str(subscription.get("investor_id"))
        fund_id = str(subscription.get("fund_id"))

        # --- Validate fund ---
        fund = funds.get(fund_id)
        if not fund:
            return json.dumps({"success": False, "message": "Fund not found"})
        if fund.get("status") != "open":
            return json.dumps({"success": False, "message": "Fund is not open for redemptions"})

        # --- Validate investor ---
        if investor_id not in investors:
            return json.dumps({"success": False, "message": "Investor not found"})

        # --- Find investor's portfolio ---
        investor_portfolio = next(
            (p for p in portfolios.values() if str(p.get("investor_id")) == investor_id),
            None
        )
        if not investor_portfolio:
            return json.dumps({"success": False, "message": "No portfolio found for this investor"})

        # --- Find portfolio holding for this fund ---
        holding = next(
            (h for h in portfolio_holdings.values()
             if str(h.get("portfolio_id")) == str(investor_portfolio.get("portfolio_id"))
             and str(h.get("fund_id")) == fund_id),
            None
        )
        if not holding:
            return json.dumps({"success": False, "message": "No holding found for this fund in the investor's portfolio"})

        current_units = float(holding.get("quantity", 0))
        cost_basis = float(holding.get("cost_basis", 0))

        if holding_units > current_units:
            return json.dumps({
                "success": False,
                "message": f"Insufficient holdings. Available: {current_units}, Requested: {holding_units}"
            })

        # --- Calculate redemption amount ---
        redemption_amount = holding_units * cost_basis

        # --- Create redemption record ---
        redemption_id = generate_id(redemptions)
        timestamp = "2025-10-01T00:00:00"

        new_redemption = {
            "redemption_id": redemption_id,
            "subscription_id": subscription_id,
            "request_date": "2025-10-01",
            "redemption_units": holding_units,
            "redemption_amount": round(redemption_amount, 2),
            "status": "processed",
            "processed_date": "2025-10-01",
            "updated_at": timestamp,
            "redemption_fee": round(redemption_amount * 0.01, 2)  # 1% fee
        }

        redemptions[str(redemption_id)] = new_redemption

        # --- Update portfolio holding quantity ---
        holding["quantity"] = round(current_units - holding_units, 4)

        return json.dumps({
            "success": True,
            "message": "Redemption processed",
            "investor_id": str(investor_id),
            "fund_id": str(fund_id),
            "redemption": new_redemption,
            "redeemed_units": holding_units,
            "redeemed_amount": round(redemption_amount, 2),
            "remaining_units": holding["quantity"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_investor_redemption",
                "description": "Process a redemption request for an investor based on subscription and portfolio holdings",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {
                            "type": "string",
                            "description": "ID of the investor's approved subscription linked to the fund"
                        },
                        "holding_units": {
                            "type": "number",
                            "description": "Number of units the investor requests to redeem (must not exceed portfolio holding)"
                        },
                        "compliance_approval": {
                            "type": "boolean",
                            "description": "Compliance approval flag (True for approved, False for rejected)"
                        },
                        "finance_approval": {
                            "type": "boolean",
                            "description": "Finance approval flag (True for approved, False for rejected)"
                        }
                    },
                    "required": ["subscription_id", "holding_units", "compliance_approval", "finance_approval"]
                }
            }
        }