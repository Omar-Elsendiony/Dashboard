import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool


class NewSmartLink(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payload: Dict[str, Any]) -> str:
        """
        creates a smart link entry on the data.
        """

        required_fields = {
            "title",
            "url",
            "host_page_id",
            "target_type",
            "created_by",
        }
        target_enum = {"page", "database", "whiteboard", "external"}

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

        # Validate that the creating user exists
        if not payload.get("created_by") or payload.get("created_by") not in users_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid User ID '{payload.get('created_by', '')}'",
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

        # Check for missing required fields
        missing_fields = required_fields - payload.keys()
        if missing_fields:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Missing required fields: {', '.join(sorted(missing_fields))}",
                }
            )

        # Ensure all required fields contain non-empty values
        for field in required_fields:
            if not payload.get(field, "").strip():
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Field '{field}' cannot be empty",
                    }
                )

        # Validate target_type
        if payload["target_type"] not in target_enum:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid target_type value '{payload['target_type']}'. Allowed values are {target_enum}",
                }
            )

        # Handle target_id based on target_type
        if payload["target_type"] == "external":
            # For external links, target_id can be null or empty
            # target_id = payload.get("target_id", None)
            # if target_id == "":
            target_id = None
        else:
            # For internal links, target_id is required and must exist
            if "target_id" not in payload:
                return json.dumps(
                    {
                        "success": False,
                        "error": "Missing required field: target_id",
                    }
                )
            
            if not payload.get("target_id", "").strip():
                return json.dumps(
                    {
                        "success": False,
                        "error": "Field 'target_id' cannot be empty for non-external links",
                    }
                )
            
            target_id = payload["target_id"]
            target_dict = data.get(payload["target_type"] + "s", {})
            if target_id not in target_dict:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"{payload['target_type']}_id '{target_id}' does not exist in {payload['target_type']}s",
                    }
                )

        # Generate a new smart_link_id
        existing_ids = [int(k) for k in smart_links_dict.keys() if k.isdigit()]
        max_id = max(existing_ids) if existing_ids else 0
        new_id = str(max_id + 1)
        timestamp = "2025-11-13T12:00:00"

        # Create the new smart link entry
        smart_links_dict[new_id] = {
            "smart_link_id": new_id,
            "title": payload["title"],
            "url": payload["url"],
            "host_page_id": payload["host_page_id"],
            "target_type": payload["target_type"],
            "target_id": target_id,
            "created_by": payload["created_by"],
            "updated_by": payload["created_by"],
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        # Update original data dictionary
        data["smart_links"] = smart_links_dict

        return json.dumps(
            {"success": True, "smart_link_id": new_id, "data": smart_links_dict[new_id]}
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        # get_info method (unchanged)
        return {
            "type": "function",
            "function": {
                "name": "new_smart_link",
                "description": (
                    "Creates a smart link on a wiki page that points to an internal entity or an external URL. "
                    "Required: 'title', 'url', 'host_page_id', 'target_type', 'created_by'. "
                    "For internal links (page, database, whiteboard), 'target_id' is also required. "
                    "For external links, 'target_id' should not be provided.\n"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payload": {
                            "type": "object",
                            "description": "The required data to create a new smart link entry.",
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
                                        "The type of the target linked by the smart link. Enum = ['page','database','whiteboard','external']"
                                    ),
                                },
                                "target_id": {
                                    "type": "string",
                                    "description": "The ID of the target linked by the smart link. Required for internal links (page, database, whiteboard), but should not be provided for external links.",
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID of the person creating the smart link.",
                                },
                            },
                            "required": ["title", "url", "host_page_id", "target_type", "created_by"],
                        },
                    },
                    "required": ["payload"],
                },
            },
        }
