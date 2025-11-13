import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class RetrievePage(Tool):
    """
    Retrieve or search for pages with flexible filters.
    - Returns ALL pages when no filters are provided.
    - Applies all provided filters using AND logic.
    - Safe handling of ID comparisons (cast to str), enums, and datetime prefix matches.
    - Case-insensitive partial matching for title.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: Optional[str] = None,
        space_id: Optional[str] = None,
        parent_page_id: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "pages": [...]} on success
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

        # Validate enum values if provided (empty strings are valid and will return empty results)
        valid_statuses = ["current", "draft", "locked", "archived", "deleted"]

        if status is not None and status != "" and status not in valid_statuses:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid status value: '{status}'. Must be one of {valid_statuses}",
                }
            )

        # Collect active filters (empty strings are valid filter values that return empty results)
        filters = {
            "page_id": page_id,
            "space_id": space_id,
            "parent_page_id": parent_page_id,
            "title": title,
            "status": status,
            "created_by": created_by,
            "updated_by": updated_by,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        # Filter out None only - empty strings are valid filter values that return empty results
        active_filters = {k: v for k, v in filters.items() if v is not None}

        # Start with all pages (dict copy to avoid mutating original rows)
        all_pages: List[Dict[str, Any]] = [
            p.copy() for p in pages_dict.values() if isinstance(p, dict)
        ]

        # If no filters, return everything
        if not active_filters:
            return json.dumps({"success": True, "pages": all_pages})

        # Apply filters incrementally (AND logic)
        results = all_pages

        # Only apply filter if value is not None
        if page_id is not None:
            pid = str(page_id)
            results = [p for p in results if p.get("page_id") == pid]

        if space_id is not None:
            sid = str(space_id)
            results = [p for p in results if p.get("space_id") == sid]

        if parent_page_id is not None:
            # Handle null parent_page_id case (to find root pages with no parent)
            if str(parent_page_id).lower() in ["null", "none"]:
                results = [p for p in results if p.get(
                    "parent_page_id") is None]
            else:
                ppid = str(parent_page_id)
                results = [p for p in results if p.get(
                    "parent_page_id") == ppid]

        if created_by is not None:
            uid = str(created_by)
            results = [p for p in results if p.get("created_by") == uid]

        if updated_by is not None:
            uid = str(updated_by)
            results = [p for p in results if p.get("updated_by") == uid]

        # Case-insensitive partial match for title
        if title is not None:
            try:
                pat = re.compile(re.escape(title), re.IGNORECASE)
                results = [
                    p
                    for p in results
                    if "title" in p and p["title"] and pat.search(p["title"])
                ]
            except re.error:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid regex pattern in title: {title}",
                    }
                )

        # Exact string filter for status
        if status is not None:
            results = [p for p in results if p.get("status") == status]

        # Datetime prefix filters
        if created_at is not None:
            results = [
                p for p in results if p.get("created_at", "").startswith(created_at)
            ]

        if updated_at is not None:
            results = [
                p for p in results if p.get("updated_at", "").startswith(updated_at)
            ]

        return json.dumps({"success": True, "pages": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "retrieve_page",
                "description": (
                    "Retrieve or search for pages based on optional filters. "
                    "Returns a list of pages; if no filters are provided, returns all pages. "
                    "Supports partial, case-insensitive matching for 'title', "
                    "exact match for 'status', "
                    "and datetime prefix matches for 'created_at'/'updated_at'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "Exact page ID match (accepts int-like input but compared as string).",
                        },
                        "space_id": {
                            "type": "string",
                            "description": "Exact space ID match (accepts int-like input but compared as string).",
                        },
                        "parent_page_id": {
                            "type": "string",
                            "description": "Exact parent page ID match (accepts int-like input but compared as string). Use 'null' or 'none' to find pages with no parent.",
                        },
                        "title": {
                            "type": "string",
                            "description": "Case-insensitive partial match for the page title.",
                        },
                        "status": {
                            "type": "string",
                            "description": "Exact match for page status ('current', 'draft', 'locked', 'archived', or 'deleted').",
                        },
                        "created_by": {
                            "type": "string",
                            "description": "Exact match on the creator user ID (compared as string).",
                        },
                        "updated_by": {
                            "type": "string",
                            "description": "Exact match on the updater user ID (compared as string).",
                        },
                        "created_at": {
                            "type": "string",
                            "description": "Datetime prefix match on created_at (e.g., '2025-10-01').",
                        },
                        "updated_at": {
                            "type": "string",
                            "description": "Datetime prefix match on updated_at (e.g., '2025-10').",
                        },
                    },
                    "required": [],
                },
            },
        }
