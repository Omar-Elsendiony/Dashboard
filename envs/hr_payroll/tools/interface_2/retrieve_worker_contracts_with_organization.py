import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveWorkerContractsWithOrganization(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, org_id: str) -> str:
        contracts = data.get("contracts", {})
        result = [
            {**c, "contract_id": cid}
            for cid, c in contracts.items()
            if c.get("worker_id") == worker_id and c.get("organization_id") == org_id
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_worker_contracts_with_organization",
                "description": "Returns documents linked to a contract for a specific worker and organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker whose contracts are being retrieved"
                        },
                        "org_id": {
                            "type": "string",
                            "description": "The ID of the organization where the worker is employed"
                        }
                    },
                    "required": ["worker_id", "org_id"]
                }
            }
        }
