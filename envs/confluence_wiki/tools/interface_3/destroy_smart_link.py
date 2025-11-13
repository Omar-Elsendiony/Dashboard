import json
from typing import Any, Dict, Literal, Optional, List
from tau_bench.envs.tool import Tool


class DestroySmartLink(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], smart_link_ids: List[str]) -> str:
        """
        Deletes a smart link from the sample data.

        Args:
            data (Dict[str, Any]): The data containing smart links.
            smart_link_ids (List[str]): The IDs of the smart links to delete.
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
        successes = {}
        failures = {}

        for smart_link_id in list(set(smart_link_ids)):
            if smart_link_id and smart_link_id in smart_links_dict:
                # Delete the smart link
                del smart_links_dict[smart_link_id]
                successes[smart_link_id] = True
            else:
                failures[smart_link_id] = (
                    f"Smart link with ID '{smart_link_id}' not found"
                )

        result = {
            "success": len(failures) == 0,
            "deleted": list(successes.keys()),
            "failed": failures,
        }
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "destroy_smart_link",
                "description": "Delete a list smart link from the Wiki system by their IDs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "smart_link_ids": {
                            "type": "array",
                            "description": "The list of unique identifiers of the smart links to be deleted.",
                        },
                    },
                    "required": ["smart_link_ids"],
                },
            },
        }
