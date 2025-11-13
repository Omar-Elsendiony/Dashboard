import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class FetchVersions(Tool):
    """
    Retrieve page versions with flexible filters.
    - Returns ALL page versions when no filters are provided.
    - Applies all provided filters using AND logic.
    - Safe handling of ID comparisons (cast to str) and datetime prefix matches.
    - Used primarily in the Remove Page SOP for hard delete operations.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_version_id: Optional[str] = None,
        page_id: Optional[str] = None,
        version_number: Optional[str] = None,
        title: Optional[str] = None,
        created_by: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "page_versions": [...]} on success
          {"success": False, "error": "..."} on error
        """

        # --- Basic input validation ---
        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid data format: 'data' must be a dict",
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

        # --- Validate and convert version_number if provided ---
        version_number_int = None
        if version_number is not None:
            try:
                version_number_int = int(version_number)
                if version_number_int < 1:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"Invalid version_number: must be a positive integer, got {version_number}",
                        }
                    )
            except (ValueError, TypeError):
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid version_number: cannot convert '{version_number}' to integer",
                    }
                )

        # --- Collect active filters (keep None out) ---
        filters = {
            "page_version_id": page_version_id,
            "page_id": page_id,
            "version_number": version_number,
            "title": title,
            "created_by": created_by,
            "created_at": created_at,
        }
        active_filters = {k: v for k, v in filters.items() if v is not None}

        # Start with all page versions (dict copy to avoid mutating original rows)
        all_versions: List[Dict[str, Any]] = [
            v.copy() for v in page_versions_dict.values() if isinstance(v, dict)
        ]

        # If no filters, return everything
        if not active_filters:
            return json.dumps({"success": True, "page_versions": all_versions})

        # --- Apply filters incrementally (AND logic) ---
        results = all_versions

        # ID / FK filters (compare as string)
        if page_version_id is not None:
            pvid = str(page_version_id)
            results = [v for v in results if v.get("page_version_id") == pvid]

        if page_id is not None:
            pid = str(page_id)
            results = [v for v in results if v.get("page_id") == pid]

        if created_by is not None:
            uid = str(created_by)
            results = [v for v in results if v.get("created_by") == uid]

        # Version number filter (exact match as integer)
        if version_number_int is not None:
            results = [
                v for v in results if v.get("version_number") == version_number_int
            ]

        # Case-insensitive partial match for title
        if title is not None:
            try:
                pat = re.compile(re.escape(title), re.IGNORECASE)
                results = [
                    v
                    for v in results
                    if "title" in v and v["title"] and pat.search(v["title"])
                ]
            except re.error:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid regex pattern in title: {title}",
                    }
                )

        # Datetime prefix filter (e.g., "2025-10-01")
        if created_at is not None:
            results = [
                v for v in results if v.get("created_at", "").startswith(created_at)
            ]

        return json.dumps({"success": True, "page_versions": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "fetch_versions",
                "description": (
                    "Retrieves version history records for wiki pages. "
                    "Each time a page is edited, a new version is created with an incremented version number. "
                    "When called with no parameters, returns all page versions across the entire wiki system. "
                    "When called with parameters, filters and returns only matching versions. "
                    "Common use cases:"
                    "- Get all versions of a specific page by providing 'page_id' (most common usage)"
                    "- Get a specific version by providing both 'page_id' and 'version_number'"
                    "- Find versions by title content, creator, or creation date"
                    "- Retrieve all versions before performing a hard delete operation on a page"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_version_id": {
                            "type": "string",
                            "description": "The unique identifier for a specific page version record. Performs exact match. Use this when you need to retrieve one specific version record by its internal ID.",
                        },
                        "page_id": {
                            "type": "string",
                            "description": "The unique identifier for a page. Performs exact match and returns ALL versions of that page, ordered by version number. This is the most commonly used filter.",
                        },
                        "version_number": {
                            "type": "string",
                            "description": "The version number of a page (1 = first version, 2 = second version, etc.). Performs exact match. Must be a positive integer provided as a string. Typically combined with 'page_id' to get a specific version of a specific page.",
                        },
                        "title": {
                            "type": "string",
                            "description": "Searches within page version titles. Performs partial, case-insensitive matching. Useful for finding versions across different pages with similar titles.",
                        },
                        "created_by": {
                            "type": "string",
                            "description": "Filters versions by the user who created them. Performs exact match on user ID. Use this to find all page versions (edits) made by a specific user across all pages.",
                        },
                        "created_at": {
                            "type": "string",
                            "description": "Filters versions by creation date/time. Performs prefix matching on ISO datetime format. Useful for auditing or finding recent changes.",
                        },
                    },
                    "required": [],
                },
            },
        }
