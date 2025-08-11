import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateContractForWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, rate: float, start_date: str) -> str:
        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        contract_id = str(uuid.uuid4())
        worker = workers[worker_id]
        contracts = data.setdefault("contracts", {})

        contract = {
            "worker_id": worker_id,
            "organization_id": worker["organization_id"],
            "user_id": worker["user_id"],
            "start_date": start_date,
            "end_date": None,
            "rate": round(rate, 4),
            "rate_type": "monthly",
            "status": "draft",
            "currency": "USD",
            "document_id": None
        }

        contracts[contract_id] = contract
        return json.dumps({"contract_id": contract_id, **contract})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_contract_for_worker",
                "description": "Creates a contract for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "ID of the worker"
                        },
                        "rate": {
                            "type": "number",
                            "description": "Monthly pay rate for the worker"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date of the contract in YYYY-MM-DD format"
                        }
                    },
                    "required": ["worker_id", "rate", "start_date"]
                }
            }
        }
