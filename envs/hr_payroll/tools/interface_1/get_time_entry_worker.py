import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTimeEntryWorker(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        worker_id: str,
        description: str = None,
        time_entry_id: str = None
    ) -> str:
        time_entries = data.get("time_entries", {})

        def matches(entry_id, entry):
            if time_entry_id and entry_id != time_entry_id:
                return False
            if entry.get("worker_id") != worker_id:
                return False
            if description and description.lower() not in entry.get("description", "").lower():
                return False
            return True

        results = [
            {**entry, "time_entry_id": entry_id}
            for entry_id, entry in time_entries.items()
            if matches(entry_id, entry)
        ]

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_time_entry_worker",
                "description": (
                    "Fetches time entries logged by a worker. Supports optional filters for description "
                    "(partial match) and time_entry_id (exact match; this is the dictionary key)."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker whose time entries are being fetched"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional case-insensitive filter for the description field"
                        },
                        "time_entry_id": {
                            "type": "string",
                            "description": "Optional exact match on the time entry ID (key of the time_entries object)"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
