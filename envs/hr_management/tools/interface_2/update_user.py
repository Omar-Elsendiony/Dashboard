import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        role: Optional[str] = None,
        status: Optional[str] = None,
        mfa_enabled: Optional[bool] = None,
        phone_number: Optional[str] = None,
    ) -> str:
        """
        Update a user's mutable fields and return the updated user object.
        Signature: update_user(user_id: str, role?: str, status?: str, mfa_enabled?: bool, phone_number?: str) -> {user}
        """

        users = data.setdefault("users", {})

        # Validate user exists
        uid = str(user_id)
        if uid not in users:
            raise ValueError(f"User {user_id} not found")

        user = users[uid]

        # Validate and apply 'role' if provided
        if role is not None:
            valid_roles = [
                "hr_director", "hr_manager", "recruiter", "payroll_administrator",
                "hiring_manager", "finance_officer", "it_administrator",
                "compliance_officer", "employee",
            ]
            if role not in valid_roles:
                raise ValueError(f"Invalid role. Must be one of {valid_roles}")
            user["role"] = role

        # Validate and apply 'status' if provided
        if status is not None:
            valid_statuses = ["active", "inactive", "suspended"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            user["status"] = status

        # Validate and apply 'mfa_enabled' if provided
        if mfa_enabled is not None:
            if not isinstance(mfa_enabled, bool):
                raise ValueError("mfa_enabled must be a boolean")
            user["mfa_enabled"] = mfa_enabled

        # Apply 'phone_number' if provided (no strict validation to keep minimal changes)
        if phone_number is not None:
            user["phone_number"] = phone_number

        # Update timestamp per tool-creation rules
        user["updated_at"] = "2025-10-01T00:00:00"

        # Return the updated user object
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user",
                "description": "Update an existing user's role, status, MFA setting, or phone number and return the updated user object.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to update"},
                        "role": {
                            "type": "string",
                            "description": "New role (optional). One of: hr_director, hr_manager, recruiter, payroll_administrator, hiring_manager, finance_officer, it_administrator, compliance_officer, employee",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (optional). One of: active, inactive, suspended",
                        },
                        "mfa_enabled": {
                            "type": "boolean",
                            "description": "Enable/disable MFA (True/False)",
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "Updated phone number (optional)",
                        },
                    },
                    "required": ["user_id"],
                },
            },
        }
