import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeleteDatabase(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        database_id: str,
        updated_by: str,
    ) -> str:
        """
        Deletes a database record by setting its status to 'deleted'.
        """
        timestamp = "2025-11-13T12:00:00"
        databases = data.get("databases", {})
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
                    "error": f"User with ID '{updated_by}' has status '{users[updated_by]['status']}'. Only active users can delete databases"
                }
            )

        database_to_delete = databases[database_id]

        # Mark as deleted
        database_to_delete["status"] = "deleted"
        database_to_delete["updated_by"] = updated_by
        database_to_delete["updated_at"] = timestamp

        return json.dumps(database_to_delete)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_database",
                "description": "Deletes a database record by setting its status to 'deleted'. This is a soft delete operation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "database_id": {
                            "type": "string",
                            "description": "ID of the database to delete (required)",
                        },
                        "updated_by": {
                            "type": "string",
                            "description": "User ID of the person deleting the database (required)",
                        },
                    },
                    "required": ["database_id", "updated_by"],
                },
            },
        }
