import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeletePageVersion(Tool):
    """
    Delete all versions of a specific page.
    - Used in Remove Page SOP when performing a hard delete to remove all page versions.
    - Deletes all page versions and their associated components for the given page_id.
    - Returns error if no versions are found for the page.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
    ) -> str:
        """
        Delete all page versions for a given page.

        Args:
            data: The complete database state
            page_id: The unique identifier of the page whose versions should be deleted

        Returns:
            JSON string with success message or error details
        """
        try:
            # Validate page_id is a string type
            if not isinstance(page_id, str):
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid page_id type: expected string, got {type(page_id).__name__}",
                    }
                )

            # Validate page_id is not empty
            if page_id == "":
                return json.dumps(
                    {
                        "success": False,
                        "error": "page_id cannot be empty",
                    }
                )

            # Get dictionaries (not lists)
            page_versions_dict = data.get("page_versions", {})
            page_version_components_dict = data.get("page_version_components", {})

            # Validate they are dictionaries
            if not isinstance(page_versions_dict, dict):
                return json.dumps(
                    {
                        "success": False,
                        "error": "Invalid page_versions container: expected dict",
                    }
                )

            if not isinstance(page_version_components_dict, dict):
                return json.dumps(
                    {
                        "success": False,
                        "error": "Invalid page_version_components container: expected dict",
                    }
                )

            # Find all versions for this page
            versions_to_delete = [
                v
                for v in page_versions_dict.values()
                if isinstance(v, dict) and v.get("page_id") == page_id
            ]

            if not versions_to_delete:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"No page versions found for page ID '{page_id}'",
                    }
                )

            # Get all version IDs to delete
            version_ids = [v["page_version_id"] for v in versions_to_delete]

            # Remove all page versions for this page
            # Create new dict without the deleted versions
            for version_id in version_ids:
                if version_id in page_versions_dict:
                    del page_versions_dict[version_id]

            # Remove all associated page version components
            # Find component IDs to delete
            component_ids_to_delete = [
                comp_id
                for comp_id, component in page_version_components_dict.items()
                if isinstance(component, dict)
                and component.get("page_version_id") in version_ids
            ]

            # Delete the components
            for comp_id in component_ids_to_delete:
                if comp_id in page_version_components_dict:
                    del page_version_components_dict[comp_id]

            return json.dumps(
                {
                    "success": True,
                    "message": f"Deleted {len(versions_to_delete)} version(s) for page '{page_id}'",
                    "deleted_count": len(versions_to_delete),
                    "deleted_versions": [
                        {
                            "page_version_id": v["page_version_id"],
                            "version_number": v["version_number"],
                        }
                        for v in versions_to_delete
                    ],
                }
            )

        except Exception as e:
            return json.dumps(
                {"success": False, "error": f"Failed to delete page versions: {str(e)}"}
            )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the tool specification for delete_page_version.

        Returns:
            Dictionary containing the tool's metadata and parameter schema
        """
        return {
            "type": "function",
            "function": {
                "name": "delete_page_version",
                "description": (
                    "Permanently deletes all version history records for a specific page. "
                    "This removes all stored versions of the page, including their content and metadata. "
                    "This operation is irreversible. "
                    "Typical usage: Called as part of hard delete operations after using delete_page with hard_delete=true. "
                    "When permanently removing a page, you must delete both the page record (via delete_page) "
                    "and its version history (via this function). "
                    "Validates that versions exist for the specified page before attempting deletion. "
                    "If no versions are found, the operation will fail. "
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The unique identifier of the page whose version history should be deleted. All versions associated with this page will be permanently removed. Required field.",
                        }
                    },
                    "required": ["page_id"],
                },
            },
        }
