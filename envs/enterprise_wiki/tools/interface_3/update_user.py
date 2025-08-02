import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: int,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        display_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        timezone: Optional[str] = None,
        locale: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        user = users.get(str(user_id))
        if not user:
            raise ValueError("User not found")

        if email is None and first_name is None and last_name is None and display_name is None and avatar_url is None and timezone is None and locale is None and status is None:
            raise ValueError("At least one field must be provided for update.")

        if email is not None:
            user["email"] = email
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if display_name is not None:
            user["display_name"] = display_name
        if avatar_url is not None:
            user["avatar_url"] = avatar_url
        if timezone is not None:
            user["timezone"] = timezone
        if locale is not None:
            user["locale"] = locale
        if status is not None:
            user["status"] = status

        return json.dumps({"status": "updated", "user": user})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user",
                "description": "Update allowed fields of a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "ID of the user"},
                        "email": {"type": "string", "description": "User email"},
                        "first_name": {"type": "string", "description": "User first name"},
                        "last_name": {"type": "string", "description": "User last name"},
                        "display_name": {"type": "string", "description": "User display name"},
                        "avatar_url": {"type": "string", "description": "User avatar URL"},
                        "timezone": {"type": "string", "description": "User timezone"},
                        "locale": {"type": "string", "description": "User locale"},
                        "status": {"type": "string", "description": "User status (e.g. active, inactive)"}
                    },
                    "required": ["user_id"]
                }
            }
        }
