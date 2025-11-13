import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GenerateDatabase(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        created_by: str,
        description: Optional[str] = None,
        host_space_id: Optional[str] = None,
        host_page_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Creates a new database record.
        """

        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-11-13T12:00:00"
        databases = data.get("databases", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        users = data.get("users", {})

        # Validate required parameters
        if not title or not created_by:
            return json.dumps(
                {
                    "error": "Missing required parameters: title and created_by are required"
                }
            )

        # Validate that either host_space_id OR host_page_id is set (mutually exclusive)
        if not host_space_id and not host_page_id:
            return json.dumps(
                {"error": "Either host_space_id or host_page_id must be provided"}
            )

        if host_space_id and host_page_id:
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
                    "error": f"Cannot create database in space with status '{spaces[host_space_id]['status']}'. Space must have status 'current'"
                }
            )

        # Validate host_page_id exists if provided
        if host_page_id and host_page_id not in pages:
            return json.dumps({"error": f"Page with ID '{host_page_id}' not found"})

        if host_page_id and pages[host_page_id]["status"] != "current":
            return json.dumps(
                {
                    "error": f"Cannot create database in page with status '{pages[host_page_id]['status']}'. Page must have status 'current'"
                }
            )

        # Validate created_by user exists
        if created_by not in users:
            return json.dumps({"error": f"User with ID '{created_by}' not found"})

        if users[created_by]["status"] != "active":
            return json.dumps(
                {
                    "error": f"User with ID '{created_by}' has status '{users[created_by]['status']}'. Only active users can create databases"
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

        # Generate new database ID
        new_database_id = generate_id(databases)

        # Create new database record
        new_database = {
            "database_id": new_database_id,
            "title": title,
            "host_space_id": host_space_id,
            "host_page_id": host_page_id,
            "description": description,
            "status": status if status else "current",
            "created_by": created_by,
            "created_at": timestamp,
            "updated_by": created_by,
            "updated_at": timestamp,
        }

        databases[new_database_id] = new_database

        return json.dumps(new_database)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_database",
                "description": "Creates a new database record. Either host_space_id OR host_page_id must be provided (mutually exclusive). The database can be hosted at space-level or page-level.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the database (required)",
                        },
                        "host_space_id": {
                            "type": "string",
                            "description": "ID of the space hosting this database (mutually exclusive with host_page_id)",
                        },
                        "host_page_id": {
                            "type": "string",
                            "description": "ID of the page hosting this database (mutually exclusive with host_space_id)",
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the database (optional)",
                        },
                        "status": {
                            "type": "string",
                            "description": "Database status: 'current', 'archived', or 'deleted' (optional, defaults to 'current')",
                        },
                        "created_by": {
                            "type": "string",
                            "description": "User ID of the creator (required)",
                        },
                    },
                    "required": ["title", "created_by"],
                },
            },
        }
