import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommitmentApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], approval_code: str) -> bool:
        approvals = data.get("approvals", {})
        
        for approval in approvals.values():
            if approval.get("code") == approval_code:
                return True
        
        return False

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "GetCommitmentApproval",
                "description": "Check if an approval record exists by its unique approval code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "approval_code": {"type": "string", "description": "Unique approval code (e.g., INV1-COMMIT-37)"}
                    },
                    "required": ["approval_code"]
                }
            }
        }
