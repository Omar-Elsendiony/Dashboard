import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class InvestorWithdrawal(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str,
               compliance_officer_approval: bool) -> str:
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        # Check for active subscriptions - fixed type consistency
        active_subscriptions = [s for s in subscriptions.values() 
                              if str(s.get("investor_id")) == str(investor_id) and s.get("status") == "approved"]
        
        if active_subscriptions:
            return json.dumps({
                "error": "Cannot offboard investor with active subscriptions. Process halted.",
                "active_subscriptions_count": len(active_subscriptions),
                "active_subscription_ids": [s.get("subscription_id") for s in active_subscriptions]
            })
        
        # In a real system, you might want to mark as inactive instead of deleting
        # For this implementation, we'll mark as inactive to preserve data integrity
        investor = investors[str(investor_id)]
        investor["status"] = "inactive"
        investor["offboarded_date"] = "2024-01-01"  # In practice, use current date
        
        return json.dumps({
            "message": "Offboarding complete",
            "investor_id": str(investor_id),
            "status": "inactive"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "investor_withdrawal",
                "description": "Offboard an investor after compliance approval",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor to offboard"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval for offboarding"}
                    },
                    "required": ["investor_id", "compliance_officer_approval"]
                }
            }
        }