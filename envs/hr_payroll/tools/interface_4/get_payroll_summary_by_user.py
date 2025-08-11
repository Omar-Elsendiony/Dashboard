import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPayrollSummaryByUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str = None,
        worker_id: str = None,
        contract_id: str = None,
        run_id: str = None
    ) -> str:
        items = data.get("payroll_items", {})

        if not any([user_id, worker_id, contract_id, run_id]):
            raise ValueError("At least one filter must be provided")

        def matches(item):
            if item.get("status") != "paid":
                return False
            if user_id and item.get("user_id") != user_id:
                return False
            if worker_id and item.get("worker_id") != worker_id:
                return False
            if contract_id and item.get("contract_id") != contract_id:
                return False
            if run_id and item.get("run_id") != run_id:
                return False
            return True

        total_paid = sum(item.get("amount", 0) for item in items.values() if matches(item))

        return json.dumps({
            "user_id": user_id,
            "worker_id": worker_id,
            "contract_id": contract_id,
            "run_id": run_id,
            "total_paid": round(total_paid, 2)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_summary_by_user",
                "description": (
                    "Summarizes total payroll paid to a user. Supports optional filters: "
                    "user_id, worker_id, contract_id, and run_id. All filters are optional, "
                    "but at least one must be provided. Status is always filtered to 'paid'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Filter by user ID"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Filter by worker ID"
                        },
                        "contract_id": {
                            "type": "string",
                            "description": "Filter by contract ID"
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Filter by payroll run ID"
                        }
                    },
                    "required": []
                }
            }
        }
