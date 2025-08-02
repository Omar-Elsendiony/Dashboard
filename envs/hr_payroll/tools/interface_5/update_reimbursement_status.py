
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateReimbursementStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, new_status: str) -> str:
        reimbursements = data.get("reimbursements", {})
        r = reimbursements.get(reimbursement_id)
        if not r:
            raise ValueError("Reimbursement not found")
        if r["status"] == "paid":
            raise ValueError("Cannot change status of a paid reimbursement")
        r["status"] = new_status
        return json.dumps({"reimbursement_id": reimbursement_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_reimbursement_status",
                "description": "Changes reimbursement status unless already paid",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {
                            "type": "string",
                            "description": "ID of the reimbursement"
                        },
                        "new_status": {
                            "type": "string",
                            "description": "New status to assign (e.g., approved, rejected)"
                        }
                    },
                    "required": ["reimbursement_id", "new_status"]
                }
            }
        }
