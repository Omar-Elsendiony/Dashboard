import json
from typing import Any, Dict, List, Set
from tau_bench.envs.tool import Tool


class AccessAncestors(Tool):
    """
    Retrieve all ancestor pages of a given page.
    - Returns all pages that are ancestors (parent, grandparent, etc.) of the specified page.
    - Traverses the page hierarchy upward recursively.
    - Returns an empty list if the page has no ancestors.
    - Returns an error if the page doesn't exist.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "ancestors": [...]} on success
          {"success": False, "error": "..."} on error
        """

        def get_ancestors_recursive(
            pages_dict: Dict[str, Any], page_id: str, visited: Set[str]
        ) -> List[Dict[str, Any]]:
            ancestors = []

            # Prevent infinite loops in case of circular references
            if page_id in visited:
                return ancestors

            visited.add(page_id)

            # Get the current page
            current_page = pages_dict.get(page_id)
            if not isinstance(current_page, dict):
                return ancestors

            # Get the parent_page_id
            parent_id = current_page.get("parent_page_id")

            # If there's a parent, add it to ancestors and recurse
            if parent_id is not None:
                parent_id_str = str(parent_id)

                # Check if parent exists in pages_dict
                if parent_id_str in pages_dict:
                    parent_page = pages_dict[parent_id_str]
                    if isinstance(parent_page, dict):
                        parent_copy = parent_page.copy()
                        ancestors.append(parent_copy)

                        # Recursively find ancestors of the parent
                        parent_ancestors = get_ancestors_recursive(
                            pages_dict, parent_id_str, visited
                        )
                        ancestors.extend(parent_ancestors)

            return ancestors

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

        # Validate page_id is provided
        if page_id is None:
            return json.dumps({"success": False, "error": "page_id is required"})

        # Convert page_id to string for consistent comparison
        page_id_str = str(page_id)

        # Check if the page exists
        if page_id_str not in pages_dict:
            # Page doesn't exist return an error
            return json.dumps(
                {
                    "success": False,
                    "error": f"Page with ID '{page_id_str}' not found",
                }
            )

        # Get all ancestors recursively
        visited = set()
        ancestors = get_ancestors_recursive(pages_dict, page_id_str, visited)

        return json.dumps({"success": True, "ancestors": ancestors})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "access_ancestors",
                "description": (
                    "Retrieve all ancestor pages of a given page. "
                    "Returns all pages that are ancestors (parent, grandparent, etc.) "
                    "of the specified page by traversing the page hierarchy upward recursively. "
                    "Returns an empty list if the page has no ancestors or if the page doesn't exist."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The page ID to find ancestors for (accepts int-like input but compared as string).",
                        }
                    },
                    "required": ["page_id"],
                },
            },
        }
