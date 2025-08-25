import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubmitPayrollItemAdjustment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        contract_id: str,
        amount: float,
        reason: str,
        worker_id: str = None,
        run_id: str = None
    ) -> str:
        contracts = data.get("contracts", {})
        payroll_items = data.setdefault("payroll_items", {})

        if contract_id not in contracts:
            raise ValueError("Invalid contract")

        contract = contracts[contract_id]
        resolved_worker_id = worker_id or contract.get("worker_id")
        org_id = contract.get("organization_id")
        user_id = contract.get("user_id")

        # Check for existing item
        for item_id, item in payroll_items.items():
            if (
                item.get("contract_id") == contract_id and
                item.get("worker_id") == resolved_worker_id and
                item.get("run_id") == run_id and
                item.get("note") == reason
            ):
                item["amount"] = round(amount, 2)
                return json.dumps({"item_id": item_id, "updated": True, **item})

        # Create new item
        new_id = str(uuid.uuid4())
        new_item = {
            "contract_id": contract_id,
            "worker_id": resolved_worker_id,
            "run_id": run_id,
            "amount": round(amount, 2),
            "currency": contract.get("currency"),
            "status": "pending",
            "user_id": user_id,
            "note": reason
        }
        payroll_items[new_id] = new_item
        return json.dumps({"item_id": new_id, "created": True, **new_item})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_payroll_item_adjustment",
                "description": (
                    "Creates or updates a payroll adjustment item. "
                    "If one exists for the same contract_id, worker_id, run_id, and reason, it will be updated; "
                    "otherwise, a new item will be created."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "Contract receiving adjustment"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Adjustment amount"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason or note for the adjustment"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Optional override for worker_id (defaults to worker in contract)"
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Optional payroll run ID"
                        }
                    },
                    "required": ["contract_id", "amount", "reason"]
                }
            }
        }
