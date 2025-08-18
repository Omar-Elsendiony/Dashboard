import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorRedemptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               status: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        redemptions = data.get("redemptions", {})
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get redemptions for this investor
        redemptions = []
        for redemption in redemptions.values():
            # Find the subscription this redemption relates to
            subscription_id = redemption.get("subscription_id")
            subscription = subscriptions.get(str(subscription_id), {})
            
            # Check if this subscription belongs to our investor
            if subscription.get("investor_id") == investor_id:
                # Filter by status if specified
                if status and redemption.get("status") != status:
                    continue
                
                # Enrich with fund details
                fund_id = subscription.get("fund_id")
                fund_details = funds.get(str(fund_id), {})
                
                enriched_redemption = {
                    **redemption,
                    "fund_id": fund_id,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type"),
                    "original_subscription_amount": subscription.get("amount")
                }
                redemptions.append(enriched_redemption)
        
        return json.dumps(redemptions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_redemptions",
                "description": "View all redemption requests including pending, approved, processed, and cancelled transactions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {
                            "type": "string",
                            "description": "ID of the investor"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by redemption status",
                            "enum": ["pending", "approved", "processed", "cancelled"]
                        }
                    },
                    "required": ["investor_id"]
                }
            }
        }
