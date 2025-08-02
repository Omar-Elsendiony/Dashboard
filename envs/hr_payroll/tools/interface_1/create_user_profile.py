
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUserProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, email: str, role: str, timezone: str) -> str:
        users = data.setdefault("users", {})
        if any(u.get("email") == email for u in users.values()):
            raise ValueError("Email already exists")

        user_id = str(uuid.uuid4())
        first_name, *last = name.split()
        users[user_id] = {
            "first_name": first_name,
            "last_name": " ".join(last) if last else "",
            "email": email,
            "role": role,
            "timezone": timezone,
            "locale": "en-US",
            "password_hash": "not_set",
            "status": "active"
        }
        return json.dumps({"user_id": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user_profile",
                "description": "Creates a user with email, role, and timezone",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string"},
                        "timezone": {"type": "string"}
                    },
                    "required": ["name", "email", "role", "timezone"]
                }
            }
        }
