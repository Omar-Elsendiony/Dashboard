
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetWorkerContractSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        contracts = data.get("contracts", {})
        summary = [
            {**c, "contract_id": cid}
            for cid, c in contracts.items()
            if c.get("worker_id") == worker_id and c.get("status") in ["active", "signed"]
        ]
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_worker_contract_summary",
                "description": "Returns details of worker’s current contract",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker whose contract details are being retrieved"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
