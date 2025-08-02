import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AssignWorkerToOrg(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, new_organization_id: str) -> str:
        workers = data.get("workers", {})
        organizations = data.get("organizations", {})

        if worker_id not in workers:
            raise ValueError(f"Worker '{worker_id}' not found.")

        if new_organization_id not in organizations:
            raise ValueError(f"Organization '{new_organization_id}' not found.")

        workers[worker_id]["organization_id"] = new_organization_id
        workers[worker_id]["updated_at"] = "2025-07-01T09:25:07.660396Z"

        return json.dumps(workers[worker_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_worker_to_org",
                "description": "Assign or reassign a worker to a new organization.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "ID of the worker to update."
                        },
                        "new_organization_id": {
                            "type": "string",
                            "description": "ID of the organization to assign."
                        }
                    },
                    "required": ["worker_id", "new_organization_id"]
                }
            }
        }
