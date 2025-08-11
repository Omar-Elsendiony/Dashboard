import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CountTeamMembers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], team_id: str) -> str:
        team_members = data.get("team_members", {})

        count = sum(
            1 for record in team_members.values()
            if record.get("team_id") == team_id and record.get("left_at") is None
        )

        return json.dumps({
            "team_id": team_id,
            "active_member_count": count
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "count_team_members",
                "description": "Returns the number of currently active members in a team (i.e., members with no left_at date).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_id": {
                            "type": "string",
                            "description": "The ID of the team whose member count is requested"
                        }
                    },
                    "required": ["team_id"]
                }
            }
        }
