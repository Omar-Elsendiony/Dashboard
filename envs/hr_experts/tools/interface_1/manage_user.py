import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageUser(Tool):
    """
    Manages user accounts including creation and updates for provisioning and employee lifecycle.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        user_id: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        phone_number: Optional[str] = None,
        status: Optional[str] = None,
        mfa_enabled: Optional[bool] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on user accounts.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        users = data.get("users", {})

        # Validate supported roles
        supported_roles = [
            "hr_director", "hr_manager", "recruiter", "payroll_administrator",
            "hiring_manager", "finance_officer", "it_administrator", 
            "compliance_officer", "employee"
        ]

        # Validate supported statuses
        supported_statuses = ["active", "inactive"]

        if action == "create":
            # Required fields for user creation
            if not all([first_name, last_name, email, role]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: first_name, last_name, email, role"
                })

            # Validate role
            if role not in supported_roles:
                return json.dumps({
                    "error": f"Invalid role '{role}'. Must be one of: {', '.join(supported_roles)}"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate email
            for existing_user in users.values():
                if existing_user.get("email") == email:
                    return json.dumps({
                        "error": f"User with email '{email}' already exists"
                    })

            # Generate new user ID
            new_user_id = generate_id(users)

            # Create new user record
            new_user = {
                "user_id": new_user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "role": role,
                "status": status or "active",  # Default to active if not specified
                "mfa_enabled": mfa_enabled if mfa_enabled is not None else False,  # Default to False
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add phone_number if provided
            if phone_number:
                new_user["phone_number"] = phone_number

            # Add to users data
            users[new_user_id] = new_user

            return json.dumps({
                "success": True,
                "message": f"User created successfully with ID {new_user_id}",
                "user_id": new_user_id,
                "user_data": new_user
            })

        elif action == "update":
            # user_id is required for update
            if not user_id:
                return json.dumps({
                    "error": "Missing required parameter 'user_id' for update operation"
                })

            # Check if user exists
            if user_id not in users:
                return json.dumps({
                    "error": f"User with ID {user_id} not found"
                })

            user_to_update = users[user_id]

            # Validate role if being updated
            if role and role not in supported_roles:
                return json.dumps({
                    "error": f"Invalid role '{role}'. Must be one of: {', '.join(supported_roles)}"
                })

            # Validate status if being updated
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate email if email is being changed
            if email and email != user_to_update.get("email"):
                for existing_user in users.values():
                    if existing_user.get("email") == email:
                        return json.dumps({
                            "error": f"User with email '{email}' already exists"
                        })

            # Track what fields are being updated
            updated_fields = []

            # Update fields if provided
            if first_name:
                user_to_update["first_name"] = first_name
                updated_fields.append("first_name")
            
            if last_name:
                user_to_update["last_name"] = last_name
                updated_fields.append("last_name")
            
            if email:
                user_to_update["email"] = email
                updated_fields.append("email")
            
            if role:
                user_to_update["role"] = role
                updated_fields.append("role")
            
            if phone_number:
                user_to_update["phone_number"] = phone_number
                updated_fields.append("phone_number")
            
            if status:
                user_to_update["status"] = status
                updated_fields.append("status")
            
            if mfa_enabled is not None:
                user_to_update["mfa_enabled"] = mfa_enabled
                updated_fields.append("mfa_enabled")

            # Update timestamp
            user_to_update["updated_at"] = timestamp

            if not updated_fields:
                return json.dumps({
                    "error": "No fields provided to update"
                })

            return json.dumps({
                "success": True,
                "message": f"User {user_id} updated successfully",
                "updated_fields": updated_fields,
                "user_data": user_to_update
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_user",
                "description": "Manages user accounts for provisioning and employee lifecycle operations. Supports creating new user accounts with proper role validation and updating existing accounts for status changes during onboarding/offboarding. For user provisioning, validates required fields (first_name, last_name, email, role) and optional fields (phone_number, status, mfa_enabled). For employee onboarding/offboarding, updates user status to 'active' or 'inactive'. Supported roles: hr_director, hr_manager, recruiter, payroll_administrator, hiring_manager, finance_officer, it_administrator, compliance_officer, employee. Supported statuses: active, inactive. Prevents duplicate email addresses and validates all role assignments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform: 'create' for user provisioning, 'update' for profile updates/status changes",
                            "enum": ["create", "update"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID (required for update operations)"
                        },
                        "first_name": {
                            "type": "string",
                            "description": "User's first name (required for create)"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "User's last name (required for create)"
                        },
                        "email": {
                            "type": "string",
                            "description": "User's email address (required for create, must be unique)"
                        },
                        "role": {
                            "type": "string",
                            "description": "User's system role (required for create)",
                            "enum": ["hr_director", "hr_manager", "recruiter", "payroll_administrator", "hiring_manager", "finance_officer", "it_administrator", "compliance_officer", "employee"]
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "User's phone number (optional)"
                        },
                        "status": {
                            "type": "string",
                            "description": "User account status (optional, defaults to 'active' for new users)",
                            "enum": ["active", "inactive"]
                        },
                        "mfa_enabled": {
                            "type": "boolean",
                            "description": "Whether multi-factor authentication is enabled (optional, defaults to false)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }