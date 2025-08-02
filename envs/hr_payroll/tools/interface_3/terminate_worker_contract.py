import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from datetime import date

class TerminateWorkerContract(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        contract_id: str = None,
        worker_id: str = None,
        organization_id: str = None,
        document_id: str = None
    ) -> str:
        contracts = data.get("contracts", {})
        target_id = None

        # Priority 1: contract_id
        if contract_id:
            if contract_id not in contracts:
                raise ValueError("Contract not found")
            target_id = contract_id

        # Priority 2: document_id
        elif document_id:
            matches = [cid for cid, c in contracts.items() if c.get("document_id") == document_id]
            if not matches:
                raise ValueError("No contract found with the given document_id")
            if len(matches) > 1:
                raise ValueError("Multiple contracts found with the same document_id")
            target_id = matches[0]

        # Priority 3: worker_id + organization_id
        elif worker_id and organization_id:
            matches = [
                cid for cid, c in contracts.items()
                if c.get("worker_id") == worker_id and c.get("organization_id") == organization_id
            ]
            if not matches:
                raise ValueError("No contract found for the given worker_id and organization_id")
            if len(matches) > 1:
                raise ValueError("Multiple contracts found for the given worker_id and organization_id")
            target_id = matches[0]

        else:
            raise ValueError("Must provide either contract_id, document_id, or worker_id and organization_id")

        contracts[target_id]["status"] = "terminated"
        contracts[target_id]["end_date"] = str(date.today())

        return json.dumps({
            "contract_id": target_id,
            "status": "terminated",
            "end_date": contracts[target_id]["end_date"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "terminate_worker_contract",
                "description": (
                    "Terminates a worker's contract using one of the following: "
                    "contract_id (preferred), document_id, or the combination of worker_id + organization_id. "
                    "Sets status to 'terminated' and records today's date as end_date."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "Contract ID (preferred method)"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID (used with organization_id)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID (used with worker_id)"
                        },
                        "document_id": {
                            "type": "string",
                            "description": "Document ID associated with the contract"
                        }
                    },
                    "required": []
                }
            }
        }
