
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ApproveOvertimeEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], time_entry_id: str) -> str:
        entries = data.get("time_entries", {})
        if time_entry_id not in entries:
            raise ValueError("Time entry not found")

        entry = entries[time_entry_id]
        if entry.get("status") not in ["submitted", "draft"]:
            raise ValueError("Only draft or submitted entries can be approved")

        entry["status"] = "approved"
        return json.dumps(entry)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "approve_overtime_entry",
                "description": "Marks a time entry as approved overtime",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time_entry_id": {
                            "type": "string",
                            "description": "The ID of the time entry to approve"
                        }
                    },
                    "required": ["time_entry_id"]
                }
            }
        }
