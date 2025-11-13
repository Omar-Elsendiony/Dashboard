import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class MakePageVersion(Tool):
    """
    Create a new version of a page.
    - Requires page_id.
    - Only allows pages with status 'current'.
    - Captures the current state of the page (title and body_storage).
    - Auto-generates version_number (next sequential for that page).
    - Auto-generates page_version_id, created_at.
    - Validates that page exists and has 'current' status.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
        title: Optional[str] = None,
        body_storage: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "page_version": {...}} on success
          {"success": False, "error": "..."} on error
        """

        # Basic input validation
        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid data format: 'data' must be a dict",
                }
            )

        pages_dict = data.get("pages", {})
        if not isinstance(pages_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid pages container: expected dict at data['pages']",
                }
            )

        page_versions_dict = data.get("page_versions", {})
        if not isinstance(page_versions_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid page_versions container: expected dict at data['page_versions']",
                }
            )

        page_version_components_dict = data.get("page_version_components", {})
        if not isinstance(page_version_components_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid page_version_components container: expected dict at data['page_version_components']",
                }
            )

        whiteboards_dict = data.get("whiteboards", {})
        if not isinstance(whiteboards_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid whiteboards container: expected dict at data['whiteboards']",
                }
            )

        smart_links_dict = data.get("smart_links", {})
        if not isinstance(smart_links_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid smart_links container: expected dict at data['smart_links']",
                }
            )

        # Validate required fields
        if page_id is None:
            return json.dumps({"success": False, "error": "page_id is required"})

        # Convert IDs to strings for consistent comparison
        page_id_str = str(page_id)

        # Validate page exists
        if page_id_str not in pages_dict:
            return json.dumps(
                {"success": False, "error": f"Page with ID '{page_id_str}' not found"}
            )

        # Get current page data
        current_page = pages_dict[page_id_str]
        if not isinstance(current_page, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid page data for page ID '{page_id_str}'",
                }
            )

        # Validate page status is 'current'
        page_status = current_page.get("status")
        if page_status != "current":
            return json.dumps(
                {
                    "success": False,
                    "error": f"Page with ID '{page_id_str}' has status '{page_status}'. Only pages with status 'current' can have versions created.",
                }
            )

        # Use provided title/body_storage or fall back to current page values
        # Treat empty strings the same as None (use page's current values)
        version_title = (
            title
            if (title is not None and title != "")
            else current_page.get("title", "")
        )
        version_body_storage = (
            body_storage
            if (body_storage is not None and body_storage != "")
            else current_page.get("body_storage", "")
        )

        # Calculate next version number for this page
        existing_versions_for_page = [
            v.get("version_number", 0)
            for v in page_versions_dict.values()
            if isinstance(v, dict) and str(v.get("page_id")) == page_id_str
        ]

        if existing_versions_for_page:
            # If versions exist, next version is max + 1
            new_version_number = max(existing_versions_for_page) + 1
        else:
            # First version for this page
            new_version_number = 1

        # Generate new page_version_id
        def generate_page_version_id(page_versions: Dict[str, Any]) -> str:
            if not page_versions:
                return "1"
            try:
                max_id = max(int(k) for k in page_versions.keys() if k.isdigit())
                return str(max_id + 1)
            except ValueError:
                # If no numeric keys, start from 1
                return "1"

        new_page_version_id = generate_page_version_id(page_versions_dict)

        # Generate timestamp
        current_time = "2025-11-13T12:00:00"

        # Create new page version (only fields from schema)
        new_page_version = {
            "page_version_id": new_page_version_id,
            "page_id": page_id_str,
            "version_number": new_version_number,
            "title": version_title,
            "body_storage": version_body_storage,
            "created_at": current_time,
        }

        # Add version to data (modify in place)
        page_versions_dict[new_page_version_id] = new_page_version
        # Fetch and save related whiteboards and smart links
        created_components = []

        # Helper function to generate component_id
        def generate_component_id(components: Dict[str, Any]) -> str:
            if not components:
                return "1"
            try:
                max_id = max(int(k) for k in components.keys() if k.isdigit())
                return str(max_id + 1)
            except ValueError:
                return "1"

        # Find whiteboards with host_page_id matching this page
        for whiteboard_id, whiteboard in whiteboards_dict.items():
            if not isinstance(whiteboard, dict):
                continue
            if str(whiteboard.get("host_page_id")) == page_id_str:
                # Parse content from JSON string to array
                content_str = whiteboard.get("content", "[]")
                try:
                    content = (
                        json.loads(content_str)
                        if isinstance(content_str, str)
                        else content_str
                    )
                except json.JSONDecodeError:
                    content = []

                # Create component_data for whiteboard
                component_data = {
                    "whiteboard_id": whiteboard_id,
                    "content": content,
                    "version": whiteboard.get("status", "current"),
                }

                component_id = generate_component_id(page_version_components_dict)

                # Create page_version_component
                component = {
                    "component_id": component_id,
                    "page_version_id": new_page_version_id,
                    "component_type": "whiteboard",
                    "component_data": component_data,
                }

                page_version_components_dict[component_id] = component
                created_components.append(component)

        # Find smart_links with parent_id matching this page and parent_type == 'page'
        for smart_link_id, smart_link in smart_links_dict.items():
            if not isinstance(smart_link, dict):
                continue
            if str(smart_link.get("host_page_id")) == page_id_str:
                # Create component_data for smart_link
                component_data = {
                    "smart_link_id": smart_link_id,
                    "title": smart_link.get("title", ""),
                    "url": smart_link.get("url", ""),
                }

                component_id = generate_component_id(page_version_components_dict)

                # Create page_version_component
                component = {
                    "component_id": component_id,
                    "page_version_id": new_page_version_id,
                    "component_type": "smart_link",
                    "component_data": component_data,
                }

                page_version_components_dict[component_id] = component
                created_components.append(component)

        return json.dumps(
            {
                "success": True,
                "page_version": new_page_version,
                "components": created_components,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "make_page_version",
                "description": (
                    "Create a new version of a page. "
                    "Requires page_id. "
                    "Only allows pages with status 'current'. "
                    "Captures the current state of the page (title and body_storage) unless overridden. "
                    "Auto-generates version_number (next sequential for that page) and page_version_id. "
                    "Validates that page exists and has 'current' status."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The page ID to create a version for (required). Page must have status 'current'.",
                        },
                        "title": {
                            "type": "string",
                            "description": "The title for this version (optional, defaults to current page title).",
                        },
                        "body_storage": {
                            "type": "string",
                            "description": "The body content for this version (optional, defaults to current page body_storage).",
                        },
                    },
                    "required": ["page_id"],
                },
            },
        }
