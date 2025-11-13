import json
from typing import Any, Dict, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool


class GenerateWhiteboard(Tool):
    """
    Create a new whiteboard in a space or page.
    - Used in Create Whiteboard SOP.
    - Requires either host_space_id OR host_page_id (mutually exclusive).
    - Validates that host space/page exists and has status 'current'.
    - Validates that title is not empty.
    - Sets status to 'current' by default.
    - Automatically sets created_by, updated_by, and timestamps.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        created_by: str,
        host_space_id: Optional[str] = None,
        host_page_id: Optional[str] = None,
    ) -> str:
        """
        Create a new whiteboard.

        Args:
            data: The complete database state
            title: The title of the whiteboard
            created_by: User ID of the creator
            host_space_id: Optional space ID where whiteboard is hosted
            host_page_id: Optional page ID where whiteboard is hosted

        Returns:
            JSON string with success message and whiteboard details or error details
        """
        try:

            def generate_id(whiteboards: Dict[str, Any]) -> str:
                """Generates a new unique ID for a record."""
                if not whiteboards:
                    return "1"
                return str(max(int(k) for k in whiteboards.keys()) + 1)

            # Validate input data is a dictionary
            if not isinstance(data, dict):
                return json.dumps(
                    {
                        "success": False,
                        "error": "Invalid data format: 'data' must be a dict",
                    }
                )

            # Get dictionaries
            whiteboards = data.get("whiteboards", {})
            users_dict = data.get("users", {})
            pages_dict = data.get("pages", {})
            spaces_dict = data.get("spaces", {})

            # Validate whiteboards is a dictionary
            if not isinstance(whiteboards, dict):
                return json.dumps(
                    {
                        "success": False,
                        "error": "Invalid whiteboards container: expected dict",
                    }
                )

            # Validate title is not empty
            if not title or not title.strip():
                return json.dumps(
                    {
                        "success": False,
                        "error": "Title cannot be empty. Please provide a valid whiteboard title.",
                    }
                )

            # Validate that exactly one host is specified
            if not host_space_id and not host_page_id:
                return json.dumps(
                    {
                        "success": False,
                        "error": "Either host_space_id or host_page_id must be provided",
                    }
                )

            if host_space_id and host_page_id:
                return json.dumps(
                    {
                        "success": False,
                        "error": "Cannot specify both host_space_id and host_page_id - they are mutually exclusive",
                    }
                )

            # Validate creator user exists
            created_by_str = str(created_by)
            if created_by_str not in users_dict:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"User not found: created_by '{created_by}' does not exist",
                    }
                )

            # Validate user is active
            user = users_dict[created_by_str]
            user_status = user.get("status")
            if user_status != "active":
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Cannot create whiteboard with inactive user: user '{created_by}' has status '{user_status}'. Only active users can create whiteboards.",
                    }
                )

            # Validate host space or page exists and is active
            host_name = None
            if host_space_id:
                host_space_id_str = str(host_space_id)
                if host_space_id_str not in spaces_dict:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Space not found: host_space_id '{host_space_id}' does not exist",
                        }
                    )

                space = spaces_dict[host_space_id_str]
                space_status = space.get("status")
                host_name = space.get("name", "Unknown")

                # Validate space is active (current status)
                if space_status != "current":
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Cannot create whiteboard in inactive space: space '{host_space_id}' has status '{space_status}'. Only spaces with status 'current' can host whiteboards.",
                        }
                    )

                # Use the validated string version
                host_space_id = host_space_id_str

            if host_page_id:
                host_page_id_str = str(host_page_id)
                if host_page_id_str not in pages_dict:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Page not found: host_page_id '{host_page_id}' does not exist",
                        }
                    )

                page = pages_dict[host_page_id_str]
                page_status = page.get("status")
                host_name = page.get("title", "Unknown")

                # Validate page is active (current status)
                if page_status != "current":
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Cannot create whiteboard on inactive page: page '{host_page_id}' has status '{page_status}'. Only pages with status 'current' can host whiteboards.",
                        }
                    )

                # Use the validated string version
                host_page_id = host_page_id_str

            # Create timestamp
            current_time = "2025-11-13T12:00:00"

            # Generate whiteboard ID
            whiteboard_id = generate_id(whiteboards)

            # Create new whiteboard
            new_whiteboard = {
                "whiteboard_id": whiteboard_id,
                "title": title.strip(),  # Strip whitespace from title
                "host_space_id": host_space_id,
                "host_page_id": host_page_id,
                "content": "",  # Always empty on creation
                "status": "current",
                "created_by": created_by_str,
                "created_at": current_time,
                "updated_by": created_by_str,
                "updated_at": current_time,
            }

            # Add to whiteboards dictionary
            whiteboards[whiteboard_id] = new_whiteboard

            host_type = "space" if host_space_id else "page"
            host_id = host_space_id if host_space_id else host_page_id

            return json.dumps(
                {
                    "success": True,
                    "message": f"Whiteboard '{title.strip()}' created successfully in {host_type} '{host_name}'",
                    "whiteboard": {
                        "whiteboard_id": whiteboard_id,
                        "title": title.strip(),
                        "host_space_id": host_space_id,
                        "host_page_id": host_page_id,
                        "content": "",  # Always empty on creation
                        "status": "current",
                        "created_by": created_by_str,
                        "created_at": current_time,
                        "updated_by": created_by_str,
                        "updated_at": current_time,
                    },
                }
            )

        except Exception as e:
            return json.dumps(
                {"success": False, "error": f"Failed to create whiteboard: {str(e)}"}
            )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the tool specification for generate_whiteboard.

        Returns:
            Dictionary containing the tool's metadata and parameter schema
        """
        return {
            "type": "function",
            "function": {
                "name": "generate_whiteboard",
                "description": (
                    "Creates a new whiteboard for visual collaboration and diagramming. "
                    "Whiteboards are interactive canvases that can be attached to either a space or a specific page. "
                    "Hosting location (must choose one):"
                    "- Space-level whiteboard: Provide 'host_space_id' to create a whiteboard accessible throughout the space"
                    "- Page-level whiteboard: Provide 'host_page_id' to create a whiteboard embedded in a specific page"
                    "IMPORTANT: You must provide either 'host_space_id' OR 'host_page_id', but not both. These are mutually exclusive."
                    "Validation and safety:"
                    "- Validates that the host space or page exists in the system"
                    "- Validates that the host space/page has status 'current' (active)"
                    "- Validates that the creator user exists and has status 'active'"
                    "- Validates that the title is not empty or whitespace-only"
                    "- Only allows whiteboards on active content (spaces/pages with status='current')"
                    "Automatically sets:"
                    "- Status to 'current' (active/published)"
                    "- 'created_at' and 'updated_at' timestamps"
                    "- 'created_by' and 'updated_by' to the creator's user ID"
                    "- Content to empty string (whiteboards start blank)"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title/name of the whiteboard. Cannot be empty or whitespace-only. Required field.",
                        },
                        "created_by": {
                            "type": "string",
                            "description": "The unique identifier of the user creating the whiteboard. User must have status 'active'. Required field for audit tracking.",
                        },
                        "host_space_id": {
                            "type": "string",
                            "description": "The unique identifier of the space to host the whiteboard. Space must exist and have status 'current'. Use this to create a space-level whiteboard. Mutually exclusive with 'host_page_id' - provide only one.",
                        },
                        "host_page_id": {
                            "type": "string",
                            "description": "The unique identifier of the page to host the whiteboard. Page must exist and have status 'current'. Use this to create a page-level whiteboard embedded in a specific page. Mutually exclusive with 'host_space_id' - provide only one.",
                        },
                    },
                    "required": ["title", "created_by"],
                },
            },
        }
