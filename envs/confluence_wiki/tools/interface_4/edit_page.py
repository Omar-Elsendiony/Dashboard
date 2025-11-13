import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool


class EditPage(Tool):
    """
    Update an existing page's properties.
    - Used in Update Page SOP for moving pages, changing parents, and updating titles.
    - Updates the 'updated_by' and 'updated_at' timestamps automatically.
    - Validates that the page exists and is not in 'deleted' status.
    - Validates no duplicate titles exist when changing space or parent.
    - Does not create page versions (handled separately by establish_page_version).
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
        updated_by: str,
        title: Optional[str] = None,
        space_id: Optional[str] = None,
        parent_page_id: Optional[str] = None,
        body_storage: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "page": {...}} on success
          {"success": False, "error": "..."} on error
        """

        # Helper function to get sibling pages
        def get_sibling_pages(
            pages_dict: Dict[str, Any],
            space_id: str,
            parent_page_id: Optional[str],
            exclude_page_id: Optional[str] = None,
        ) -> List[Dict[str, Any]]:
            """
            Get all pages that would be siblings in the given location.

            Args:
                pages_dict: Dictionary of all pages
                space_id: The space ID to check
                parent_page_id: The parent page ID (None for root pages)
                exclude_page_id: Page ID to exclude from results (the page being updated)

            Returns:
                List of sibling pages
            """
            siblings = []

            for page_key, page in pages_dict.items():
                if not isinstance(page, dict):
                    continue

                # Skip the page being updated
                if exclude_page_id and str(page.get("page_id")) == str(exclude_page_id):
                    continue

                # Check if in same space
                if str(page.get("space_id")) != str(space_id):
                    continue

                # Check if has same parent
                page_parent = page.get("parent_page_id")

                if parent_page_id is None:
                    # Looking for root pages (no parent)
                    if page_parent is None:
                        siblings.append(page)
                else:
                    # Looking for pages with specific parent
                    if page_parent is not None and str(page_parent) == str(
                        parent_page_id
                    ):
                        siblings.append(page)

            return siblings

        # --- Basic input validation ---
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

        users_dict = data.get("users", {})
        if not isinstance(users_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid users container: expected dict at data['users']",
                }
            )

        # --- Validate required parameters ---
        if not page_id:
            return json.dumps(
                {"success": False, "error": "Missing required parameter: page_id"}
            )

        if not updated_by:
            return json.dumps(
                {"success": False, "error": "Missing required parameter: updated_by"}
            )

        # --- Validate page exists ---
        page_id_str = str(page_id)
        if page_id_str not in pages_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Page not found: page_id '{page_id}' does not exist",
                }
            )

        page = pages_dict[page_id_str]

        # --- Validate page is not deleted ---
        if page.get("status") == "deleted":
            return json.dumps(
                {
                    "success": False,
                    "error": f"Cannot update deleted page: page_id '{page_id}'",
                }
            )

        # --- Validate user exists ---
        updated_by_str = str(updated_by)
        if updated_by_str not in users_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"User not found: updated_by '{updated_by}' does not exist",
                }
            )

        # --- Validate status enum if provided ---
        valid_statuses = ["current", "draft", "archived", "locked"]
        if status is not None and status not in valid_statuses:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid status value: '{status}'. Must be one of {valid_statuses}",
                }
            )

        # --- Validate space_id if provided ---
        if space_id is not None:
            spaces_dict = data.get("spaces", {})
            space_id_str = str(space_id)
            if space_id_str not in spaces_dict:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Space not found: space_id '{space_id}' does not exist",
                    }
                )
            if spaces_dict[space_id_str].get("status") == "archived":
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Cannot move page to archived space: space_id '{space_id}'",
                    }
                )

        # --- Validate parent_page_id if provided ---
        if parent_page_id is not None:
            # Allow explicit null to set as root page
            if parent_page_id != "":
                parent_id_str = str(parent_page_id)
                if parent_id_str not in pages_dict:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Parent page not found: parent_page_id '{parent_page_id}' does not exist",
                        }
                    )

                parent_page = pages_dict[parent_id_str]
                if parent_page.get("status") == "deleted":
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Cannot set deleted page as parent: parent_page_id '{parent_page_id}'",
                        }
                    )

                # Prevent setting a page as its own parent
                if parent_id_str == page_id_str:
                    return json.dumps(
                        {
                            "success": False,
                            "error": "Cannot set a page as its own parent",
                        }
                    )

                # Prevent circular references (check if new parent is a descendant)
                current = parent_page
                while current.get("parent_page_id"):
                    if current.get("parent_page_id") == page_id_str:
                        return json.dumps(
                            {
                                "success": False,
                                "error": "Cannot create circular parent relationship",
                            }
                        )
                    current = pages_dict.get(current.get("parent_page_id"), {})

        # --- Validate no duplicate titles when changing space or parent ---
        # Determine the final title (after update)
        final_title = title if title is not None else page.get("title")

        # Determine the final space (after update)
        final_space_id = str(space_id) if space_id is not None else page.get("space_id")

        # Determine the final parent (after update)
        if parent_page_id is not None:
            final_parent_page_id = str(parent_page_id) if parent_page_id != "" else None
        else:
            final_parent_page_id = page.get("parent_page_id")

        # Check if space or parent is changing
        space_is_changing = space_id is not None and str(space_id) != page.get(
            "space_id"
        )
        parent_is_changing = parent_page_id is not None and (
            str(parent_page_id) if parent_page_id != "" else None
        ) != page.get("parent_page_id")

        # If space or parent is changing, check for duplicate titles in the new location
        if space_is_changing or parent_is_changing:
            # Get siblings in the new location
            siblings = get_sibling_pages(
                pages_dict,
                final_space_id,
                final_parent_page_id,
                exclude_page_id=page_id_str,
            )

            # Check if any sibling has the same title (case-insensitive)
            for sibling in siblings:
                sibling_title = sibling.get("title", "")
                if sibling_title.lower() == final_title.lower():
                    location_desc = (
                        f"space '{final_space_id}' under parent '{final_parent_page_id}'"
                        if final_parent_page_id
                        else f"root level of space '{final_space_id}'"
                    )
                    return json.dumps(
                        {
                            "success": False,
                            "error": (
                                f"Duplicate title: A page with title '{final_title}' already exists in {location_desc}. "
                                f"Page titles must be unique among siblings."
                            ),
                        }
                    )

        # --- Apply updates ---
        updated_at = datetime.utcnow().isoformat() + "Z"

        if title is not None:
            page["title"] = title

        if space_id is not None:
            page["space_id"] = str(space_id)

        if parent_page_id is not None:
            # Empty string means set as root page (null parent)
            page["parent_page_id"] = (
                str(parent_page_id) if parent_page_id != "" else None
            )

        if body_storage is not None:
            page["body_storage"] = body_storage

        if status is not None:
            page["status"] = status

        # Always update metadata
        page["updated_by"] = updated_by_str
        page["updated_at"] = updated_at

        return json.dumps({"success": True, "page": page})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "edit_page",
                "description": (
                    "Updates properties of an existing wiki page. "
                    "Can modify page metadata (title, status), content (body), and hierarchical relationships (space, parent page). "
                    "Automatically updates 'updated_by' and 'updated_at' timestamps. "
                    "Validates that the page exists and is not deleted before updating. "
                    "Validates that any referenced entities (space, parent page) exist and are valid. "
                    "IMPORTANT: When changing space_id or parent_page_id, validates that no sibling page has the same title. "
                    "Page titles must be unique among siblings (pages with the same parent in the same space). "
                    "Common use cases:"
                    "- Move pages between spaces by changing 'space_id' (checks for duplicate titles in target space)"
                    "- Reorganize page hierarchy by changing 'parent_page_id' or setting pages as root pages (checks for duplicate titles among new siblings)"
                    "- Update page titles and content"
                    "- Change page status (draft, current, archived, locked)"
                    "- Reassign child pages to a new parent when their original parent is being removed"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The unique identifier of the page to update. Required field.",
                        },
                        "updated_by": {
                            "type": "string",
                            "description": "The user ID of the person performing the update. Required field for audit tracking.",
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the page. Optional. Only provide if you want to change the title. When changing space or parent, the new title must be unique among siblings.",
                        },
                        "space_id": {
                            "type": "string",
                            "description": "ID of the space to move the page to. Optional. Must reference a valid, non-archived space. Validates that no page with the same title exists at the same level in the target space. Only provide when moving pages between spaces.",
                        },
                        "parent_page_id": {
                            "type": "string",
                            "description": "ID of the new parent page to nest this page under. Optional. Provide empty string to make this a root-level page with no parent. Must not create circular references (page cannot be its own ancestor). Validates that no sibling under the new parent has the same title. Only provide when reorganizing page hierarchy.",
                        },
                        "body_storage": {
                            "type": "string",
                            "description": "Updated content/body of the page in storage format. Optional. Only provide if you want to change the page content.",
                        },
                        "status": {
                            "type": "string",
                            "description": "Status for the page. The accepted values are 'current', 'draft', 'archived', 'locked'. Optional and only provide if you want to change the status.",
                        },
                    },
                    "required": ["page_id", "updated_by"],
                },
            },
        }
