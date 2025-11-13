import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GenerateLabel(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
        label_name: str,
        added_by: str,
    ) -> str:
        """
        Creates a new page label record.
        """

        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-11-13T12:00:00"
        page_labels = data.get("page_labels", {})
        pages = data.get("pages", {})
        users = data.get("users", {})

        # Validate required parameters
        if not all([page_id, label_name, added_by]):
            return json.dumps(
                {
                    "error": "Missing required parameters: page_id, label_name, and added_by are required"
                }
            )

        # Validate page exists
        if page_id not in pages:
            return json.dumps({"error": f"Page with ID '{page_id}' not found"})

        # Validate added_by user exists
        if added_by not in users:
            return json.dumps({"error": f"User with ID '{added_by}' not found"})

        # Check for duplicate label on the same page
        for existing_label in page_labels.values():
            if (
                existing_label.get("page_id") == page_id
                and existing_label.get("label_name") == label_name
            ):
                return json.dumps(
                    {
                        "error": f"Label '{label_name}' already exists on page '{page_id}'"
                    }
                )

        # Generate new page label ID
        new_label_id = generate_id(page_labels)

        # Create new page label record
        new_label = {
            "page_label_id": new_label_id,
            "page_id": page_id,
            "label_name": label_name,
            "added_by": added_by,
            "added_at": timestamp,
        }

        page_labels[new_label_id] = new_label

        return json.dumps(new_label)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_label",
                "description": "Creates a new label for a page. Labels are stored directly with the label name and cannot be duplicated on the same page.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "ID of the page to add the label to (required)",
                        },
                        "label_name": {
                            "type": "string",
                            "description": "Name of the label (required)",
                        },
                        "added_by": {
                            "type": "string",
                            "description": "User ID of the person adding the label (required)",
                        },
                    },
                    "required": ["page_id", "label_name", "added_by"],
                },
            },
        }
