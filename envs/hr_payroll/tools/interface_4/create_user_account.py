import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUserAccount(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str = None,
        email: str = None,
        role: str = None,
        first_name: str = None,
        last_name: str = None,
        locale: str = "en-US",
        timezone: str = "UTC",
        status: str = "active",
        password_hash: str = "dummyhash"
    ) -> str:
        users = data.setdefault("users", {})

        if not email:
            raise ValueError("Email is required")
        if not role:
            raise ValueError("Role is required")
        if any(u.get("email") == email for u in users.values()):
            raise ValueError("Email already exists")

        user_id = str(uuid.uuid4())

        # Derive first/last name from 'name' if not explicitly given
        if not first_name and name:
            parts = name.strip().split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

        user = {
            "first_name": first_name or "",
            "last_name": last_name or "",
            "email": email,
            "role": role,
            "timezone": timezone,
            "locale": locale,
            "password_hash": password_hash,
            "status": status
        }

        users[user_id] = user
        return json.dumps({"user_id": user_id, **user})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user_account",
                "description": (
                    "Creates a new user with full profile details. Either full name (via `name`) "
                    "or `first_name`/`last_name` must be provided. "
                    "Default values will be used if optional fields are not provided."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Full name of the user (used only if first_name and last_name are not provided)"
                        },
                        "first_name": {
                            "type": "string",
                            "description": "First name of the user"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "Last name of the user"
                        },
                        "email": {
                            "type": "string",
                            "description": "Email address of the user"
                        },
                        "role": {
                            "type": "string",
                            "description": "Role to assign to the user (e.g., admin, employee)"
                        },
                        "locale": {
                            "type": "string",
                            "description": "Locale of the user (e.g., en-US, ru_UA). Default is en-US"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone of the user (e.g., UTC, Asia/Kolkata). Default is UTC"
                        },
                        "status": {
                            "type": "string",
                            "description": "Account status (e.g., active, pending). Default is active"
                        },
                        "password_hash": {
                            "type": "string",
                            "description": "Hashed password of the user. Default is dummyhash"
                        }
                    },
                    "required": ["email", "role"]
                }
            }
        }
