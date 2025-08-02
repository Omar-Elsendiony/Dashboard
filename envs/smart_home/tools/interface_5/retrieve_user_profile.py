import json
import re
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveUserProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str = None,
               first_name: str = None,
               last_name: str = None,
               date_of_birth: str = None,
               role: str = None,
               phone_number: str = None,
               email: str = None) -> str:
        """
        Retrieve user profiles matching any combination of the given fields. All fields are optional.
        Phone numbers are compared by digits only (ignoring formatting characters) and support suffix matching.
        Email comparison is case-insensitive.
        """
        users = data.get("users", {})
        results = []

        def normalize_phone(p) -> str:
            if p is None:
                return ""
            return re.sub(r"\D", "", str(p))

        target_phone = normalize_phone(phone_number)
        target_email = email.lower() if email else None

        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if first_name and user.get("first_name") != first_name:
                continue
            if last_name and user.get("last_name") != last_name:
                continue
            if date_of_birth and user.get("date_of_birth") != date_of_birth:
                continue
            if role and user.get("role") != role:
                continue
            if phone_number:
                user_phone = normalize_phone(user.get("phone_number"))
                if not user_phone.endswith(target_phone):
                    continue
            if target_email:
                user_email = user.get("email", "").lower()
                if user_email != target_email:
                    continue
            results.append(user)

        return json.dumps(results if results else {"error": "No matching user profiles found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Metadata for the retrieve_user_profile tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "retrieve_user_profile",
                "description": "Retrieve user profiles based on any combination of ID, name, DOB, role, or contact details. Phone comparison ignores formatting and supports suffix matching. Email is case-insensitive.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user"
                        },
                        "first_name": {
                            "type": "string",
                            "description": "User's first name"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "User's last name"
                        },
                        "date_of_birth": {
                            "type": "string",
                            "description": "User's date of birth (YYYY-MM-DD)"
                        },
                        "role": {
                            "type": "string",
                            "description": "Role of the user (Owner, Partner, Child, Guest, Servant)"
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "User's phone number (digits only, suffix match supported)"
                        },
                        "email": {
                            "type": "string",
                            "description": "User's email address (case-insensitive)"
                        }
                    },
                    "required": []
                }
            }
        }
