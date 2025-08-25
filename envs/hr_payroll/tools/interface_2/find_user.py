import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FindUser(Tool):
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
        results = []

        for uid, user in users.items():
            if user_id and uid != user_id:
                continue
            if email and user.get("email") != email:
                continue
            if first_name and user.get("first_name") != first_name:
                continue
            if last_name and user.get("last_name") != last_name:
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if locale and user.get("locale") != locale:
                continue
            if timezone and user.get("timezone") != timezone:
                continue

            user_workers = [
                {"worker_id": wid, **w}
                for wid, w in workers.items()
                if w.get("user_id") == uid
            ]
            results.append({"user_id": uid, **user, "workers": user_workers})

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_user",
                "description": "Search for users based on filters such as user ID, email, name, role, etc. Also returns any worker records linked to the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "email": {"type": "string", "description": "Email of the user"},
                        "first_name": {"type": "string", "description": "First name of the user"},
                        "last_name": {"type": "string", "description": "Last name of the user"},
                        "role": {"type": "string", "description": "Role assigned to the user"},
                        "status": {"type": "string", "description": "Status of the user account"},
                        "locale": {"type": "string", "description": "User's locale"},
                        "timezone": {"type": "string", "description": "User's timezone"}
                    },
                    "required": []
                }
            }
        }
