import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetPermissions(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        content_type: Optional[str] = None,
        content_id: Optional[str] = None,
    ) -> str:
        """
        Return all permissions of a particular user that match provided key arguments.
        If content_type and content_id are omitted, returns all permissions for the user across all content.
        Key arguments: user_id (required), content_type (optional), content_id (optional).
        """
        permissions = data.get("permissions", {})

        # Build filters dict from provided key arguments and drop None values
        filters: Dict[str, Any] = {
            "user_id": user_id,
            "content_type": content_type,
            "content_id": content_id,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        # user_id is mandatory
        if "user_id" not in filters:
            return json.dumps({"success": False, "error": "user_id is required"})

        # Validate enum values
        if "content_type" in filters:
            if str(filters["content_type"]) not in {"space", "page"}:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid content_type value: '{filters['content_type']}'. Must be one of ['space', 'page']",
                    }
                )

        # Validate referenced entities exist
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})

        if "user_id" in filters and str(filters["user_id"]) not in users:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid user_id: '{filters['user_id']}'. User not found",
                }
            )

        if "content_id" in filters:
            cid = str(filters["content_id"])
            if "content_type" in filters:
                ctype = str(filters["content_type"])
                if ctype == "space" and cid not in spaces:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"content_id '{cid}' does not reference a valid space",
                        }
                    )
                if ctype == "page" and cid not in pages:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"content_id '{cid}' does not reference a valid page",
                        }
                    )
            else:
                # If content_type not given, ensure content exists somewhere
                if cid not in spaces and cid not in pages:
                    return json.dumps(
                        {
                            "success": False,
                            "error": f"content_id '{cid}' must reference an existing space or page",
                        }
                    )

        # Direct match for provided filters
        matching_permissions = []
        for perm in permissions.values():
            if all(str(perm.get(k)) == str(v) for k, v in filters.items()):
                matching_permissions.append(perm)

        # Cascade: if requesting a page's permissions and none found, fall back to space permissions
        pages = data.get("pages", {})

        is_page_request = (
            ("content_type" in filters and str(filters["content_type"]) == "page")
            or ("content_type" not in filters and "content_id" in filters and str(filters["content_id"]) in pages)
        )

        if (
            is_page_request
            and len(matching_permissions) == 0
            and "user_id" in filters
            and "content_id" in filters
        ):
            page_id_for_lookup = str(filters["content_id"])
            page_row = pages.get(page_id_for_lookup)
            if page_row is not None:
                space_id = str(page_row.get("space_id"))
                fallback_user = str(filters["user_id"])
                matching_permissions = [
                    perm
                    for perm in permissions.values()
                    if str(perm.get("user_id")) == fallback_user
                    and str(perm.get("content_type")) == "space"
                    and str(perm.get("content_id")) == space_id
                ]
        return json.dumps(
            {
                "success": True,
                "count": len(matching_permissions),
                "permissions": matching_permissions,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_permissions",
                "description": (
                    "Return permissions for a user and optional content filters. "
                    "user_id is required; content_type and content_id are optional."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content_id": {
                            "type": "string",
                            "description": "Associated content identifier",
                        },
                        "content_type": {
                            "type": "string",
                            "description": "Type of content: 'space' or 'page'",
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User identifier who holds the permission",
                        },
                    },
                    "required": ["user_id"],
                },
            },
        }
