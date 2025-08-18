import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               status: Optional[str] = None, fund_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})  # Back to dictionary with default {}
        funds = data.get("funds", {})

        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get subscriptions for this investor
        final_subscriptions = []
        
        # Debug: Check what type subscriptions actually is
        if not isinstance(subscriptions, dict):
            raise ValueError(f"Expected subscriptions to be a dict, but got {type(subscriptions)}")
        
        for subscription in subscriptions.values():
            # Compare as strings to handle type mismatches
            if str(subscription.get("investor_id")) == str(investor_id):
                # Filter by status if specified
                if status and subscription.get("status") != status:
                    continue
                
                # Filter by fund if specified
                if fund_id and str(subscription.get("fund_id")) != str(fund_id):
                    continue
                
                # Enrich with fund details
                sub_fund_id = subscription.get("fund_id")
                fund_details = funds.get(str(sub_fund_id), {})
                
                enriched_subscription = {
                    **subscription,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type")
                }
                final_subscriptions.append(enriched_subscription)

        return json.dumps(final_subscriptions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_subscriptions",
                "description": "List all subscription requests and their current status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {
                            "type": "string",
                            "description": "ID of the investor"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by subscription status",
                            "enum": ["pending", "approved", "cancelled"]
                        },
                        "fund_id": {
                            "type": "string",
                            "description": "Filter by fund ID"
                        }
                    },
                    "required": ["investor_id"]
                }
            }
        }