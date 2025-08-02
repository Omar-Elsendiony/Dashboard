
import json
from typing import Any, Dict
from collections import defaultdict
from tau_bench.envs.tool import Tool

class GetReimbursementTotalsByWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        reimbursements = data.get("reimbursements", {})
        known_statuses = ["approved", "paid", "submitted", "rejected"]

        # Initialize result with all known statuses
        result = {
            status: {
                "amount": 0.0,
                "reimbursement_ids": []
            }
            for status in known_statuses
        }

        for reimbursement_id, r in reimbursements.items():
            if r.get("worker_id") == worker_id:
                status = r.get("status", "submitted")
                if status not in result:
                    # Skip unknown statuses (or you could add them dynamically if desired)
                    continue
                amount = r.get("amount", 0.0)
                result[status]["amount"] += float(amount)
                result[status]["reimbursement_ids"].append(reimbursement_id)

        return json.dumps({
            "worker_id": worker_id,
            "totals": result
        })


    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reimbursement_totals_by_worker",
                "description": "Summarizes reimbursements for a worker across different statuses",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID to fetch reimbursement totals for"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
