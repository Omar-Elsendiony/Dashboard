
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AllocateTimeEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, hours: float, task: str) -> str:
        if hours <= 0 or hours > 24:
            raise ValueError("Invalid hours range")

        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        time_entries = data.setdefault("time_entries", {})
        entry_id = str(uuid.uuid4())
        time_entries[entry_id] = {
            "worker_id": worker_id,
            "duration_hours": round(hours, 2),
            "project_code": "AUTO",
            "description": task,
            "status": "submitted",
            "date": "2025-07-01",
            "start_time": "2025-07-01T09:00:00Z",
            "end_time": "2025-07-01T17:00:00Z",
            "user_id": workers[worker_id]["user_id"]
        }
        return json.dumps({"time_entry_id": entry_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "allocate_time_entry",
                "description": "Logs time entry for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {"type": "string"},
                        "hours": {"type": "number"},
                        "task": {"type": "string"}
                    },
                    "required": ["worker_id", "hours", "task"]
                }
            }
        }
