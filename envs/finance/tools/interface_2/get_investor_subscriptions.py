import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               status: Optional[str] = None, target_fund_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get subscriptions for this investor
        subscriptions = []
        for subscription in subscriptions.values():
            if subscription.get("investor_id") == investor_id:
                # Filter by status if specified
                if status and subscription.get("status") != status:
                    continue
                
                # Filter by fund if specified
                if target_fund_id and subscription.get("target_fund_id") != target_fund_id:
                    continue
                
                # Enrich with fund details
                sub_fund_id = subscription.get("target_fund_id")
                fund_details = funds.get(str(sub_fund_id), {})
                
                enriched_subscription = {
                    **subscription,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type")
                }
                subscriptions.append(enriched_subscription)
        
        return json.dumps(subscriptions)

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
                        "target_fund_id": {
                            "type": "string",
                            "description": "Filter by fund ID"
                        }
                    },
                    "required": ["investor_id"]
                }
            }
        }
