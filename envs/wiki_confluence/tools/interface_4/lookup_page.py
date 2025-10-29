import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class LookupPage(Tool):
    """
    A tool to retrieve or search for pages within a database (e.g., Confluence).
    It supports flexible filtering based on various page attributes.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: Optional[Any] = None,
        space_id: Optional[Any] = None,
        parent_page_id: Optional[Any] = None,
        title: Optional[str] = None,
        content_format: Optional[str] = None,
        current_version: Optional[Any] = None,
        state: Optional[str] = None,
        created_by_user_id: Optional[Any] = None,
        updated_by_user_id: Optional[Any] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        is_trashed: Optional[bool] = None,
        is_published: Optional[bool] = None
    ) -> str:
        """
        Retrieve pages based on a set of optional filters.
        If no filters are provided, all pages are returned.
        Filters are combined with an 'AND' logic.
        """

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format: 'data' must be a dict"
            })

        pages_dict = data.get("pages", {})
        if not isinstance(pages_dict, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid pages container: expected dict at data['pages']"
            })

        # --- Check for active filters ---
        filters = {
            'page_id': page_id,
            'space_id': space_id,
            'parent_page_id': parent_page_id,
            'title': title,
            'content_format': content_format,
            'current_version': current_version,
            'state': state,
            'created_by_user_id': created_by_user_id,
            'updated_by_user_id': updated_by_user_id,
            'created_at': created_at,
            'updated_at': updated_at,
            'is_trashed': is_trashed,
            'is_published': is_published,
        }
        
        # We check against None because `is_trashed=False` is a valid, active filter
        active_filters = {k: v for k, v in filters.items() if v is not None}

        # Start with all pages
        all_pages: List[Dict[str, Any]] = [
            page.copy() for page in pages_dict.values() 
            if isinstance(page, dict)
        ]
        
        # If no filters are active, return all pages
        if not active_filters:
            return json.dumps({"success": True, "pages": all_pages})

        # --- Apply active filters ---
        results = all_pages

        # --- ID Filters (Handle str or int input, compare as str) ---
        # The database stores IDs as strings. Convert filter input to string.
        if page_id is not None:
            str_page_id = str(page_id)
            results = [p for p in results if p.get('page_id') == str_page_id]

        if space_id is not None:
            str_space_id = str(space_id)
            results = [p for p in results if p.get('space_id') == str_space_id]

        if parent_page_id is not None:
            str_parent_page_id = str(parent_page_id)
            results = [p for p in results if p.get('parent_page_id') == str_parent_page_id]

        if created_by_user_id is not None:
            str_created_by = str(created_by_user_id)
            results = [p for p in results if p.get('created_by_user_id') == str_created_by]

        if updated_by_user_id is not None:
            str_updated_by = str(updated_by_user_id)
            results = [p for p in results if p.get('updated_by_user_id') == str_updated_by]

        # --- Title Filter (Case-insensitive, partial match) ---
        if title is not None:
            try:
                pattern = re.compile(re.escape(title), re.IGNORECASE)
                # Ensure 'title' key exists and is not None before searching
                results = [
                    p for p in results 
                    if 'title' in p and p['title'] and pattern.search(p['title'])
                ]
            except re.error:
                return json.dumps({"success": False, "error": f"Invalid regex pattern in title: {title}"})

        # --- Enum Filters (Exact match) ---
        if content_format is not None:
            results = [p for p in results if p.get('content_format') == content_format]

        if state is not None:
            results = [p for p in results if p.get('state') == state]

        # --- Version Filter (Handle str or int input, compare as int) ---
        # The database stores version as an integer. Convert filter input to int.
        if current_version is not None:
            try:
                int_version = int(current_version)
                results = [p for p in results if p.get('current_version') == int_version]
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False, 
                    "error": f"Invalid format for current_version: expected an integer or numeric string, got '{current_version}'"
                })

        # --- Datetime Filters (String starts-with) ---
        if created_at is not None:
            # Use .get(key, '') to avoid error if key is missing
            results = [p for p in results if p.get('created_at', '').startswith(created_at)]
            
        if updated_at is not None:
            results = [p for p in results if p.get('updated_at', '').startswith(updated_at)]

        # --- Boolean Filters (Exact match) ---
        if is_trashed is not None:
            # Use `is` for strict boolean comparison (True, False, None)
            results = [p for p in results if p.get('is_trashed') is is_trashed]
            
        if is_published is not None:
            results = [p for p in results if p.get('is_published') is is_published]
            
        # --- Return Results ---
        # If filters are given and no item matches, this will correctly
        # return an empty list: {"success": True, "pages": []}
        return json.dumps({"success": True, "pages": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Provides the schema and description for the get_page tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "get_page",
                "description": "Retrieve or search for pages based on a set of filters. Returns a list of pages. If no filters are provided, returns all pages.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "Unique identifier of the page (e.g., '123' or 123). Matches exact ID."
                        },
                        "space_id": {
                            "type": "string",
                            "description": "Filter by space identifier (e.g., '45' or 45)."
                        },
                        "parent_page_id": {
                            "type": "string",
                            "description": "Filter by parent page identifier (e.g., '67' or 67)."
                        },
                        "title": {
                            "type": "string",
                            "description": "Page title to search for (supports partial matching, case-insensitive)."
                        },
                        "content_format": {
                            "type": "string",
                            "description": "'markdown', 'html', 'richtext'",
                            "enum": ["markdown", "html", "richtext"]
                        },
                        "current_version": {
                            "type": "integer",
                            "description": "Filter by the current version number (e.g., 1 or '1')."
                        },
                        "state": {
                            "type": "string",
                            "description": "'draft', 'published', 'archived'",
                            "enum": ["draft", "published", "archived"]
                        },
                        "created_by_user_id": {
                            "type": "string",
                            "description": "Filter by the user ID of the creator (e.g., '10' or 10)."
                        },
                        "updated_by_user_id": {
                            "type": "string",
                            "description": "Filter by the user ID of the last updater (e.g., '11' or 11)."
                        },
                        "created_at": {
                            "type": "string",
                            "description": "Filter by creation timestamp. Matches if the timestamp string starts with the provided value (e.g., '2025-09-14')."
                        },
                        "updated_at": {
                            "type": "string",
                            "description": "Filter by update timestamp. Matches if the timestamp string starts with the provided value (e.g., '2025-09-15')."
                        },
                        "is_trashed": {
                            "type": "boolean",
                            "description": "Filter by whether the page is in the trash (true/false)."
                        },
                        "is_published": {
                            "type": "boolean",
                            "description": "Filter by whether the page is published (true/false)."
                        }
                    },
                    "required": [] # No parameters are required
                }
            }
        }
