import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAnalysisApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], approval_code: str) -> str:
        approvals = data.get("approvals", {})
        
        for approval in approvals.values():
            if approval.get("code") == approval_code:
                return json.dumps(approval)
        
        raise ValueError(f"Approval with code {approval_code} not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_approval_by_code",
                "description": "Get a specific approval record by its unique approval code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "approval_code": {"type": "string", "description": "Unique approval code (e.g., INV1-COMMIT-37)"}
                    },
                    "required": ["approval_code"]
                }
            }
        }
