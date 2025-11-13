import json
from typing import Any, Dict, Literal, Optional
from tau_bench.envs.tool import Tool


class DeleteWhiteboard(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], whiteboard_id: str) -> str:
        """
        Deletes a whiteboard from the sample data.

        Args:
            data (Dict[str, Any]): The data containing whiteboards.
            whiteboard_id (Optional[str]): The ID of the whiteboard to delete.
        Returns:
            str: A json string indicating the result of the deletion.
        """
        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid data format: 'data' must be a dict",
                }
            )

        whiteboards_dict = data.get("whiteboards", {})
        # Logical correction: Check for ID in whiteboards_dict, not data
        if whiteboard_id and whiteboard_id in whiteboards_dict:
            try:
                # Delete the whiteboard from the dictionary
                del whiteboards_dict[whiteboard_id]

                # Update the original data dictionary
                data["whiteboards"] = whiteboards_dict

                return json.dumps({"success": True, "whiteboards": whiteboards_dict})

            except (KeyError, TypeError):

                pass

        # Return failure if ID is missing or not found
        return json.dumps(
            {
                "success": False,
                "error": f"Whiteboard with ID '{whiteboard_id}' not found",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_whiteboard",
                "description": "Delete a whiteboard from the Wiki system by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "whiteboard_id": {
                            "type": "string",
                            "description": "The unique identifier of the whiteboard to be deleted.",
                        },
                    },
                    "required": ["whiteboard_id"],
                },
            },
        }
