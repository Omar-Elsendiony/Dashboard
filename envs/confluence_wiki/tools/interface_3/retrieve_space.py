import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class RetrieveSpace(Tool):
    """
    Retrieve or search for spaces with flexible filters.
    - Returns ALL spaces when no filters are provided.
    - Applies all provided filters using AND logic.
    - Safe handling of ID comparisons (cast to str), enums, and datetime prefix matches.
    - Case-insensitive partial matching for name and description.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        space_id: Optional[str] = None,
        space_key: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "spaces": [...]} on success
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

        spaces_dict = data.get("spaces", {})
        if not isinstance(spaces_dict, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid spaces container: expected dict at data['spaces']",
                }
            )

        # --- Validate enum values if provided ---
        valid_types = ["global", "personal"]
        valid_statuses = ["current", "archived"]

        if type is not None and type not in valid_types:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid type value: '{type}'. Must be one of {valid_types}",
                }
            )

        if status is not None and status not in valid_statuses:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid status value: '{status}'. Must be one of {valid_statuses}",
                }
            )

        # --- Collect active filters (keep None out) ---
        filters = {
            "space_id": space_id,
            "space_key": space_key,
            "name": name,
            "description": description,
            "type": type,
            "status": status,
            "created_by": created_by,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        active_filters = {k: v for k, v in filters.items() if v is not None}

        # Start with all spaces (dict copy to avoid mutating original rows)
        all_spaces: List[Dict[str, Any]] = [
            s.copy() for s in spaces_dict.values() if isinstance(s, dict)
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

        if created_by is not None:
            uid = str(created_by)
            results = [s for s in results if s.get("created_by") == uid]

        # Exact string filters
        if space_key is not None:
            results = [s for s in results if s.get("space_key") == space_key]

        if type is not None:
            results = [s for s in results if s.get("type") == type]

        if status is not None:
            results = [s for s in results if s.get("status") == status]

        # Case-insensitive partial matches
        if name is not None:
            try:
                pat = re.compile(re.escape(name), re.IGNORECASE)
                results = [
                    s
                    for s in results
                    if "name" in s and s["name"] and pat.search(s["name"])
                ]
            except re.error:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid regex pattern in name: {name}",
                    }
                )

        if description is not None:
            try:
                pat = re.compile(re.escape(description), re.IGNORECASE)
                results = [
                    s
                    for s in results
                    if "description" in s
                    and s["description"]
                    and pat.search(s["description"])
                ]
            except re.error:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid regex pattern in description: {description}",
                    }
                )

        # Datetime prefix filters (e.g., "2025-10-01")
        if created_at is not None:
            results = [
                s for s in results if s.get("created_at", "").startswith(created_at)
            ]

        if updated_at is not None:
            results = [
                s for s in results if s.get("updated_at", "").startswith(updated_at)
            ]

        return json.dumps({"success": True, "spaces": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "retrieve_space",
                "description": (
                    "Retrieves spaces from the Wiki system based on search criteria. "
                    "A space is a container for organizing wiki pages and content. "
                    "When called with no parameters, returns all spaces in the system. "
                    "When called with parameters, filters and returns only matching spaces. "
                    "You can combine multiple filters to narrow down results. "
                    "All filters support AND logic (all conditions must match)."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "The unique identifier for a specific space. Performs exact match. Example: '12345' or 'sp_67890'. Use this when you know the exact space ID.",
                        },
                        "space_key": {
                            "type": "string",
                            "description": "The unique key/code for a space. Performs exact match (case-sensitive). Example: 'ENG' for Engineering space or 'DOCS' for Documentation space. Use this for human-readable space identifiers.",
                        },
                        "name": {
                            "type": "string",
                            "description": "Searches within space names. Performs partial, case-insensitive matching. Example: searching 'engineer' will match 'Engineering Team', 'Software Engineering', etc.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Searches within space descriptions. Performs partial, case-insensitive matching. Example: searching 'project' will match any space description containing that word.",
                        },
                        "type": {
                            "type": "string",
                            "description": "Filters by space type. The accepted values are 'global' and 'personal'. 'global' = shared team/organization spaces accessible by multiple users. 'personal' = individual user spaces. Performs exact match.",
                        },
                        "status": {
                            "type": "string",
                            "description": "Filters by space status. The accepted values are 'current' and 'archived'. 'current' = active spaces in use. 'archived' = spaces that have been archived/deprecated. Performs exact match.",
                        },
                        "created_by": {
                            "type": "string",
                            "description": "Filters spaces by their creator's user ID. Performs exact match. Example: 'usr_12345'. Use this to find all spaces created by a specific user.",
                        },
                        "created_at": {
                            "type": "string",
                            "description": "Filters spaces by creation date/time. Performs prefix matching on ISO datetime format",
                        },
                        "updated_at": {
                            "type": "string",
                            "description": "Filters spaces by last update date/time. Performs prefix matching on ISO datetime format",
                        },
                    },
                    "required": [],
                },
            },
        }
