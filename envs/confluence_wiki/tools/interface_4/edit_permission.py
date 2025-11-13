import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class EditPermission(Tool):
    """
    Update an existing permission.
    - Requires permission_id and operation.
    - Optionally accepts granted_by (updates who granted the permission).
    - Validates that permission exists.
    - Validates that operation is a valid enum value.
    - Validates that granted_by user exists and has status 'active' if provided.
    - Updates the permission record in place.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        permission_id: str,
        operation: str,
        granted_by: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "permission": {...}} on success
          {"success": False, "error": "..."} on error
        """

        # Basic input validation
        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid data format: 'data' must be a dict",
                }
            )

        permissions_dict = data.get("permissions", {})
        if not isinstance(permissions_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid permissions container: expected dict at data['permissions']",
                }
            )

        users_dict = data.get("users", {})
        if not isinstance(users_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid users container: expected dict at data['users']",
                }
            )

        # Validate required fields
        if permission_id is None:
            return json.dumps({"success": False, "error": "permission_id is required"})

        if operation is None:
            return json.dumps({"success": False, "error": "operation is required"})

        # Convert IDs to strings for consistent comparison
        permission_id_str = str(permission_id)

        # Validate permission exists
        if permission_id_str not in permissions_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Permission with ID '{permission_id_str}' not found",
                }
            )

        # Validate operation enum
        valid_operations = [
            "view",
            "edit",
            "create",
            "admin",
            "restrict_other_users",
        ]
        if operation not in valid_operations:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid operation value: '{operation}'. Must be one of {valid_operations}",
                }
            )

        # Validate granted_by user exists and is active if provided
        if granted_by is not None:
            granted_by_str = str(granted_by)
            if granted_by_str not in users_dict:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"User with ID '{granted_by_str}' not found",
                    }
                )

            # Validate user status is 'active'
            user = users_dict[granted_by_str]
            if not isinstance(user, dict):
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid user data for user ID '{granted_by_str}'",
                    }
                )

            user_status = user.get("status")
            if user_status != "active":
                return json.dumps(
                    {
                        "success": False,
                        "error": f"User with ID '{granted_by_str}' has status '{user_status}'. Only users with status 'active' can grant permissions.",
                    }
                )

        # Get existing permission
        existing_permission = permissions_dict[permission_id_str]
        if not isinstance(existing_permission, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid permission data for permission ID '{permission_id_str}'",
                }
            )

        # Create a copy to avoid mutating the original before validation
        updated_permission = existing_permission.copy()
        # Update operation (required field)
        updated_permission["operation"] = operation
        # Update granted_by if provided
        if granted_by is not None:
            updated_permission["granted_by"] = str(granted_by)
            # Update granted_at timestamp when granted_by changes
            updated_permission["granted_at"] = "2025-11-13T12:00:00"
        # Update permission in data (modify in place)
        permissions_dict[permission_id_str] = updated_permission

        return json.dumps({"success": True, "permission": updated_permission})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "edit_permission",
                "description": (
                    "Update an existing permission. "
                    "Requires permission_id and operation. "
                    "Optionally accepts granted_by to update who granted the permission. "
                    "Validates that permission exists, operation is valid, and granted_by user exists and has status 'active' if provided. "
                    "Updates the permission record in place."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "permission_id": {
                            "type": "string",
                            "description": "The permission ID to update (required).",
                        },
                        "operation": {
                            "type": "string",
                            "description": "The new operation type for the permission (required). Valid values: 'view', 'edit', 'create', 'admin', 'restrict_other_users'. Accepts 'admin' as alias for 'administer'.",
                        },
                        "granted_by": {
                            "type": "string",
                            "description": "The user ID who granted the permission (optional, updates granted_by and granted_at if provided). User must have status 'active'.",
                        },
                    },
                    "required": ["permission_id", "operation"],
                },
            },
        }
