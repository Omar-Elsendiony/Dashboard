import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorTransactionsHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               start_date: Optional[str] = None, end_date: Optional[str] = None,
               transaction_type: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        payments = data.get("payments", {})
        commitments = data.get("commitments", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        transactions = []
        
        # Get subscriptions
        if not transaction_type or transaction_type == "subscription":
            for subscription in subscriptions.values():
                if str(subscription.get("investor_id")) == str(investor_id):  # Added str() conversion
                    request_date = subscription.get("request_date")
                    
                    # Date filtering
                    if start_date and request_date and request_date < start_date:
                        continue
                    if end_date and request_date and request_date > end_date:
                        continue
                    
                    # Enrich with fund details
                    fund_id = subscription.get("fund_id")
                    fund_details = funds.get(str(fund_id), {})
                    
                    transactions.append({
                        "transaction_id": subscription.get("subscription_id"),
                        "transaction_type": "subscription",
                        "fund_id": fund_id,
                        "fund_name": fund_details.get("name"),
                        "amount": subscription.get("amount"),
                        "status": subscription.get("status"),
                        "date": request_date,
                        "approval_date": subscription.get("approval_date")
                    })
        
        # Get redemptions
        if not transaction_type or transaction_type == "redemption":
            for redemption in redemptions.values():
                subscription_id = redemption.get("subscription_id")
                subscription = subscriptions.get(str(subscription_id), {})
                
                if str(subscription.get("investor_id")) == str(investor_id):  # Added str() conversion
                    request_date = redemption.get("request_date")
                    
                    # Date filtering
                    if start_date and request_date and request_date < start_date:
                        continue
                    if end_date and request_date and request_date > end_date:
                        continue
                    
                    # Enrich with fund details
                    fund_id = subscription.get("fund_id")
                    fund_details = funds.get(str(fund_id), {})
                    
                    transactions.append({
                        "transaction_id": redemption.get("redemption_id"),
                        "transaction_type": "redemption",
                        "fund_id": fund_id,
                        "fund_name": fund_details.get("name"),
                        "amount": redemption.get("redemption_amount"),
                        "status": redemption.get("status"),
                        "date": request_date,
                        "processed_date": redemption.get("processed_date"),
                        "redemption_fee": redemption.get("redemption_fee")
                    })
        
        # Get commitments
        if not transaction_type or transaction_type == "commitment":
            for commitment in commitments.values():
                if str(commitment.get("investor_id")) == str(investor_id):  # Added str() conversion
                    commitment_date = commitment.get("commitment_date")
                    
                    # Date filtering
                    if start_date and commitment_date and commitment_date < start_date:
                        continue
                    if end_date and commitment_date and commitment_date > end_date:
                        continue
                    
                    # Enrich with fund details
                    fund_id = commitment.get("fund_id")
                    fund_details = funds.get(str(fund_id), {})
                    
                    transactions.append({
                        "transaction_id": commitment.get("commitment_id"),
                        "transaction_type": "commitment",
                        "fund_id": fund_id,
                        "fund_name": fund_details.get("name"),
                        "amount": commitment.get("commitment_amount"),
                        "status": commitment.get("status"),
                        "date": commitment_date
                    })
        
        # Sort by date (most recent first) - handle None dates safely
        transactions.sort(key=lambda x: x.get("date") or "", reverse=True)
        
        return json.dumps(transactions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_transactions_history",
                "description": "Comprehensive transaction history including all subscriptions, redemptions, switches, and payments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "start_date": {"type": "string", "description": "Start date for transaction history (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for transaction history (YYYY-MM-DD format)"},
                        "transaction_type": {"type": "string", "description": "Filter by transaction type (subscription, redemption, commitment)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }