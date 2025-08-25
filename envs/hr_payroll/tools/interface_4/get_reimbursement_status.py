
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetReimbursementStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str) -> str:
        reimbursements = data.get("reimbursements", {})
        r = reimbursements.get(reimbursement_id)
        if not r:
            raise ValueError("Reimbursement not found")

        return json.dumps({
            "reimbursement_id": reimbursement_id,
            "status": r.get("status")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reimbursement_status",
                "description": "Returns current status of a reimbursement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {
                            "type": "string",
                            "description": "The ID of the reimbursement record"
                        }
                    },
                    "required": ["reimbursement_id"]
                }
            }
        }
