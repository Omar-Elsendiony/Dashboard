
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNewContract(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, terms: Dict[str, Any]) -> str:
        contracts = data.setdefault("contracts", {})
        contract_id = str(uuid.uuid4())

        required_fields = ["start_date", "end_date", "rate", "rate_type", "currency"]
        for f in required_fields:
            if f not in terms:
                raise ValueError(f"Missing field in terms: {f}")
        if terms["end_date"] <= terms["start_date"]:
            raise ValueError("End date must be after start date")

        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        user_id = workers[worker_id]["user_id"]
        org_id = workers[worker_id]["organization_id"]

        contracts[contract_id] = {
            "worker_id": worker_id,
            "organization_id": org_id,
            "user_id": user_id,
            "start_date": terms["start_date"],
            "end_date": terms["end_date"],
            "rate": terms["rate"],
            "rate_type": terms["rate_type"],
            "currency": terms["currency"],
            "status": "draft",
            "document_id": None
        }
        return json.dumps({"contract_id": contract_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_contract",
                "description": "Creates a new contract for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker"
                        },
                        "terms": {
                            "type": "object",
                            "description": "Terms of the contract",
                            "properties": {
                                "start_date": {"type": "string", "description": "Contract start date"},
                                "end_date": {"type": "string", "description": "Contract end date"},
                                "rate": {"type": "number", "description": "Payment rate"},
                                "rate_type": {"type": "string", "description": "Rate type"},
                                "currency": {"type": "string", "description": "Payment currency"}
                            },
                            "required": ["start_date", "end_date", "rate", "rate_type", "currency"]
                        }
                    },
                    "required": ["worker_id", "terms"]
                }
            }
        }
