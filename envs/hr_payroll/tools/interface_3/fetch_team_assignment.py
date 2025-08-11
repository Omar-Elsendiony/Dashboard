
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchTeamAssignment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        team_members = data.get("team_members", {})
        teams = [
            {**tm, "team_member_id": tid}
            for tid, tm in team_members.items()
            if tm.get("worker_id") == worker_id
        ]
        return json.dumps(teams)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_team_assignment",
                "description": "Lists team assignment(s) of a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker whose team assignments are requested"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
