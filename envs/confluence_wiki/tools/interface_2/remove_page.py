import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class RemovePage(Tool):
    """
    Delete a page (soft delete by default, hard delete if specified).
    - Used in Remove Page SOP.
    - Soft delete: Sets status to 'deleted' and updates metadata.
    - Hard delete: Permanently removes the page from the database.
    - Does NOT handle descendants (must be reassigned before calling this).
    - Does NOT delete page versions (use remove_page_version separately for hard delete).
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
        deleted_by: str,
        hard_delete: bool = False,
    ) -> str:
        """
        Delete a page (soft or hard delete).

        Args:
            data: The complete database state
            page_id: The unique identifier of the page to delete
            deleted_by: User ID performing the deletion
            hard_delete: If True, permanently removes the page; if False (default), sets status to 'deleted'

        Returns:
            JSON string with success message or error details
        """

        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid data format: 'data' must be a dict",
                }
            )

        pages_dict = data.get("pages", {})
        users_dict = data.get("users", {})

        # Validate page exists
        page_id_str = str(page_id)
        if page_id_str not in pages_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Page not found: page_id '{page_id}' does not exist",
                }
            )

        page = pages_dict[page_id_str]

        # Validate page is not already deleted (for soft delete)
        if not hard_delete and page.get("status") == "deleted":
            return json.dumps(
                {"success": False, "error": f"Page '{page_id}' is already deleted"}
            )

        # Validate page is not locked
        if page.get("status") == "locked":
            return json.dumps(
                {
                    "success": False,
                    "error": f"Cannot delete locked page: page_id '{page_id}'",
                }
            )

        # Validate page is not archived
        if page.get("status") == "archived":
            return json.dumps(
                {
                    "success": False,
                    "error": f"Cannot delete archived page: page_id '{page_id}'. Unarchive it first.",
                }
            )

        # Validate user exists
        deleted_by_str = str(deleted_by)
        if deleted_by_str not in users_dict:
            return json.dumps(
                {
                    "success": False,
                    "error": f"User not found: deleted_by '{deleted_by}' does not exist",
                }
            )

        # Check for descendants (should be handled before calling delete)
        has_descendants = any(
            p.get("parent_page_id") == page_id_str
            for p in pages_dict.values()
            if isinstance(p, dict)
        )

        if has_descendants:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Cannot delete page '{page_id}': page has child pages. Reassign children first using modify_page.",
                }
            )

        page_title = page.get("title", "Unknown")

        if hard_delete:
            # Hard delete: Remove page from database
            del pages_dict[page_id_str]

            return json.dumps(
                {
                    "success": True,
                    "message": f"Page '{page_title}' (ID: {page_id}) permanently deleted",
                    "delete_type": "hard",
                    "page_id": page_id_str,
                    "title": page_title,
                }
            )
        else:
            # Soft delete: Set status to 'deleted' and update metadata
            current_time = "2025-11-13T12:00:00"

            page["status"] = "deleted"
            page["updated_by"] = deleted_by_str
            page["updated_at"] = current_time

            return json.dumps(
                {
                    "success": True,
                    "message": f"Page '{page_title}' (ID: {page_id}) marked as deleted",
                    "delete_type": "soft",
                    "page_id": page_id_str,
                    "title": page_title,
                    "deleted_by": deleted_by_str,
                    "deleted_at": current_time,
                }
            )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the tool specification for remove_page.

        Returns:
            Dictionary containing the tool's metadata and parameter schema
        """
        return {
            "type": "function",
            "function": {
                "name": "remove_page",
                "description": (
                    "Deletes a wiki page using either soft delete or hard delete."
                    "Soft delete (default): Sets the page status to 'deleted' while preserving the record in the database."
                    "The page can potentially be restored later. This is the recommended and safer deletion method."
                    "Hard delete: Permanently removes the page record from the database. This action is irreversible."
                    "When using hard delete, you must separately call remove_page_version to remove all associated page versions."
                    "Prerequisites that must be met before deletion:"
                    "- Page must not have 'locked' or 'archived' status"
                    "- Page must have no child pages (use modify_page to reassign children to a new parent first)"
                    "- User must have delete permission for the page"
                    "Automatically updates 'deleted_by' and 'deleted_at' metadata for audit tracking."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The unique identifier of the page to delete. Required field.",
                        },
                        "deleted_by": {
                            "type": "string",
                            "description": "The user ID of the person performing the deletion. Required field for audit tracking.",
                        },
                        "hard_delete": {
                            "type": "boolean",
                            "description": "Deletion type. If true, permanently removes the page from the database (irreversible). If false (default), marks the page as deleted but preserves the record. Use false unless permanent removal is specifically required.",
                        },
                    },
                    "required": ["page_id", "deleted_by"],
                },
            },
        }
