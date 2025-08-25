import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AssignWorkerToTeam(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        worker_id: str,
        team_id: str,
        role: str,
        joined_at: str
    ) -> str:
        team_members = data.setdefault("team_members", {})

        # Optional validations
        if "users" in data and user_id not in data["users"]:
            raise ValueError("User ID not found")
        if "workers" in data and worker_id not in data["workers"]:
            raise ValueError("Worker ID not found")
        if "teams" in data and team_id not in data["teams"]:
            raise ValueError("Team ID not found")

        team_member_id = str(uuid.uuid4())

        new_record = {
            "user_id": user_id,
            "worker_id": worker_id,
            "team_id": team_id,
            "role": role,
            "joined_at": joined_at,
            "left_at": None
        }

        team_members[team_member_id] = new_record

        return json.dumps({
            "team_member_id": team_member_id,
            **new_record
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_worker_to_team",
                "description": "Assigns a worker to a team by creating a team member record. Returns the full record including team_member_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "User ID associated with the worker"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "The worker ID to assign to the team"
                        },
                        "team_id": {
                            "type": "string",
                            "description": "The ID of the team to assign the worker to"
                        },
                        "role": {
                            "type": "string",
                            "description": "The role of the worker in the team (e.g., lead, member)"
                        },
                        "joined_at": {
                            "type": "string",
                            "description": "The date the worker joined the team (format: YYYY-MM-DD)"
                        }
                    },
                    "required": ["user_id", "worker_id", "team_id", "role", "joined_at"]
                }
            }
        }
