import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AuthenticateApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], approval_code: str) -> str:
        approvals = data.get("approvals", {})
        
        for approval in approvals.values():
            if approval.get("code") == approval_code:
                return json.dumps({"approval_valid": True})
        
        return json.dumps({"approval_valid": False})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "authenticate_approval",
                "description": "Authenticate whether a given approval code exists in the approvals dataset. Returns boolean indicating if approval is valid.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "approval_code": {
                            "type": "string",
                            "description": "Approval code for validation (e.g., INV1-COMMIT-37)"
                        }
                    },
                    "required": ["approval_code"]
                }
            }
        }
