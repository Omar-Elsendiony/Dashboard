import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

import json
from typing import Any, Dict, Optional

class find_user(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[str] = None,
        role: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        results = []

        # Validate status if provided
        valid_statuses = {"active", "inactive", "suspended"}
        if status is not None and status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

        # Validate role if provided
        valid_roles = {"admin", "employee"}
        if role is not None and role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")

        for user in users.values():
            if user_id is not None and str(user.get("user_id")) != str(user_id):
                continue
            if email is not None and user.get("email", "") != email:
                continue
            if status is not None and user.get("status") != status:
                continue
            if role is not None and user.get("role") != role:
                continue
            results.append(user)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_user",
                "description": "Find users filtered by user_id, email, status, or role.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Filter by user ID"
                        },
                        "email": {
                            "type": "string",
                            "description": "Filter by email address"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status (active, inactive, suspended)"
                        },
                        "role": {
                            "type": "string",
                            "description": "Filter by role (admin, employee)"
                        }
                    },
                    "required": []
                }
            }
        }
