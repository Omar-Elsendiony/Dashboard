import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveTeamMember(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        team_member_id: str = None,
        worker_id: str = None,
        team_id: str = None
    ) -> str:
        team_members = data.get("team_members", {})

        target_id = None

        # Case 1: Direct match via team_member_id
        if team_member_id:
            if team_member_id not in team_members:
                return json.dumps({
                    "status": "error",
                    "message": "Team member ID not found",
                    "team_member_id": team_member_id
                })
            record = team_members[team_member_id]

            # Cross-validation if worker_id or team_id is provided
            if worker_id and record.get("worker_id") != worker_id:
                return json.dumps({
                    "status": "error",
                    "message": "worker_id does not match the team_member_id",
                    "team_member_id": team_member_id
                })
            if team_id and record.get("team_id") != team_id:
                return json.dumps({
                    "status": "error",
                    "message": "team_id does not match the team_member_id",
                    "team_member_id": team_member_id
                })

            target_id = team_member_id

        # Case 2: Match by worker_id + team_id
        elif worker_id and team_id:
            for tid, record in team_members.items():
                if record.get("worker_id") == worker_id and record.get("team_id") == team_id:
                    target_id = tid
                    break
            if not target_id:
                return json.dumps({
                    "status": "error",
                    "message": "No team member found for given worker_id and team_id",
                    "worker_id": worker_id,
                    "team_id": team_id
                })
        else:
            return json.dumps({
                "status": "error",
                "message": "You must provide either team_member_id or both worker_id and team_id"
            })

        removed = team_members.pop(target_id)
        return json.dumps({
            "status": "removed",
            "team_member_id": target_id,
            **removed
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_team_member",
                "description": (
                    "Removes a team member using either team_member_id (primary key), or by providing the "
                    "combination of worker_id and team_id (unique composite). If both methods are used, they must match."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_member_id": {
                            "type": "string",
                            "description": "ID of the team member to remove (primary key)"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID (used with team_id if team_member_id not provided)"
                        },
                        "team_id": {
                            "type": "string",
                            "description": "Team ID (used with worker_id if team_member_id not provided)"
                        }
                    },
                    "required": []
                }
            }
        }
