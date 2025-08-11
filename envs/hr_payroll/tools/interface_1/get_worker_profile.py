import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetWorkerProfile(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        worker_id: str = None,
        user_id: str = None,
        organization_id: str = None
    ) -> str:
        workers = data.get("workers", {})

        # Case 1: Direct lookup by worker_id
        if worker_id:
            if worker_id not in workers:
                raise ValueError("Worker not found for the given worker_id")
            worker = workers[worker_id]
            if user_id and worker.get("user_id") != user_id:
                raise ValueError("Provided user_id does not match the given worker_id")
            return json.dumps({
                "worker_id": worker_id,
                "user_id": worker.get("user_id"),
                "worker_type": worker.get("worker_type"),
                "status": worker.get("status"),
                "organization_id": worker.get("organization_id")
            })

        # Case 2: Composite key — user_id + organization_id
        if user_id and organization_id:
            for wid, w in workers.items():
                if w.get("user_id") == user_id and w.get("organization_id") == organization_id:
                    return json.dumps({
                        "worker_id": wid,
                        "user_id": w.get("user_id"),
                        "worker_type": w.get("worker_type"),
                        "status": w.get("status"),
                        "organization_id": w.get("organization_id")
                    })
            raise ValueError("Worker not found for the given user_id and organization_id")

        raise ValueError("You must provide either worker_id or both user_id and organization_id")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_worker_profile",
                "description": (
                    "Retrieves the profile of a worker using either:\n"
                    "- worker_id alone\n"
                    "- user_id and organization_id (composite key).\n"
                    "If both worker_id and user_id are provided, they must match."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The unique ID of the worker"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "The user ID associated with the worker (must be combined with organization_id)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "The organization ID (used with user_id to identify the worker)"
                        }
                    },
                    "required": []
                }
            }
        }
