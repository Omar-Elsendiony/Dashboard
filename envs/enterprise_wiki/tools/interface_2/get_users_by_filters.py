import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUsersByFilters(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        status: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        locale: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> str:
        users = data.get("users", {})
        filtered_users = []
        
        if (status is None and username is None and email is None and locale is None and timezone is None):
            raise ValueError("At least one filter criterion must be provided.")

        for user in users.values():
            if status and user.get("status") != status:
                continue
            if username and user.get("username") != username:
                continue
            if email and user.get("email") != email:
                continue
            if locale and user.get("locale") != locale:
                continue
            if timezone and user.get("timezone") != timezone:
                continue
            filtered_users.append(user)

        return json.dumps(filtered_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users_by_filters",
                "description": "Get users filtered by any combination of user fields",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "User status (e.g., active, inactive, suspended)"},
                        "username": {"type": "string", "description": "Exact match on username"},
                        "email": {"type": "string", "description": "Exact match on email"},
                        "locale": {"type": "string", "description": "Locale (e.g., en_GB, en_US)"},
                        "timezone": {"type": "string", "description": "Timezone (e.g., Europe/London, America/New_York)"}
                    }
                }
            }
        }
