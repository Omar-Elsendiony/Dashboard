import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListActiveWorkers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], organization_id: str) -> str:
        workers = data.get("workers", {})
        contracts = data.get("contracts", {})
        active = []

        for worker_id, w in workers.items():
            if w.get("status") != "active":
                continue
            has_active_contract = any(
                c.get("worker_id") == worker_id and
                c.get("status") in ["active", "signed"] and
                c.get("organization_id") == organization_id
                for c in contracts.values()
            )
            if has_active_contract:
                active.append({**w, "worker_id": worker_id})

        return json.dumps(active)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_active_workers",
                "description": "Returns active workers with valid contracts for a given organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "The ID of the organization whose active workers are to be listed"
                        }
                    },
                    "required": ["organization_id"]
                }
            }
        }
