import json
from typing import Any, Dict, Literal, Optional
from tau_bench.envs.tool import Tool


class RemoveSmartLink(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], smart_link_id: str, url: Optional[str] = None
    ) -> str:
        """
        Deletes a smart link from the sample data.

        Args:
            data (Dict[str, Any]): The data containing smart links.
            smart_link_id (Optional[str]): The ID of the smart link to delete.
            url (Optional[str]): The URL of the smart link to delete.
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

        smart_links_dict = data.get("smart_links", {})

        # Logical Correction: Check for ID in smart_links_dict, not data
        if smart_link_id and smart_link_id in smart_links_dict:

            # Verify the smart link matches the URL if provided
            target_link = smart_links_dict[smart_link_id]
            if url and target_link.get("url") != url:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Smart link ID '{smart_link_id}' does not match the provided URL",
                    }
                )
            try:
                # Delete the smart link
                del smart_links_dict[smart_link_id]

                # Update the original data dictionary
                data["smart_links"] = smart_links_dict

                return json.dumps({"success": True, "smart_links": smart_links_dict})

            except (KeyError, TypeError):
                # This should not be hit if the prior 'in' check worked
                pass

        # Return failure if ID is missing or not found
        return json.dumps(
            {
                "success": False,
                "error": f"Smart link with ID '{smart_link_id}' not found",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_smart_link",
                "description": "Delete a smart link from the Wiki system by its ID and URL if provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "smart_link_id": {
                            "type": "string",
                            "description": "The unique identifier of the smart link to be deleted.",
                        },
                        "url": {
                            "type": "string",
                            "description": "The URL of the smart link to be deleted (optional).",
                        },
                    },
                    "required": ["smart_link_id"],
                },
            },
        }
