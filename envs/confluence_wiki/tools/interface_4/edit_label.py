import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class EditLabel(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_label_id: str,
        label_name: str,
    ) -> str:
        """
        Updates an existing page label record.
        """
        timestamp = "2025-11-13T12:00:00"
        page_labels = data.get("page_labels", {})

        # Validate required parameters
        if not page_label_id or not label_name:
            return json.dumps(
                {
                    "error": "Missing required parameters: page_label_id and label_name are required"
                }
            )

        # Check if label exists
        if page_label_id not in page_labels:
            return json.dumps(
                {"error": f"Page label with ID '{page_label_id}' not found"}
            )

        label_to_update = page_labels[page_label_id]
        page_id = label_to_update.get("page_id")

        # Check for duplicate label name on the same page (excluding current label)
        for existing_label_id, existing_label in page_labels.items():
            if (
                existing_label_id != page_label_id
                and existing_label.get("page_id") == page_id
                and existing_label.get("label_name") == label_name
            ):
                return json.dumps(
                    {
                        "error": f"Label '{label_name}' already exists on page '{page_id}'"
                    }
                )

        # Update label name
        label_to_update["label_name"] = label_name
        label_to_update["updated_at"] = timestamp

        return json.dumps(label_to_update)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "edit_label",
                "description": "Updates an existing page label by changing its label name. The new label name must not duplicate an existing label on the same page.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_label_id": {
                            "type": "string",
                            "description": "ID of the page label to update (required)",
                        },
                        "label_name": {
                            "type": "string",
                            "description": "New label name (required)",
                        },
                    },
                    "required": ["page_label_id", "label_name"],
                },
            },
        }
