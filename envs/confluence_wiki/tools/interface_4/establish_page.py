import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class EstablishPage(Tool):
    """
    Create a new page in the system.
    - Requires space_id, title, and created_by.
    - Optionally accepts parent_page_id, body_storage, and status.
    - Validates that space and user exist.
    - Validates that parent_page_id exists if provided.
    - Auto-generates page_id, created_at, updated_at, and updated_by.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        space_id: str,
        title: str,
        created_by: str,
        parent_page_id: Optional[str] = None,
        body_storage: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "page": {...}} on success
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

        pages_dict = data.get("pages", {})
        if not isinstance(pages_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid pages container: expected dict at data['pages']",
                }
            )

        spaces_dict = data.get("spaces", {})
        if not isinstance(spaces_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid spaces container: expected dict at data['spaces']",
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
        if space_id is None:
            return json.dumps({"success": False, "error": "space_id is required"})

        if not title or not title.strip():
            return json.dumps(
                {"success": False, "error": "title is required and cannot be empty"}
            )

        if created_by is None:
            return json.dumps({"success": False, "error": "created_by is required"})

        # Convert IDs to strings for consistent comparison
        space_id_str = str(space_id)
        created_by_str = str(created_by)

        # Validate space exists
        if space_id_str not in spaces_dict:
            return json.dumps(
                {"success": False, "error": f"Space with ID '{space_id_str}' not found"}
            )

        # Validate user exists
        if created_by_str not in users_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"User with ID '{created_by_str}' not found",
                }
            )

        # Validate status enum if provided
        # Pages cannot be created with 'deleted' or 'locked' status
        valid_statuses = ["current", "draft", "archived"]
        if status is not None:
            if status in ["deleted", "locked"]:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid status value: '{status}'. Pages cannot be created with 'deleted' or 'locked' status.",
                    }
                )
            if status not in valid_statuses:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid status value: '{status}'. Must be one of {valid_statuses}",
                    }
                )
        # Validate parent_page_id if provided
        if parent_page_id is not None:
            parent_page_id_str = str(parent_page_id)
            if parent_page_id_str not in pages_dict:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Parent page with ID '{parent_page_id_str}' not found",
                    }
                )

            # Validate that parent page is in the same space
            parent_page = pages_dict[parent_page_id_str]
            if isinstance(parent_page, dict):
                parent_space_id = parent_page.get("space_id")
                if parent_space_id != space_id_str:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Parent page '{parent_page_id_str}' is in space '{parent_space_id}', but new page is in space '{space_id_str}'. Parent and child must be in the same space.",
                        }
                    )

        # Generate new page ID
        def generate_page_id(pages: Dict[str, Any]) -> str:
            if not pages:
                return "1"
            try:
                max_id = max(int(k) for k in pages.keys() if k.isdigit())
                return str(max_id + 1)
            except ValueError:
                # If no numeric keys, start from 1
                return "1"

        new_page_id = generate_page_id(pages_dict)

        # Generate timestamp
        current_time = "2025-11-12T12:00:00"
        # Create new page
        new_page = {
            "page_id": new_page_id,
            "title": title.strip(),
            "space_id": space_id_str,
            "parent_page_id": (
                str(parent_page_id) if parent_page_id is not None else None
            ),
            "body_storage": body_storage if body_storage is not None else "",
            "status": status if status is not None else "current",
            "created_by": created_by_str,
            "created_at": current_time,
            "updated_by": created_by_str,
            "updated_at": current_time,
        }

        # Add page to data (modify in place)
        pages_dict[new_page_id] = new_page

        return json.dumps({"success": True, "page": new_page})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "establish_page",
                "description": (
                    "Create a new page in the system. "
                    "Requires space_id, title, and created_by. "
                    "Optionally accepts parent_page_id, body_storage, and status. "
                    "Validates that space and user exist, and that parent_page_id exists if provided. "
                    "Auto-generates page_id, created_at, updated_at, and updated_by."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "The space ID where the page will be created (required).",
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the page (required, cannot be empty).",
                        },
                        "created_by": {
                            "type": "string",
                            "description": "The user ID of the creator (required).",
                        },
                        "parent_page_id": {
                            "type": "string",
                            "description": "The parent page ID if this is a child page (optional). Parent and child must be in the same space.",
                        },
                        "body_storage": {
                            "type": "string",
                            "description": "The body content of the page (optional, defaults to empty string).",
                        },
                        "status": {
                            "type": "string",
                            "description": "The status of the page (optional, defaults to 'current'). Valid values: 'current', 'draft', 'archived'.",
                        },
                    },
                    "required": ["space_id", "title", "created_by"],
                },
            },
        }
