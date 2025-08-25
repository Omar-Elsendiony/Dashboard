import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateWorker(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        worker_type: str,
        status: str,
        organization_id: str
    ) -> str:
        workers = data.setdefault("workers", {})

        # Optional validations
        if "users" in data and user_id not in data["users"]:
            raise ValueError("User ID does not exist")
        if "organizations" in data and organization_id not in data["organizations"]:
            raise ValueError("Organization ID does not exist")

        worker_id = str(uuid.uuid4())
        workers[worker_id] = {
            "user_id": user_id,
            "worker_type": worker_type,
            "status": status,
            "organization_id": organization_id
        }

        return json.dumps({"worker_id": worker_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_worker",
                "description": "Creates a new worker profile using user_id, worker_type, status, and organization_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user to associate with the worker"
                        },
                        "worker_type": {
                            "type": "string",
                            "description": "Type of worker (e.g., employee, contractor)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Worker status (e.g., active, inactive)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID to assign the worker under"
                        }
                    },
                    "required": ["user_id", "worker_type", "status", "organization_id"]
                }
            }
        }


    