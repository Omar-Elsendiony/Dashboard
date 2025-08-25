
import json
from typing import Any, Dict
from datetime import date
from tau_bench.envs.tool import Tool

class FetchTimeEntriesByPeriod(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        start_date: str,
        end_date: str,
        worker_id: str = None,
        status: str = None
    ) -> str:
        time_entries = data.get("time_entries", {})
        result = []

        for tid, entry in time_entries.items():
            entry_date = entry.get("date")
            if not (entry_date and start_date <= entry_date <= end_date):
                continue

            if worker_id and entry.get("worker_id") != worker_id:
                continue

            if status and entry.get("status") != status:
                continue

            result.append({**entry, "time_entry_id": tid})

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_time_entries_by_period",
                "description": "Retrieves time entries within a specified date range, optionally filtered by worker ID and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "description": "Start of date range in YYYY-MM-DD format"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End of date range in YYYY-MM-DD format"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID to filter time entries (optional)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Status to filter time entries (optional)"
                        }
                    },
                    "required": ["start_date", "end_date"]
                }
            }
        }

