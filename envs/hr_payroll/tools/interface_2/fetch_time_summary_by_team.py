import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class FetchTimeSummaryByTeam(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        team_id: str,
        start_date: str = None,
        end_date: str = None,
        worker_type: str = None,
        time_entry_ids: List[str] = None,
        status: str = None,
        project_code: str = None
    ) -> str:
        team_members = data.get("team_members", {})
        time_entries = data.get("time_entries", {})
        workers = data.get("workers", {})

        # Step 1: Find valid worker_ids in the team
        member_worker_ids = {
            m["worker_id"]
            for m in team_members.values()
            if m["team_id"] == team_id
        }

        # Step 2: Apply worker_type filter if specified
        if worker_type:
            member_worker_ids = {
                wid for wid in member_worker_ids
                if workers.get(wid, {}).get("worker_type") == worker_type
            }

        summary = {}
        filtered_entries = []

        def in_range(date_str: str) -> bool:
            if not date_str:
                return False
            if start_date and date_str < start_date:
                return False
            if end_date and date_str > end_date:
                return False
            return True

        for entry_id, entry in time_entries.items():
            if time_entry_ids and entry_id not in time_entry_ids:
                continue
            if entry["worker_id"] not in member_worker_ids:
                continue
            if status and entry.get("status") != status:
                continue
            if project_code and entry.get("project_code") != project_code:
                continue
            if (start_date or end_date) and not in_range(entry.get("date")):
                continue

            duration = entry.get("duration_hours", 0)
            entry_date = entry.get("date")
            summary[entry_date] = summary.get(entry_date, 0) + duration
            filtered_entries.append({"time_entry_id": entry_id, **entry})

        return json.dumps({
            "team_id": team_id,
            "summary_by_date": summary,
            "entries": filtered_entries
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_time_summary_by_team",
                "description": (
                    "Fetches time entries and daily hour totals for a team. "
                    "Supports filtering by date range, worker type, time entry IDs, entry status, and project code."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_id": {
                            "type": "string",
                            "description": "The ID of the team to fetch time entry summaries for"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date to filter time entries (YYYY-MM-DD)"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date to filter time entries (YYYY-MM-DD)"
                        },
                        "worker_type": {
                            "type": "string",
                            "description": "Filter only entries by workers of this type"
                        },
                        "time_entry_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter to only include specified time entry IDs"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter entries by their status (e.g., 'draft', 'submitted')"
                        },
                        "project_code": {
                            "type": "string",
                            "description": "Filter entries with this project code"
                        }
                    },
                    "required": ["team_id"]
                }
            }
        }
