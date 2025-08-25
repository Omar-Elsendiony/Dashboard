import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LogBonusPayrollItem(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, amount: float, run_id: str = None) -> str:
        workers = data.get("workers", {})
        contracts = data.get("contracts", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        contract_id = next(
            (cid for cid, c in contracts.items()
             if c.get("worker_id") == worker_id and c.get("status") in ["active", "signed"]),
            None
        )
        if not contract_id:
            raise ValueError("No active contract found for worker")

        payroll_items = data.setdefault("payroll_items", {})
        item_id = str(uuid.uuid4())
        payroll_items[item_id] = {
            "run_id": run_id,
            "worker_id": worker_id,
            "contract_id": contract_id,
            "amount": round(amount, 2),
            "currency": "USD",
            "status": "pending",
            "user_id": workers[worker_id]["user_id"]
        }

        return json.dumps({"payroll_item_id": item_id, **payroll_items[item_id]})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_bonus_payroll_item",
                "description": "Logs a bonus payroll item for a worker with an active contract. Optionally supports assigning to a specific run ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "Worker to assign the bonus to"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to log as bonus"
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Optional payroll run ID to associate the item with"
                        }
                    },
                    "required": ["worker_id", "amount"]
                }
            }
        }
