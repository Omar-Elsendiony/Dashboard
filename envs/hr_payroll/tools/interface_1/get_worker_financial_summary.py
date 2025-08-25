
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetWorkerFinancialSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        payroll_items = data.get("payroll_items", {})
        reimbursements = data.get("reimbursements", {})

        total_payroll = sum(item.get("amount", 0) for item in payroll_items.values() if item.get("worker_id") == worker_id)
        total_reimb = sum(item.get("amount", 0) for item in reimbursements.values() if item.get("worker_id") == worker_id)

        return json.dumps({
            "worker_id": worker_id,
            "total_payroll_amount": round(total_payroll, 2),
            "total_reimbursements_amount": round(total_reimb, 2)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_worker_financial_summary",
                "description": "Summarizes payroll and reimbursements for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {"type": "string"}
                    },
                    "required": ["worker_id"]
                }
            }
        }
