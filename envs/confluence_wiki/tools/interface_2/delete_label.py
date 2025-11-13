import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeleteLabel(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_label_id: str,
    ) -> str:
        """
        Removes a page label record by deleting it from the system.

        Args:
            data: Environment data containing page_labels
            page_label_id: ID of the page label to remove

        Returns:
            JSON string with the removed label data or error message
        """
        page_labels = data.get("page_labels", {})

        # Validate required parameter
        if not page_label_id:
            return json.dumps(
                {"error": "Missing required parameter: page_label_id is required"}
            )

        # Check if page label exists
        if page_label_id not in page_labels:
            return json.dumps(
                {"error": f"Page label with ID '{page_label_id}' not found"}
            )

        # Get the label before removing it
        removed_label = page_labels[page_label_id].copy()

        # Remove the page label
        del page_labels[page_label_id]

        return json.dumps(removed_label)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_label",
                "description": "Removes a page label record by deleting it from the system. This is a permanent delete operation that removes the label-page association.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_label_id": {
                            "type": "string",
                            "description": "ID of the page label to remove (required)",
                        }
                    },
                    "required": ["page_label_id"],
                },
            },
        }
