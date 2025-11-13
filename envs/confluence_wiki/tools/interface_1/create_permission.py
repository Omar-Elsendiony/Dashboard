import json
from typing import Any, Dict, Optional
from datetime import datetime
import uuid
from tau_bench.envs.tool import Tool


class CreatePermission(Tool):
    """
    Create permission entry for a user on a page or space.
    - Used in Create Page SOP (Step 5) to make page creator the page admin.
    - Grants specific operations (view, edit, delete, create, admin, restrict_other_users) to users.
    - Validates that content (page/space) and user exist and are active.
    - Prevents duplicate permission entries.
    - Only allows permissions on active content (status='current').
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        content_id: str,
        content_type: str,
        user_id: str,
        operation: str,
        granted_by: str,
    ) -> str:
        """
        Create a permission entry for a user on a page or space.

        Args:
            data: The complete database state
            content_id: The ID of the page or space
            content_type: Type of content ('page' or 'space')
            user_id: User ID being granted the permission
            operation: The operation being granted (view, edit, delete, create, admin, restrict_other_users)
            granted_by: User ID granting the permission

        Returns:
            JSON string with success message and permission details or error details
        """

        try:

            def generate_id(permissions: Dict[str, Any]) -> str:
                """Generates a new unique ID for a record."""
                if not permissions:
                    return "1"
                return str(max(int(k) for k in permissions.keys()) + 1)

            # Get dictionaries
            permissions_dict = data.get("permissions", {})
            users_dict = data.get("users", {})
            pages_dict = data.get("pages", {})
            spaces_dict = data.get("spaces", {})

            # Validate input data is a dictionary
            if not isinstance(data, dict):
                return json.dumps(
                    {
                        "success": False,
                        "error": "Invalid data format: 'data' must be a dict",
                    }
                )

            # Validate permissions_dict is a dictionary
            if not isinstance(permissions_dict, dict):
                return json.dumps(
                    {
                        "success": False,
                        "error": "Invalid permissions container: expected dict",
                    }
                )

            # Valid operation types
            valid_operations = [
                "view",
                "edit",
                "delete",
                "create",
                "admin",
                "restrict_other_users",
            ]
            valid_content_types = ["space", "page"]

            # Validate content_type enum
            if content_type not in valid_content_types:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid content_type '{content_type}'. Must be one of: {valid_content_types}",
                    }
                )

            # Validate operation enum
            if operation not in valid_operations:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid operation '{operation}'. Must be one of: {valid_operations}",
                    }
                )

            # Validate content exists and is active
            content_id_str = str(content_id)
            if content_type == "page":
                if content_id_str not in pages_dict:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Page not found: content_id '{content_id}' does not exist",
                        }
                    )
                page = pages_dict[content_id_str]
                content_title = page.get("title", "Unknown")
                page_status = page.get("status")

                # Validate page is active (current status)
                if page_status != "current":
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Cannot grant permission on inactive page: page '{content_id}' has status '{page_status}'. Only pages with status 'current' can receive new permissions.",
                        }
                    )

            elif content_type == "space":
                if content_id_str not in spaces_dict:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Space not found: content_id '{content_id}' does not exist",
                        }
                    )
                space = spaces_dict[content_id_str]
                content_title = space.get("name", "Unknown")
                space_status = space.get("status")

                # Validate space is active (current status)
                if space_status != "current":
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Cannot grant permission on inactive space: space '{content_id}' has status '{space_status}'. Only spaces with status 'current' can receive new permissions.",
                        }
                    )

            # Validate user exists and is active
            user_id_str = str(user_id)
            if user_id_str not in users_dict:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"User not found: user_id '{user_id}' does not exist",
                    }
                )

            user = users_dict[user_id_str]
            user_status = user.get("status")

            # Validate user is active
            if user_status != "active":
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Cannot grant permission to inactive user: user '{user_id}' has status '{user_status}'. Only active users can receive permissions.",
                    }
                )

            # Validate granted_by user exists and is active
            granted_by_str = str(granted_by)
            if granted_by_str not in users_dict:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"User not found: granted_by '{granted_by}' does not exist",
                    }
                )

            granting_user = users_dict[granted_by_str]
            granting_user_status = granting_user.get("status")

            # Validate granting user is active
            if granting_user_status != "active":
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Cannot grant permission by inactive user: user '{granted_by}' has status '{granting_user_status}'. Only active users can grant permissions.",
                    }
                )

            # Check for duplicate permission
            duplicate = any(
                p.get("content_id") == content_id_str
                and p.get("content_type") == content_type
                and p.get("user_id") == user_id_str
                and p.get("operation") == operation
                for p in permissions_dict.values()
                if isinstance(p, dict)
            )

            if duplicate:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Permission already exists: user '{user_id}' already has '{operation}' permission on {content_type} '{content_id}'",
                    }
                )

            # Generate unique permission ID
            permission_id = generate_id(permissions_dict)

            # Create timestamp
            current_time = "2025-11-13T12:00:00"

            # Create new permission entry
            new_permission = {
                "permission_id": permission_id,
                "content_id": content_id_str,
                "content_type": content_type,
                "user_id": user_id_str,
                "operation": operation,
                "granted_by": granted_by_str,
                "granted_at": current_time,
            }

            # Add to permissions dictionary
            permissions_dict[permission_id] = new_permission

            return json.dumps(
                {
                    "success": True,
                    "message": f"Permission '{operation}' granted to user '{user_id}' on {content_type} '{content_title}'",
                    "permission": {
                        "permission_id": permission_id,
                        "content_id": content_id_str,
                        "content_type": content_type,
                        "user_id": user_id_str,
                        "operation": operation,
                        "granted_by": granted_by_str,
                        "granted_at": current_time,
                    },
                }
            )

        except Exception as e:
            return json.dumps(
                {"success": False, "error": f"Failed to create permission: {str(e)}"}
            )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the tool specification for create_permission.

        Returns:
            Dictionary containing the tool's metadata and parameter schema
        """
        return {
            "type": "function",
            "function": {
                "name": "create_permission",
                "description": (
                    "Creates a permission entry that grants a specific operation to a user on a page or space. "
                    "Permissions control what actions users can perform on wiki content. "
                    "Common use cases:"
                    "- Grant 'admin' permission to page creators for full control over their pages"
                    "- Give specific users 'edit' access to collaborate on pages"
                    "- Provide 'view' access to users who should only read content"
                    "- Delegate permission management by granting 'restrict_other_users'"
                    "Validation and safety:"
                    "- Validates that the content (page or space) exists and has status 'current' (active)"
                    "- Validates that the user receiving the permission exists and has status 'active'"
                    "- Validates that the user granting the permission exists and has status 'active'"
                    "- Prevents duplicate permission entries (same user, content, and operation)"
                    "- Only allows permissions on active content (pages with status='current', spaces with status='current')\n"
                    "- Only allows permissions to/from active users (status='active')"
                    "\n"
                    "Automatically records 'granted_by' and 'granted_at' metadata for audit tracking."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content_id": {
                            "type": "string",
                            "description": "The unique identifier of the page or space to grant permission on. The content must have status 'current'. Required field.",
                        },
                        "content_type": {
                            "type": "string",
                            "description": "The type of content ('page', 'space') being granted permission on. 'page' = individual wiki page, 'space' = collection of pages. Required field.",
                        },
                        "user_id": {
                            "type": "string",
                            "description": "The unique identifier of the user being granted the permission. The user must have status 'active'. Required field.",
                        },
                        "operation": {
                            "type": "string",
                            "description": (
                                "The operation being granted to the user. Required field. Operations:"
                                "- 'view': Read access to view content"
                                "- 'edit': Modify and update content"
                                "- 'delete': Remove or soft-delete content"
                                "- 'create': Create new child pages under the content"
                                "- 'admin': Full control including managing permissions and settings"
                                "- 'restrict_other_users': Ability to modify permissions for other users"
                            ),
                        },
                        "granted_by": {
                            "type": "string",
                            "description": "The unique identifier of the user granting this permission. The user must have status 'active'. Typically the content creator, administrator, or another user with 'admin' or 'restrict_other_users' permission. Required field for audit tracking.",
                        },
                    },
                    "required": [
                        "content_id",
                        "content_type",
                        "user_id",
                        "operation",
                        "granted_by",
                    ],
                },
            },
        }
