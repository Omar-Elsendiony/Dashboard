import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorSubscriptionList(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], target_fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None, investor_status: Optional[str] = None,
               request_assigned_to: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if target_fund_id and subscription.get("target_fund_id") != target_fund_id:
                continue
            if investor_id and subscription.get("investor_id") != investor_id:
                continue
            if investor_status and subscription.get("investor_status") != investor_status:
                continue
            if request_assigned_to and subscription.get("request_assigned_to") != request_assigned_to:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "investor_name": "get_subscriptions",
                "description": "Get subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "investor_status": {"type": "string", "description": "Filter by investor_status (pending, approved, cancelled)"},
                        "request_assigned_to": {"type": "string", "description": "Filter by assigned user ID"}
                    },
                    "required": []
                }
            }
        }
