import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdatePage(Tool):

    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, last_modified_by: str, **updates: Any) -> str:
        IMMUTABLE_FIELDS = {"id"}
        pages = data.get("pages", {})
        if page_id not in pages:
            raise ValueError("Page not found")

        if updates == {}:
            raise ValueError("No parameters to update")

        page = pages[page_id]

        # Apply each provided field except immutables and None values (optional choice)
        for key, value in updates.items():
            if key in IMMUTABLE_FIELDS or key == "page_id":
                continue
            if value is None:
                continue  # drop Nones; remove this if you want to allow explicit nulling
            page[key] = value
        
        # Ensure the page has an updated_at field
        updated_at = "2025-07-01T00:00:00Z"

        page["updated_at"] = updated_at
        page["last_modified_by"] = last_modified_by
        # Return the updated page as a JSON string
        pages[page_id] = page
        # data["pages"] = pages  # Update the original data structure

        return json.dumps(page)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Return a function schema where each updatable field is a top-level parameter.
        Adjust the properties list to match the actual schema in your data model.
        """
        return {
            "type": "function",
            "function": {
                "name": "update_page",
                "description": "Update page content fields by ID. Omit any field you do not want to change.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page to update."
                        },
                        "space_id": {
                            "type": "integer",
                            "description": "Space that owns the page."
                        },
                        "title": {
                            "type": "string",
                            "description": "Page title."
                        },
                        "content": {
                            "type": "string",
                            "description": "Page body content."
                        },
                        "content_format": {
                            "type": "string",
                            "description": "Format of `content` (e.g., 'md', 'html')."
                        },
                        "parent_id": {
                            "type": ["integer", "null"],
                            "description": "Parent page ID, if any."
                        },
                        "position": {
                            "type": "integer",
                            "description": "Ordering position."
                        },
                        "status": {
                            "type": "string",
                            "description": "Publication status (e.g., 'draft', 'historical')."
                        },
                        "version": {
                            "type": "integer",
                            "description": "Version number."
                        },
                        "template_id": {
                            "type": ["integer", "null"],
                            "description": "Associated template ID, if any."
                        },
                        "excerpt": {
                            "type": "string",
                            "description": "Short summary / preview text."
                        },
                        "created_at": {
                            "type": "string",
                            "description": "ISO8601 creation timestamp."
                        },
                        "updated_at": {
                            "type": "string",
                            "description": "ISO8601 last update timestamp."
                        },
                        "published_at": {
                            "type": ["string", "null"],
                            "description": "ISO8601 publication timestamp, if published."
                        },
                        "created_by": {
                            "type": "integer",
                            "description": "User ID that created the page."
                        },
                        "last_modified_by": {
                            "type": "integer",
                            "description": "User ID that last modified the page."
                        },
                    },
                    "required": ["page_id", "last_modified_by"]
                }
            }
        }
