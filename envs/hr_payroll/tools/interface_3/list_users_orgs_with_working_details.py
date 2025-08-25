import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListUsersOrgsWithWorkingDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        role: str = None,
        status: str = None,
        locale: str = None,
        timezone: str = None
    ) -> str:
        users = data.get("users", {})
        workers = data.get("workers", {})
        orgs = data.get("organizations", {})

        def user_matches(u: Dict[str, Any]) -> bool:
            return (
                (not user_id or u[0] == user_id) and
                (not email or u[1].get("email") == email) and
                (not first_name or u[1].get("first_name") == first_name) and
                (not last_name or u[1].get("last_name") == last_name) and
                (not role or u[1].get("role") == role) and
                (not status or u[1].get("status") == status) and
                (not locale or u[1].get("locale") == locale) and
                (not timezone or u[1].get("timezone") == timezone)
            )

        result = []
        for uid, user in filter(user_matches, users.items()):
            user_workers = []
            for wid, worker in workers.items():
                if worker.get("user_id") != uid:
                    continue
                org_id = worker.get("organization_id")
                org_details = orgs.get(org_id, {})
                user_workers.append({
                    "worker_id": wid,
                    **worker,
                    "organization": {
                        "organization_id": org_id,
                        **org_details
                    }
                })

            result.append({
                "user_id": uid,
                **user,
                "workers": user_workers
            })

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_users_orgs_with_working_details",
                "description": "Returns user(s) with associated workers and organization details. Filters can be applied on user fields.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Filter by exact user ID"
                        },
                        "email": {
                            "type": "string",
                            "description": "Filter by email"
                        },
                        "first_name": {
                            "type": "string",
                            "description": "Filter by first name"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "Filter by last name"
                        },
                        "role": {
                            "type": "string",
                            "description": "Filter by user role"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by user status"
                        },
                        "locale": {
                            "type": "string",
                            "description": "Filter by user locale"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Filter by user timezone"
                        }
                    },
                    "required": []
                }
            }
        }
