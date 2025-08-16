import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class InvestorOffboarding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, reason_code: str, 
               compliance_officer_approval: bool) -> str:
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        # Check for active subscriptions
        active_subscriptions = [s for s in subscriptions.values() 
                              if s.get("investor_id") == int(investor_id) and s.get("status") == "approved"]
        
        if active_subscriptions:
            return json.dumps({"error": "Cannot offboard investor with active subscriptions. Process halted."})
        
        # Remove investor (in practice, might just mark as inactive)
        del investors[str(investor_id)]
        
        return json.dumps({"success": True, "message": "Offboarding complete"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "investor_offboarding",
                "description": "Offboard an investor after compliance approval",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor to offboard"},
                        "reason_code": {"type": "string", "description": "Reason code for offboarding"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval for offboarding"}
                    },
                    "required": ["investor_id", "reason_code", "compliance_officer_approval"]
                }
            }
        }
