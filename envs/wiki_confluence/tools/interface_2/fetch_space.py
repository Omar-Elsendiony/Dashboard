import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class FetchSpace(Tool):
    """
    Retrieve or search for spaces with flexible filters.
    - Returns ALL spaces when no filters are provided.
    - Applies all provided filters using AND logic.
    - Safe handling of ID comparisons (cast to str), booleans, and datetime prefix matches.
    - Case-insensitive partial matching for space_name and space_purpose.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        space_id: Optional[Any] = None,
        space_key: Optional[str] = None,
        space_name: Optional[str] = None,
        space_purpose: Optional[str] = None,
        created_by_user_id: Optional[Any] = None,
        created_at: Optional[str] = None,
        is_deleted: Optional[bool] = None,
        deleted_at: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "spaces": [...]} on success
          {"success": False, "error": "..."} on error
        """

        # --- Basic input validation ---
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format: 'data' must be a dict"
            })

        spaces_dict = data.get("spaces", {})
        if not isinstance(spaces_dict, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid spaces container: expected dict at data['spaces']"
            })

        # --- Collect active filters (keep None out; False is a valid boolean filter) ---
        filters = {
            "space_id": space_id,
            "space_key": space_key,
            "space_name": space_name,
            "space_purpose": space_purpose,
            "created_by_user_id": created_by_user_id,
            "created_at": created_at,
            "is_deleted": is_deleted,
            "deleted_at": deleted_at,
        }
        active_filters = {k: v for k, v in filters.items() if v is not None}

        # Start with all spaces (dict copy to avoid mutating original rows)
        all_spaces: List[Dict[str, Any]] = [
            s.copy() for s in spaces_dict.values()
            if isinstance(s, dict)
        ]

        # If no filters, return everything
        if not active_filters:
            return json.dumps({"success": True, "spaces": all_spaces})

        # --- Apply filters incrementally (AND logic) ---
        results = all_spaces

        # ID / FK filters (compare as string)
        if space_id is not None:
            sid = str(space_id)
            results = [s for s in results if s.get("space_id") == sid]

        if created_by_user_id is not None:
            uid = str(created_by_user_id)
            results = [s for s in results if s.get("created_by_user_id") == uid]

        # Exact string filter
        if space_key is not None:
            results = [s for s in results if s.get("space_key") == space_key]

        # Case-insensitive partial matches
        if space_name is not None:
            try:
                pat = re.compile(re.escape(space_name), re.IGNORECASE)
                results = [
                    s for s in results
                    if "space_name" in s and s["space_name"] and pat.search(s["space_name"])
                ]
            except re.error:
                return json.dumps({"success": False, "error": f"Invalid regex pattern in space_name: {space_name}"})

        if space_purpose is not None:
            try:
                pat = re.compile(re.escape(space_purpose), re.IGNORECASE)
                results = [
                    s for s in results
                    if "space_purpose" in s and s["space_purpose"] and pat.search(s["space_purpose"])
                ]
            except re.error:
                return json.dumps({"success": False, "error": f"Invalid regex pattern in space_purpose: {space_purpose}"})

        # Datetime prefix filters (e.g., "2025-10-01")
        if created_at is not None:
            results = [s for s in results if s.get("created_at", "").startswith(created_at)]

        if deleted_at is not None:
            results = [s for s in results if s.get("deleted_at", "") and s.get("deleted_at", "").startswith(deleted_at)]

        # Boolean filter (strict True/False)
        if is_deleted is not None:
            results = [s for s in results if s.get("is_deleted") is is_deleted]

        return json.dumps({"success": True, "spaces": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "fetch_space",
                "description": (
                    "Retrieve or search for spaces based on optional filters. "
                    "Returns a list of spaces; if no filters are provided, returns all spaces. "
                    "Supports partial, case-insensitive matching for 'space_name' and 'space_purpose', "
                    "exact match for 'space_key', strict boolean for 'is_deleted', "
                    "and datetime prefix matches for 'created_at'/'deleted_at'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "Exact space ID match (accepts int-like input but compared as string)."
                        },
                        "space_key": {
                            "type": "string",
                            "description": "Exact space key match (unique per space)."
                        },
                        "space_name": {
                            "type": "string",
                            "description": "Case-insensitive partial match for the space name."
                        },
                        "space_purpose": {
                            "type": "string",
                            "description": "Case-insensitive partial match for the space purpose/description."
                        },
                        "created_by_user_id": {
                            "type": "string",
                            "description": "Exact match on the creator user ID (compared as string)."
                        },
                        "created_at": {
                            "type": "string",
                            "description": "Datetime prefix match on created_at (e.g., '2025-10-01')."
                        },
                        "is_deleted": {
                            "type": "boolean",
                            "description": "Filter by deletion status (true/false)."
                        },
                        "deleted_at": {
                            "type": "string",
                            "description": "Datetime prefix match on deleted_at (e.g., '2025-10')."
                        }
                    },
                    "required": [] # No parameters are required
                }
            }
        }
