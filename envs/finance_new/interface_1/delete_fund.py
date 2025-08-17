import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, compliance_officer_approval: bool,
               fund_manager_approval: bool) -> str:
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Check for active subscriptions
        active_subscriptions = [s for s in subscriptions.values() 
                            if s.get("fund_id") == int(fund_id) and s.get("status") == "approved"]
        
        if active_subscriptions:
            return json.dumps({"error": "Cannot delete fund with active subscriptions. Process halted."})
        
        # Delete fund
        del funds[str(fund_id)]
        
        return json.dumps({"success": True, "message": "Fund deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_fund",
                "description": "Delete a fund after required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund to delete"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag (True/False)"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag (True/False)"}
                    },
                    "required": ["fund_id", "compliance_officer_approval", "fund_manager_approval"]
                }
            }
        }
