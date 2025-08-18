import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ValidateComplianceApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], compliance_approval_code: str) -> str:
        approvals = data.get("approvals", {})
        
        for approval in approvals.values():
            if (approval.get("code") == compliance_approval_code and 
                approval.get("approver_role") == "compliance_officer"):
                return json.dumps({"approval_valid": True})
        
        return json.dumps({"approval_valid": False})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "investor_name": "validate_approval_interface_2",
                "description": "Validate compliance officer approval code for Interface 2 (Investor Management & Portfolio Operations). Returns boolean indicating if approval is valid.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "compliance_approval_code": {"type": "string", "description": "Compliance officer approval code for validation (e.g., SUBCR0021)"}
                    },
                    "required": ["compliance_approval_code"]
                }
            }
        }
