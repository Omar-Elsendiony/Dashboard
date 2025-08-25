import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserLocaleAndTimezone(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str = None, worker_id: str = None) -> str:
        users = data.get("users", {})
        workers = data.get("workers", {})

        # Resolve user_id using worker_id if needed
        if not user_id:
            if not worker_id:
                raise ValueError("Either user_id or worker_id must be provided")
            if worker_id not in workers:
                raise ValueError("Worker not found")
            user_id = workers[worker_id].get("user_id")

        user = users.get(user_id)
        if not user:
            raise ValueError("User not found")

        return json.dumps({
            "user_id": user_id,
            "locale": user.get("locale"),
            "timezone": user.get("timezone")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_locale_and_timezone",
                "description": "Retrieves user locale and timezone info. Either user_id or worker_id must be provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user (takes precedence if both IDs are given)"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker (used to resolve user_id if user_id is not provided)"
                        }
                    },
                    "required": []
                }
            }
        }
