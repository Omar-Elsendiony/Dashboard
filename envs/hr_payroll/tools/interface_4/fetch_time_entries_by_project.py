
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchTimeEntriesByProject(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], project_keyword: str) -> str:
        entries = data.get("time_entries", {})
        results = [
            {**entry, "time_entry_id": tid}
            for tid, entry in entries.items()
            if project_keyword.lower() in (entry.get("project_code") or "").lower()
        ]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_time_entries_by_project",
                "description": "Filters time entries by project name or tag",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_keyword": {
                            "type": "string",
                            "description": "A project name or keyword to filter time entries"
                        }
                    },
                    "required": ["project_keyword"]
                }
            }
        }
