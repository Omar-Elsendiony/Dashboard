import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class FetchDirectChildren(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Return the direct child pages of the given page_id.
        Children are pages whose 'parent_page_id' equals the given 'page_id'.

        Optional filters (ANDed):
        - title: exact match on page title
        - status: one of ['current','draft','locked','archived','deleted']
        - space_id: must reference an existing space
        """
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})

        if str(page_id) not in pages:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Page not found: '{page_id}'",
                }
            )

        # Build and validate filters
        filters = filters or {}
        allowed_keys = {"title", "status", "space_id"}
        provided_keys = set(filters.keys())

        # Reject unexpected filter keys
        unexpected = [k for k in provided_keys if k not in allowed_keys]
        if unexpected:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Unsupported filter(s) provided: {', '.join(unexpected)}",
                }
            )

        # Drop filters with None values
        filters = {k: v for k, v in filters.items() if v is not None}

        # Validate individual filter values
        if "status" in filters:
            valid_statuses = {"current", "draft", "locked", "archived", "deleted"}
            if str(filters["status"]) not in valid_statuses:
                return json.dumps(
                    {
                        "success": False,
                        "error": (
                            f"Invalid status value: '{filters['status']}'. "
                            f"Must be one of {sorted(list(valid_statuses))}"
                        ),
                    }
                )

        if "space_id" in filters:
            if str(filters["space_id"]) not in spaces:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid space_id: '{filters['space_id']}'. Space not found",
                    }
                )

        if "title" in filters and not isinstance(filters["title"], str):
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid title: must be a string",
                }
            )

        # Gather direct children first
        children = []
        for _, page in pages.items():
            if str(page.get("parent_page_id")) == str(page_id):
                children.append(page)

        # Apply AND of filters
        if filters:

            def matches(p: Dict[str, Any]) -> bool:
                for k, v in filters.items():
                    if str(p.get(k)) != str(v):
                        return False
                return True

            children = [p for p in children if matches(p)]

        return json.dumps(
            {
                "success": True,
                "page_id": str(page_id),
                "count": len(children),
                "children": children,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_direct_children",
                "description": "Get direct child pages of a page by page_id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the parent page",
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters applied with AND",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Exact page title",
                                },
                                "status": {
                                    "type": "string",
                                    "description": "One of: current, draft, locked, archived, deleted",
                                },
                                "space_id": {
                                    "type": "string",
                                    "description": "Space ID; must exist",
                                },
                            },
                            "required": [],
                        },
                    },
                    "required": ["page_id"],
                },
            },
        }
