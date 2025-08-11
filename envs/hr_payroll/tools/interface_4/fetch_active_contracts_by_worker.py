
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchActiveContractsByWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        contracts = data.get("contracts", {})
        active_contracts = [
            {**c, "contract_id": cid}
            for cid, c in contracts.items()
            if c.get("worker_id") == worker_id and c.get("status") in ["active", "signed"]
        ]
        return json.dumps(active_contracts)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_active_contracts_by_worker",
                "description": "Gets active contracts for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker whose active contracts are being retrieved"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
