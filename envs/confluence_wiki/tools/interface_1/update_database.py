import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateDatabase(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        database_id: str,
        updated_by: str,
        title: Optional[str] = None,
        host_space_id: Optional[str] = None,
        host_page_id: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Updates an existing database record.
        """
        timestamp = "2025-11-13T12:00:00"
        databases = data.get("databases", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        users = data.get("users", {})

        # Validate required parameters
        if not database_id or not updated_by:
            return json.dumps(
                {
                    "error": "Missing required parameters: database_id and updated_by are required"
                }
            )

        # Check if database exists
        if database_id not in databases:
            return json.dumps({"error": f"Database with ID '{database_id}' not found"})

        # Validate updated_by user exists
        if updated_by not in users:
            return json.dumps({"error": f"User with ID '{updated_by}' not found"})

        if users[updated_by]["status"] != "active":
            return json.dumps(
                {
                    "error": f"User with ID '{updated_by}' has status '{users[updated_by]['status']}'. Only active users can update databases"
                }
            )

        # At least one optional field must be provided
        if not any([title, host_space_id, host_page_id, description, status]):
            return json.dumps(
                {"error": "At least one field to update must be provided"}
            )

        database_to_update = databases[database_id]

        # Validate host changes if provided
        if host_space_id is not None or host_page_id is not None:
            # If both are being set, ensure mutual exclusivity
            effective_space_id = (
                host_space_id
                if host_space_id is not None
                else database_to_update.get("host_space_id")
            )
            effective_page_id = (
                host_page_id
                if host_page_id is not None
                else database_to_update.get("host_page_id")
            )

            if effective_space_id and effective_page_id:
                return json.dumps(
                    {
                        "error": "Only one of host_space_id or host_page_id can be set (mutually exclusive)"
                    }
                )

        # Validate host_space_id exists if provided
        if host_space_id and host_space_id not in spaces:
            return json.dumps({"error": f"Space with ID '{host_space_id}' not found"})

        if host_space_id and spaces[host_space_id]["status"] != "current":
            return json.dumps(
                {
                    "error": f"Cannot move database to space with status '{spaces[host_space_id]['status']}'. Space must have status 'current'"
                }
            )

        # Validate host_page_id exists if provided
        if host_page_id and host_page_id not in pages:
            return json.dumps({"error": f"Page with ID '{host_page_id}' not found"})

        if host_page_id and pages[host_page_id]["status"] != "current":
            return json.dumps(
                {
                    "error": f"Cannot move database to page with status '{pages[host_page_id]['status']}'. Page must have status 'current'"
                }
            )

        # Validate status if provided
        valid_statuses = ["current", "archived", "deleted"]
        if status and status not in valid_statuses:
            return json.dumps(
                {
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                }
            )

        # Update fields if provided
        if title:
            database_to_update["title"] = title
        if host_space_id is not None:
            database_to_update["host_space_id"] = host_space_id
            database_to_update["host_page_id"] = None
        if host_page_id is not None:
            database_to_update["host_page_id"] = host_page_id
            database_to_update["host_space_id"] = None
        if description is not None:
            database_to_update["description"] = description
        if status:
            database_to_update["status"] = status

        database_to_update["updated_by"] = updated_by
        database_to_update["updated_at"] = timestamp

        return json.dumps(database_to_update)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_database",
                "description": "Updates an existing database record. At least one optional field must be provided for update. Either host_space_id OR host_page_id can be set (mutually exclusive).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "database_id": {
                            "type": "string",
                            "description": "ID of the database to update (required)",
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the database (optional)",
                        },
                        "host_space_id": {
                            "type": "string",
                            "description": "New space ID hosting this database (optional, mutually exclusive with host_page_id)",
                        },
                        "host_page_id": {
                            "type": "string",
                            "description": "New page ID hosting this database (optional, mutually exclusive with host_space_id)",
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the database (optional)",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status: 'current', 'archived', or 'deleted' (optional)",
                        },
                        "updated_by": {
                            "type": "string",
                            "description": "User ID of the updater (required)",
                        },
                    },
                    "required": ["database_id", "updated_by"],
                },
            },
        }
