import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        display_name: str,
        avatar_url: str = None,
        timezone: str = None,
        locale: str = None,
        status: str = "active",
        last_login_at: str = None
    ) -> str:
        users = data.get("users", {})

        created_at = updated_at = "2025-07-01T00:00:00Z"

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1    
        
        id = generate_id(users)    
        user = {
            "id": id,
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "display_name": display_name,
            "avatar_url": avatar_url,
            "timezone": timezone,
            "locale": locale,
            "status": status,
            "last_login_at": last_login_at,
            "created_at": created_at,
            "updated_at": updated_at
        }


        users[str(id)] = user
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Create a new user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "display_name": {"type": "string"},
                        "avatar_url": {"type": "string", "nullable": True},
                        "timezone": {"type": "string", "nullable": True},
                        "locale": {"type": "string", "nullable": True},
                        "status": {"type": "string", "default": "active"},
                        "last_login_at": {"type": "string", "format": "date-time", "nullable": True},
                        "created_at": {"type": "string", "format": "date-time", "nullable": True},
                        "updated_at": {"type": "string", "format": "date-time", "nullable": True}
                    },
                    "required": [
                        "username", "email", "display_name", "first_name", "last_name"
                    ]
                }
            }
        }
