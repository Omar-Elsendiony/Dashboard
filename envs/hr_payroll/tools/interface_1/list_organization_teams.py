import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOrganizationTeams(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        team_id: str = None,
        organization_id: str = None,
        name: str = None,
        description: str = None
    ) -> str:
        teams = data.get("teams", {})

        def matches(tid, team):
            if team_id and tid != team_id:
                return False
            if organization_id and team.get("organization_id") != organization_id:
                return False
            if name and name.lower() not in team.get("name", "").lower():
                return False
            if description and description.lower() not in team.get("description", "").lower():
                return False
            return True

        results = [
            {**team, "team_id": tid}
            for tid, team in teams.items()
            if matches(tid, team)
        ]

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_organization_teams",
                "description": (
                    "Lists organization teams with optional filters on team_id (key), "
                    "organization_id, name, or description. Only team_id yields a unique result."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_id": {
                            "type": "string",
                            "description": "Filter by team ID (dictionary key)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Filter by organization ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Filter by team name (case-insensitive partial match)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Filter by team description (case-insensitive partial match)"
                        }
                    },
                    "required": []
                }
            }
        }
