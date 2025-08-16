import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_user_information(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        email: Optional[str] = None
    ) -> str:
        """
        Retrieve a single user record filtered by user_id or email.
        At least one of user_id or email must be provided.
        Returns a JSON object of the matching user.
        """
        if not user_id and not email:
            raise ValueError("At least one of user_id or email must be provided")

        users = data.get("users", {})
        found_user: Optional[Dict[str, Any]] = None

        for uid, user in users.items():
            # Apply filters
            if user_id and str(uid) != user_id:
                continue
            if email and user.get("email") != email:
                continue
            found_user = user
            break

        # No matching user found
        if not found_user:
            raise ValueError(f"User not found")

        return json.dumps(found_user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_information",
                "description": "Retrieve a single user's information filtered by user ID or email (one required)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "email": {"type": "string", "description": "Filter by user email"}
                    },
                    "required": []
                }
            }
        }
