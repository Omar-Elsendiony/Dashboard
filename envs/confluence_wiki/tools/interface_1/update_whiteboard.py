import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateWhiteboard(Tool):
    """Update an existing whiteboard."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        whiteboard_id: str,
        payload: Dict[str, Any],
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "whiteboard": {...}} on success
          {"success": False, "error": "..."} on error
        """
        color_enum = {
            "red",
            "blue",
            "green",
            "yellow",
            "orange",
            "purple",
            "pink",
            "gray",
            "white",
            "black",
        }
        shape_enum = {"sticky_note", "circle", "rectangle", "oval", "diamond"}
        status_enum = {"current", "archived", "deleted"}

        whiteboards_dict = data.get("whiteboards", {})
        users_dict = data.get("users", {})
        pages_dict = data.get("pages", {})
        spaces_dict = data.get("spaces", {})

        if not payload.get("updated_by"):
            return json.dumps(
                {
                    "success": False,
                    "error": f"updated_by field is required in payload",
                }
            )
        if payload.get("updated_by") not in users_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid User ID '{payload.get('updated_by', '')}'",
                }
            )

        if whiteboard_id not in whiteboards_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Whiteboard with ID '{whiteboard_id}' not found",
                }
            )

        whiteboard = whiteboards_dict[whiteboard_id]
        if whiteboard.get("status") == "deleted":
            return json.dumps(
                {
                    "success": False,
                    "error": "Cannot update a deleted whiteboard",
                }
            )
        if (
            payload.get("host_page_id")
            and payload.get("host_page_id") not in pages_dict
        ):
            return json.dumps(
                {
                    "success": False,
                    "error": f"Host page with ID '{payload.get('host_page_id')}' not found",
                }
            )
        if (
            payload.get("host_space_id")
            and payload.get("host_space_id") not in spaces_dict
        ):
            return json.dumps(
                {
                    "success": False,
                    "error": f"Host space with ID '{payload.get('host_space_id')}' not found",
                }
            )
        status_value = payload.get("status")
        if status_value and status_value not in status_enum:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid status value: '{status_value}'. Must be one of {status_enum}",
                }
            )

        def append_content(existing_content, new_content):
            length_existing = len(existing_content)

            # Validate type if provided
            content_type = new_content.get("type", "sticky_note")
            if content_type not in shape_enum:
                raise ValueError(
                    f"Invalid type value: '{content_type}'. Must be one of {shape_enum}"
                )

            # Validate color if provided
            content_color = new_content.get("color", "yellow")
            if content_color not in color_enum:
                raise ValueError(
                    f"Invalid color value: '{content_color}'. Must be one of {color_enum}"
                )

            # Determine new ID
            new_id = "1"
            if existing_content:
                try:
                    max_id = max(
                        int(item["id"]) for item in existing_content if item.get("id")
                    )
                    new_id = str(max_id + 1)
                except ValueError:
                    new_id = str(length_existing + 1)

            new_content_data = {
                "id": new_id,
                "type": content_type,
                "text": new_content.get("text", ""),
                "x_position": (
                    existing_content[-1].get("x_position", 100) + 120
                    if existing_content
                    and existing_content[-1].get("x_position") is not None
                    else 100
                ),
                "y_position": new_content.get("y_position", 100),
                "width": new_content.get("width", 100),
                "height": new_content.get("height", 100),
                "color": content_color,
            }
            existing_content.append(new_content_data)
            return existing_content

        def replace_content(existing_content, new_content):
            content_id = new_content.get("id")
            if not content_id:
                raise ValueError("Content to replace must have an 'id' field.")

            for idx, item in enumerate(existing_content):
                if item.get("id") == content_id:
                    # Preserve un-updated fields
                    updated_item = existing_content[idx].copy()

                    # Validate type if provided
                    if "type" in new_content:
                        if new_content["type"] not in shape_enum:
                            raise ValueError(
                                f"Invalid type value: '{new_content['type']}'. Must be one of {shape_enum}"
                            )
                        updated_item["type"] = new_content["type"]

                    # Validate color if provided
                    if "color" in new_content:
                        if new_content["color"] not in color_enum:
                            raise ValueError(
                                f"Invalid color value: '{new_content['color']}'. Must be one of {color_enum}"
                            )
                        updated_item["color"] = new_content["color"]

                    # Update text if provided
                    if "text" in new_content:
                        updated_item["text"] = new_content["text"]

                    # Update position/size if provided
                    if "x_position" in new_content:
                        updated_item["x_position"] = new_content["x_position"]
                    if "y_position" in new_content:
                        updated_item["y_position"] = new_content["y_position"]
                    if "width" in new_content:
                        updated_item["width"] = new_content["width"]
                    if "height" in new_content:
                        updated_item["height"] = new_content["height"]

                    existing_content[idx] = updated_item
                    return existing_content

            raise ValueError(f"Content with id '{content_id}' does not exist.")

        def remove_content(existing_content, content_to_remove):
            # Assumes content_to_remove is an object with an "id" key
            if not isinstance(content_to_remove, dict) or "id" not in content_to_remove:
                return existing_content

            updated_content = [
                item
                for item in existing_content
                if item["id"] != content_to_remove["id"]
            ]
            return updated_content

        # --- Basic input validation ---
        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid data format: 'data' must be a dict",
                }
            )

        # --- Update the whiteboard ---
        for key, value in payload.items():
            if key == "content":
                # Validate content is a JSON string
                if not payload.get("content_action"):
                    return json.dumps(
                        {
                            "success": False,
                            "error": "Content update requires 'content_action' field in payload.",
                        }
                    )
                try:
                    content_value = json.loads(value)
                    existing_content = json.loads(whiteboard.get("content", "[]"))

                    if payload.get("content_action") == "append":
                        # Append new content item to existing content
                        updated_content = append_content(
                            existing_content, content_value
                        )
                        whiteboard["content"] = json.dumps(updated_content)
                    elif payload.get("content_action") == "replace":
                        # Replace existing content item with new content
                        try:
                            updated_content = replace_content(
                                existing_content, content_value
                            )
                            whiteboard["content"] = json.dumps(updated_content)
                        except ValueError as ve:
                            return json.dumps(
                                {
                                    "success": False,
                                    "error": str(ve),
                                }
                            )
                    elif payload.get("content_action") == "remove":
                        # Remove specified content items from existing content
                        updated_content = remove_content(
                            existing_content, content_value
                        )
                        whiteboard["content"] = json.dumps(updated_content)
                    else:
                        return json.dumps(
                            {
                                "success": False,
                                "error": f"Invalid content_action: '{payload.get('content_action')}'",
                            }
                        )

                except json.JSONDecodeError:
                    return json.dumps(
                        {
                            "success": False,
                            "error": "Invalid content format: 'content' must be a valid JSON string",
                        }
                    )
                continue
            elif key == "status":
                # Validation already performed above, but keeping structure for robustness
                whiteboard[key] = value
            else:
                # Update general field
                whiteboard[key] = value

        whiteboard["updated_at"] = "2025-11-13T12:00:00"
        return json.dumps({"success": True, "whiteboard": whiteboard})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        # get_info method remains unchanged
        return {
            "type": "function",
            "function": {
                "name": "update_whiteboard",
                "description": (
                    "Update an existing whiteboard. "
                    "Requires whiteboard_id and payload. "
                    "Validates that whiteboard exists. "
                    "Updates the whiteboard record in place."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "whiteboard_id": {
                            "type": "string",
                            "description": "The whiteboard ID to update (required).",
                        },
                        "payload": {
                            "type": "object",
                            "description": "The data payload containing update fields.",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "The new title of the whiteboard.",
                                },
                                "content_action": {
                                    "type": "string",
                                    "description": "The action to perform on content: 'append', 'replace', or 'remove'.",
                                },
                                "content": {
                                    "type": "string",
                                    "description": (
                                        "The content item to add, update, or remove. "
                                        "Required fields depend on content_action: "
                                        "- For 'append': 'type' is required. 'text', and 'color' are optional while ID is auto-generated"
                                        'Example: \'{"type": "sticky_note", "text": "New idea", "color": "yellow"}\''
                                        "- For 'remove': only 'id' of the item to remove is required. "
                                        'Example: \'{"id": "3"}\''
                                        "- For 'replace': 'id' is required along with the specific fields to update (type, text, color, etc.)."
                                        'Example: \'{"id": "2", "type": "oval", "color": "blue"}\'\n'
                                    ),
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "ID of the content item.",
                                        },
                                        "type": {
                                            "type": "string",
                                            "description": "The shape of the content item. Enum = ['sticky_note', 'circle', 'rectangle', 'oval', 'diamond']",
                                        },
                                        "text": {
                                            "type": "string",
                                            "description": "Text content of the item.",
                                        },
                                        "color": {
                                            "type": "string",
                                            "description": 'Color of the content item. Enum = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "gray", "white", "black"]',
                                        },
                                    },
                                },
                                "status": {
                                    "type": "string",
                                    "description": "The status of the whiteboard. Enum = ['current', 'archived', 'deleted'].",
                                },
                                "updated_by": {
                                    "type": "string",
                                    "description": "The ID of the user making the update.",
                                },
                                "host_page_id": {
                                    "type": "string",
                                    "description": "The ID of the host page where the whiteboard is located.",
                                },
                                "host_space_id": {
                                    "type": "string",
                                    "description": "The ID of the host space where the whiteboard is located.",
                                },
                            },
                        },
                    },
                    "required": ["whiteboard_id", "payload"],
                },
            },
        }
