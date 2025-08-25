
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessReimbursementRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, amount: float, reason: str) -> str:
        workers = data.get("workers", {})
        if worker_id not in workers or workers[worker_id]["status"] != "active":
            raise ValueError("Invalid or inactive worker")

        user_id = workers[worker_id]["user_id"]
        org_id = workers[worker_id]["organization_id"]
        contract_id = next((cid for cid, c in data.get("contracts", {}).items() if c["worker_id"] == worker_id), None)

        if not contract_id:
            raise ValueError("No contract found for worker")

        reimb_id = str(uuid.uuid4())
        reimbursements = data.setdefault("reimbursements", {})
        reimbursements[reimb_id] = {
            "worker_id": worker_id,
            "organization_id": org_id,
            "amount": round(amount, 2),
            "currency": "USD",
            "status": "submitted",
            "submit_date": "2025-07-01",
            "approve_date": None,
            "user_id": user_id,
            "contract_id": contract_id,
            "description": reason
        }

        return json.dumps({"reimbursement_id": reimb_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_reimbursement_request",
                "description": "Creates a reimbursement record for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker submitting the reimbursement"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to be reimbursed"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for the reimbursement request"
                        }
                    },
                    "required": ["worker_id", "amount", "reason"]
                }
            }
        }
