import json
from typing import Any, Dict, List, Set
from tau_bench.envs.tool import Tool


class AccessDescendants(Tool):
    """
    Retrieve all descendant pages of a given page.
    - Returns all pages that are descendants (children, grandchildren, etc.) of the specified page.
    - Traverses the page hierarchy recursively.
    - Returns an empty list if the page has no descendants.
    - Returns an error if the page doesn't exist.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
    ) -> str:
        """
        Return a JSON string:
          {"success": True, "descendants": [...]} on success
          {"success": False, "error": "..."} on error
        """

        def get_descendants_recursive(
            pages_dict: Dict[str, Any], page_id: str, visited: Set[str]
        ) -> List[Dict[str, Any]]:
            descendants = []

            # Find all direct children (pages where parent_page_id == page_id)
            for page_key, page in pages_dict.items():
                if not isinstance(page, dict):
                    continue

                parent_id = page.get("parent_page_id")

                # Check if this page is a direct child
                if parent_id is not None and str(parent_id) == str(page_id):
                    child_id = page.get("page_id")

                    # Prevent infinite loops in case of circular references
                    if child_id and str(child_id) in visited:
                        continue

                    page_copy = page.copy()
                    descendants.append(page_copy)

                    # Mark this child as visited and recursively find its descendants
                    if child_id:
                        child_id_str = str(child_id)
                        visited.add(child_id_str)
                        child_descendants = get_descendants_recursive(
                            pages_dict, child_id_str, visited
                        )
                        descendants.extend(child_descendants)

            return descendants

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
            return json.dumps(
                {
                    "success": False,
                    "error": f"Page with ID '{page_id_str}' not found",
                }
            )

        # Get all descendants recursively
        visited = set()
        descendants = get_descendants_recursive(pages_dict, page_id_str, visited)

        return json.dumps({"success": True, "descendants": descendants})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Tool schema for function-calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "access_descendants",
                "description": (
                    "Retrieve all descendant pages of a given page. "
                    "Returns all pages that are descendants (children, grandchildren, etc.) "
                    "of the specified page by traversing the page hierarchy recursively. "
                    "Returns an empty list if the page has no descendants. "
                    "Returns an error if the page doesn't exist."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The page ID to find descendants for (accepts int-like input but compared as string).",
                        }
                    },
                    "required": ["page_id"],
                },
            },
        }
