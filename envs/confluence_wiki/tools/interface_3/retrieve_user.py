import json
from typing import Any, Dict, Literal, Optional
from tau_bench.envs.tool import Tool


class RetrieveUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        identifier: str,
        identifier_type: str = "user_id",
    ) -> str:
        """
        Retrieve user details by ID or email.
        """

        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        users = data.get("users", {})

        if identifier_type == "user_id":
            if str(identifier) in users:
                user_data = users[str(identifier)].copy()
                return json.dumps({"success": True, "user_data": user_data})
            else:
                return json.dumps(
                    {"success": False, "error": f"User {identifier} not found"}
                )
        elif identifier_type == "email":
            for user_id, user in users.items():
                if user.get("email") == identifier:
                    user_data = user.copy()
                    return json.dumps({"success": True, "user_data": user_data})
            return json.dumps(
                {"success": False, "error": f"User with email '{identifier}' not found"}
            )
        else:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid identifier_type '{identifier_type}'. Must be 'user_id' or 'email'",
                }
            )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_user",
                "description": "Retrieves detailed information about a user from the Wiki system. You can look up users by their unique user ID or by their email address. This function returns the user's profile data including their ID, email, name, and other associated metadata.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "identifier": {
                            "type": "string",
                            "description": "The value used to identify the user. This can be either a user ID or an email address. Required field.",
                        },
                        "identifier_type": {
                            "type": "string",
                            "description": "Specifies what type of identifier you're providing. The accepted values are 'user_id' and 'email'. Use 'user_id' when searching by user ID, or 'email' when searching by email address. If not specified, defaults to 'user_id'.",
                        },
                    },
                    "required": ["identifier"],
                },
            },
        }
