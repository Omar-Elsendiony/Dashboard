
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RejectReimbursementRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, reason: str) -> str:
        reimbursements = data.get("reimbursements", {})
        r = reimbursements.get(reimbursement_id)
        if not r:
            raise ValueError("Reimbursement not found")
        if r["status"] in ["paid", "approved"]:
            raise ValueError("Cannot reject paid/approved reimbursement")

        r["status"] = "rejected"
        r["reject_reason"] = reason
        return json.dumps({"reimbursement_id": reimbursement_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "reject_reimbursement_request",
                "description": "Marks a reimbursement as rejected",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {
                            "type": "string",
                            "description": "ID of the reimbursement to reject"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for rejection"
                        }
                    },
                    "required": ["reimbursement_id", "reason"]
                }
            }
        }
