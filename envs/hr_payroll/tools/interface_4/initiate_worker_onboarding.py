import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class InitiateWorkerOnboarding(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        org_id: str,
        user_id: str = None,
        worker_id: str = None
    ) -> str:
        users = data.get("users", {})
        orgs = data.get("organizations", {})
        workers = data.setdefault("workers", {})

        # Validate org
        if org_id not in orgs:
            raise ValueError("Organization not found")

        # Case 1: Update existing worker's org_id
        if worker_id:
            if worker_id not in workers:
                raise ValueError("Worker not found")
            if user_id and workers[worker_id]["user_id"] != user_id:
                raise ValueError("Provided user_id does not match the worker's user_id")

            workers[worker_id]["organization_id"] = org_id
            workers[worker_id]["status"] = "onboarding"

            return json.dumps({
                "worker_id": worker_id,
                **workers[worker_id]
            })

        # Case 2: Create new worker for given user
        if not user_id:
            raise ValueError("Either worker_id or user_id must be provided")

        if user_id not in users:
            raise ValueError("User not found")

        if users[user_id]["status"] in ["suspended", "pending"]:
            raise ValueError("User is not eligible for onboarding")

        if any(w["user_id"] == user_id for w in workers.values()):
            raise ValueError("User already linked to a worker")

        new_worker_id = str(uuid.uuid4())
        workers[new_worker_id] = {
            "user_id": user_id,
            "organization_id": org_id,
            "worker_type": "employee",
            "status": "onboarding"
        }

        return json.dumps({
            "worker_id": new_worker_id,
            **workers[new_worker_id]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "initiate_worker_onboarding",
                "description": (
                    "Begins onboarding for a user or worker. "
                    "If worker_id is given, updates the organization and status. "
                    "If user_id is given, creates a new worker unless already linked."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "User to onboard (optional if worker_id is given)"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Existing worker to update with new organization"
                        },
                        "org_id": {
                            "type": "string",
                            "description": "Organization to assign for onboarding"
                        }
                    },
                    "required": ["org_id"]
                }
            }
        }
