import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class StartNewEngagement(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        organization_id: str,
        status: str = "active",
        worker_type: str = "employee",
        time_entry: Dict[str, Any] = None
    ) -> str:
        users = data.get("users", {})
        orgs = data.get("organizations", {})
        if organization_id not in orgs:
            raise ValueError("Organization not found")

        # Resolve user_id from full name
        matched_user_id = None
        for uid, u in users.items():
            full_name = f"{u.get('first_name', '').strip()} {u.get('last_name', '').strip()}".strip()
            if full_name.lower() == name.strip().lower():
                matched_user_id = uid
                break

        if not matched_user_id:
            raise ValueError("No user found with the given name")

        workers = data.setdefault("workers", {})
        if any(w["user_id"] == matched_user_id and w["organization_id"] == organization_id for w in workers.values()):
            raise ValueError("This user already has a worker in the given organization")

        # Create worker
        worker_id = str(uuid.uuid4())
        workers[worker_id] = {
            "user_id": matched_user_id,
            "organization_id": organization_id,
            "status": status,
            "worker_type": worker_type
        }

        response = {
            "worker_id": worker_id,
            **workers[worker_id]
        }

        # Optionally create time entry
        if time_entry:
            entries = data.setdefault("time_entries", {})
            time_entry_id = str(uuid.uuid4())
            entries[time_entry_id] = {
                "user_id": matched_user_id,
                "worker_id": worker_id,
                "status": time_entry.get("status", "draft"),
                "description": time_entry.get("description", ""),
                "project_code": time_entry.get("project_code"),
                "duration_hours": time_entry.get("duration_hours"),
                "start_time": time_entry.get("start_time"),
                "end_time": time_entry.get("end_time"),
                "date": time_entry.get("date")
            }
            response["time_entry"] = {"time_entry_id": time_entry_id, **entries[time_entry_id]}

        return json.dumps(response)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "start_new_engagement",
                "description": (
                    "Creates a new worker for a user identified by full name in a given organization. "
                    "Optionally allows logging the first time entry along with worker creation."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Full name of the user (e.g., 'Brent Bartlett')"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "ID of the organization where engagement is started"
                        },
                        "status": {
                            "type": "string",
                            "description": "Status of the worker (default: 'active')"
                        },
                        "worker_type": {
                            "type": "string",
                            "description": "Type of worker (e.g., 'employee', 'contractor')"
                        },
                        "time_entry": {
                            "type": "object",
                            "description": "Optional time entry to log with the engagement",
                            "properties": {
                                "description": {"type": "string"},
                                "project_code": {"type": "string"},
                                "status": {"type": "string"},
                                "duration_hours": {"type": "number"},
                                "start_time": {"type": "string"},
                                "end_time": {"type": "string"},
                                "date": {"type": "string"}
                            }
                        }
                    },
                    "required": ["name", "organization_id"]
                }
            }
        }
