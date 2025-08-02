import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacesByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],  **criteria: Any) -> str:
        """
        Return all spaces that match *all* supplied non-None criteria.
        Example call:
            GetSpacesByFilters.invoke(data, name="General Documentation", status="current")
        """
        spaces = data.get("spaces", {})
        filtered_spaces = []
        # print("Criteria received:", criteria)
        
        # Remove params that aren't actual filters (defensive) and drop None values
        criteria = {
            k: v for k, v in criteria.items()
            if k not in ("data",) and v is not None  # 'data' shouldn't be passed, but guard anyway
        }
        
        # Check for empty criteria after filtering
        if not criteria:
            raise ValueError("At least one filter criterion must be provided.")

        for space in spaces.values():
            # require all provided criteria to match exactly
            if all(str(space.get(k)) == str(v) for k, v in criteria.items()):
                filtered_spaces.append(space)

        return json.dumps(filtered_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        JSON schema for the tool. All properties except none are optional;
        specify only the ones you want to filter on. Matching is exact/equality.
        """
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_filters",
                "description": (
                    "Return spaces whose fields exactly match all provided criteria. "
                    "Omit a field to ignore it."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "Space ID."
                        },
                        "key": {
                            "type": "string",
                            "description": "Short machine-friendly key/slug."
                        },
                        "name": {
                            "type": "string",
                            "description": "Human-readable space name."
                        },
                        "description": {
                            "type": "string",
                            "description": "Long description / purpose."
                        },
                        "type": {
                            "type": "string",
                            "description": "Visibility or category (e.g., 'private', 'public')."
                        },
                        "status": {
                            "type": "string",
                            "description": "Lifecycle status (e.g., 'current', 'archived')."
                        },
                        "homepage_id": {
                            "type": "integer",
                            "description": "ID of the homepage page for the space."
                        },
                        "theme": {
                            "type": ["string", "null"],
                            "description": "Theme identifier, if themed."
                        },
                        "logo_url": {
                            "type": ["string", "null"],
                            "description": "Logo URL."
                        },
                        "anonymous_access": {
                            "type": "boolean",
                            "description": "Whether anonymous users may view the space (True/False)."
                        },
                        "public_signup": {
                            "type": "boolean",
                            "description": "Whether users can self-enroll."
                        },
                        "created_at": {
                            "type": "string",
                            "description": "ISO8601 creation timestamp."
                        },
                        "updated_at": {
                            "type": "string",
                            "description": "ISO8601 last update timestamp."
                        },
                    },
                    "required": []
                },
            },
        }
