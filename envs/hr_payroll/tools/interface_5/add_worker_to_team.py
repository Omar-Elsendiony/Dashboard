
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddWorkerToTeam(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, team_id: str) -> str:
        workers = data.get("workers", {})
        teams = data.get("teams", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")
        if team_id not in teams:
            raise ValueError("Team not found")

        worker = workers[worker_id]
        team = teams[team_id]
        if team["organization_id"] != worker["organization_id"]:
            raise ValueError("Worker and team belong to different organizations")

        member_id = str(uuid.uuid4())
        data.setdefault("team_members", {})[member_id] = {
            "team_id": team_id,
            "worker_id": worker_id,
            "role": "member",
            "joined_at": "2025-07-01",
            "left_at": None,
            "user_id": worker["user_id"]
        }
        return json.dumps({"assignment_id": member_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_worker_to_team",
                "description": "Assigns a worker to a team within the same organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "Worker to assign to the team"
                        },
                        "team_id": {
                            "type": "string",
                            "description": "Team to which the worker is assigned"
                        }
                    },
                    "required": ["worker_id", "team_id"]
                }
            }
        }
