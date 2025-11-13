import json
from typing import Any, Dict, Literal, Optional
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool


class EditSmartLink(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        smart_link_id: str,
        payload: Dict[str, Any],
    ) -> str:
        """
        Updates a smart link entry on the data.
        """

        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid data format: 'data' must be a dict",
                }
            )

        smart_links_dict = data.get("smart_links", {})
        users_dict = data.get("users", {})
        host_pages_dict = data.get("pages", {})

        # Validate that the updating user exists
        if not payload.get("updated_by") or payload.get("updated_by") not in users_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid User ID '{payload.get('updated_by', '')}'",
                }
            )

        # Validate host_page_id if provided in payload
        if (
            payload.get("host_page_id")
            and payload.get("host_page_id") not in host_pages_dict
        ):
            return json.dumps(
                {
                    "success": False,
                    "error": f"Host page with ID '{payload.get('host_page_id')}' does not exist",
                }
            )

        if smart_link_id and smart_link_id in smart_links_dict:

            if payload:
                # Verify that the payload matches the expected structure
                fields = {
                    "title",
                    "url",
                    "host_page_id",
                    "target_type",
                    "target_id",
                    "updated_by",
                }
                target_enum = {"page", "database", "whiteboard", "external"}

                if "target_type" in payload:
                    if payload["target_type"] not in target_enum:
                        return json.dumps(
                            {
                                "success": False,
                                "error": f"Invalid target_type value '{payload['target_type']}'. Allowed values are {target_enum}",
                            }
                        )
                    elif "target_id" not in payload:
                        return json.dumps(
                            {
                                "success": False,
                                "error": f"Field 'target_id' is required when updating 'target_type'",
                            }
                        )
                    else:
                        # Check if the target ID exists in the corresponding entity list
                        target_type = payload["target_type"]
                        target_id = payload["target_id"]

                        if target_type != "external":
                            target_dict = data.get(target_type + "s", {})
                            if target_id not in target_dict:
                                return json.dumps(
                                    {
                                        "success": False,
                                        "error": f"{target_type}_id '{target_id}' does not exist in {target_type}s",
                                    }
                                )

                for key in payload:
                    if key not in fields:
                        return json.dumps(
                            {
                                "success": False,
                                "error": f"Invalid field '{key}' in payload for updating smart link",
                            }
                        )

                    elif isinstance(payload[key], str) and not payload[key].strip():
                        return json.dumps(
                            {
                                "success": False,
                                "error": f"Field '{key}' cannot be empty",
                            }
                        )

                # Apply update and set timestamp
                smart_links_dict[smart_link_id].update(payload)
                smart_links_dict[smart_link_id]["updated_at"] = "2025-11-13T12:00:00"

                return json.dumps(
                    {
                        "success": True,
                        "smart_link_id": smart_link_id,
                        "data": smart_links_dict[smart_link_id],
                    }
                )
            else:
                return json.dumps(
                    {
                        "success": False,
                        "error": "Payload is required for updating smart link",
                    }
                )
        return json.dumps(
            {
                "success": False,
                "error": f"Smart link with ID '{smart_link_id}' not found",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        # get_info method (unchanged)
        return {
            "type": "function",
            "function": {
                "name": "edit_smart_link",
                "description": "Update a smart link on the Wiki system by its ID and URL if provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "smart_link_id": {
                            "type": "string",
                            "description": "The unique identifier of the smart link to be updated.",
                        },
                        "payload": {
                            "type": "object",
                            "description": "The fields to update in the smart link entry.",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "The title of the smart link.",
                                },
                                "url": {
                                    "type": "string",
                                    "description": "The URL of the smart link.",
                                },
                                "host_page_id": {
                                    "type": "string",
                                    "description": "The ID of the host page where the smart link is located.",
                                },
                                "target_type": {
                                    "type": "string",
                                    "description": (
                                        "The type of the target linked by the smart link. Enum = ['page','database','whiteboard','external',]"
                                    ),
                                },
                                "target_id": {
                                    "type": "string",
                                    "description": "The ID of the target linked by the smart link.",
                                },
                                "updated_by": {
                                    "type": "string",
                                    "description": "User ID of the person updating the smart link.",
                                },
                            },
                        },
                    },
                    "required": ["smart_link_id", "payload"],
                },
            },
        }
