import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ValidateFundManagerApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_approval_code: str) -> str:
        approvals = data.get("approvals", {})
        
        for approval in approvals.values():
            if (approval.get("code") == fund_approval_code and 
                approval.get("approver_role") == "fund_manager"):
                return json.dumps({"approval_valid": True})
        
        return json.dumps({"approval_valid": False})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "validate_fund_manager_approval",
                "description": "Validate fund manager approval code for Fund Management & Trading Operations. Returns boolean indicating if approval is valid.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_approval_code": {"type": "string", "description": "Fund manager approval code for validation (e.g., FUND0001)"}
                    },
                    "required": ["fund_approval_code"]
                }
            }
        }
