import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorRedemptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               investor_status: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        redemptions = data.get("redemptions", {})
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get redemptions for this investor
        investor_redemptions = []
        for redemption in redemptions.values():
            # Find the subscription this redemption relates to
            investor_subscription_id = redemption.get("subscription_id")
            subscription = subscriptions.get(str(investor_subscription_id), {})
            
            # Check if this subscription belongs to our investor
            if subscription.get("investor_id") == investor_id:
                # Filter by investor_status if specified
                if investor_status and redemption.get("status") != investor_status:
                    continue
                
                # Enrich with fund details
                target_fund_id = subscription.get("target_fund_id")
                fund_details = funds.get(str(target_fund_id), {})
                
                enriched_redemption = {
                    **redemption,
                    "target_fund_id": target_fund_id,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type"),
                    "original_subscription_amount": subscription.get("amount")
                }
                investor_redemptions.append(enriched_redemption)
        
        return json.dumps(investor_redemptions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_redemptions",
                "description": "View all redemption requests including pending, approved, and processed transactions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "status": {"type": "string", "description": "Filter by redemption investor_status (pending, approved, processed, cancelled)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
