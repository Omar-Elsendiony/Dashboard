
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListWorkersByOrg(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], org_id: str) -> str:
        workers = data.get("workers", {})
        filtered = [
            {**w, "worker_id": wid}
            for wid, w in workers.items()
            if w.get("organization_id") == org_id
        ]
        return json.dumps(filtered)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_workers_by_org",
                "description": "Lists workers belonging to a specific organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "org_id": {
                            "type": "string",
                            "description": "The organization ID whose workers are being queried"
                        }
                    },
                    "required": ["org_id"]
                }
            }
        }
