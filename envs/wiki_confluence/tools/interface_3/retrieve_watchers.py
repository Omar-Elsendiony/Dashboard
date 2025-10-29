import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class RetrieveWatchers(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        group_id: Optional[str] = None,
        space_id: Optional[str] = None,
        page_id: Optional[str] = None
    ) -> str:
        """
        Retrieve all watchers, optionally filtered by user_id, group_id, space_id, page_id.
        Supports flexible filtering with any combination of the four identifier parameters.
        """
        # Input validation
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        watchers_raw = data.get("watchers", {})

        # Normalize watchers to a list of watcher dicts with validation
        if isinstance(watchers_raw, dict):
            watchers_list: List[Dict[str, Any]] = [
                watcher for watcher in watchers_raw.values()
                if isinstance(watcher, dict)
            ]
        elif isinstance(watchers_raw, list):
            watchers_list = [
                watcher for watcher in watchers_raw
                if isinstance(watcher, dict)
            ]
        else:
            return json.dumps({"success": False, "error": "Invalid watchers format"})

        # Build filters dictionary efficiently
        filters = {
            k: v for k, v in {
                "user_id": user_id,
                "group_id": group_id,
                "space_id": space_id,
                "page_id": page_id
            }.items() if v is not None
        }

        # Early return if no filters
        if not filters:
            return json.dumps({
                "success": True,
                "count": len(watchers_list),
                "watchers": watchers_list
            })

        # Optimized filtering using list comprehension
        matching_watchers = [
            watcher for watcher in watchers_list
            if all(watcher.get(key) == value for key, value in filters.items())
        ]

        return json.dumps({
            "success": True,
            "count": len(matching_watchers),
            "watchers": matching_watchers
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_watchers",
                "description": "Retrieve all watchers from the Confluence system with optional filtering. This tool fetches watchers and allows filtering by any combination of user_id, group_id, space_id, and page_id. Returns watcher details including watcher IDs, types (user or group), and subscription information. Essential for notification management, understanding content subscribers, and managing watch lists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Filter watchers by specific user ID (optional)"
                        },
                        "group_id": {
                            "type": "string",
                            "description": "Filter watchers by specific group ID (optional)"
                        },
                        "space_id": {
                            "type": "string",
                            "description": "Filter watchers by specific space ID (optional)"
                        },
                        "page_id": {
                            "type": "string",
                            "description": "Filter watchers by specific page ID (optional)"
                        }
                    },
                    "required": []
                }
            }
        }
