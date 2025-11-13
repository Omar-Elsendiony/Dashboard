import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class LookupPermissions(Tool):
    @staticmethod
    def invoke(
    data: Dict[str, Any],
    user_id: str,
    content_type: str,
    content_id: str,
    ) -> str:
        """Return permissions for a user on a specific space or page.
        For pages, this includes both direct permissions (explicitly granted on the page itself) 
        and inherited permissions (cascaded from parent pages up the hierarchy and from the containing space). 
        Permissions flow down from parent to child pages automatically."""
        permissions = data.get("permissions", {})

        # Build filters dict from provided key arguments and drop None values
        filters: Dict[str, Any] = {
            "user_id": user_id,
            "content_type": content_type,
            "content_id": content_id,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        # Required fields: user_id, content_type, content_id
        if "user_id" not in filters or str(filters["user_id"]) == "":
            return json.dumps({"success": False, "error": "user_id is required"})
        if "content_type" not in filters or str(filters["content_type"]) == "":
            return json.dumps({"success": False, "error": "content_type is required"})
        if "content_id" not in filters or str(filters["content_id"]) == "":
            return json.dumps({"success": False, "error": "content_id is required"})

        # Validate enum values
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

        # Cascade: traverse up the page hierarchy to find inherited permissions
        is_page_request = (str(filters["content_type"]) == "page")

        if (
            is_page_request
            and "user_id" in filters
            and "content_id" in filters
        ):
            page_id = str(filters["content_id"])
            fallback_user = str(filters["user_id"])
            
            # Helper function to get ancestors
            def get_ancestors(page_id: str) -> list:
                """Returns list of ancestor IDs: [parent_page_id, grandparent_page_id, ..., space_id]"""
                ancestors = []
                current_page_id = page_id
                visited = set()  # Prevent infinite loops
                
                while current_page_id and current_page_id not in visited:
                    visited.add(current_page_id)
                    page_data = pages.get(current_page_id)
                    
                    if not page_data:
                        break
                    
                    parent_page_id = page_data.get("parent_page_id")
                    
                    # If there's a parent page, add it to ancestors
                    if parent_page_id:
                        ancestors.append(("page", str(parent_page_id)))
                        current_page_id = str(parent_page_id)
                    else:
                        # No parent page, so add the space and stop
                        space_id = page_data.get("space_id")
                        if space_id:
                            ancestors.append(("space", str(space_id)))
                        break
                
                return ancestors
            
            # Get all ancestors
            ancestors = get_ancestors(page_id)
            
            # Check permissions for each ancestor in order
            for content_type, content_id in ancestors:
                inherited_perms = [
                    perm
                    for perm in permissions.values()
                    if str(perm.get("user_id")) == fallback_user
                    and str(perm.get("content_type")) == content_type
                    and str(perm.get("content_id")) == content_id
                ]
                matching_permissions.extend(inherited_perms)
        
        # Dedupe by operation only and return minimal fields (operation, user_id)
        seen_ops = set()
        perms_out = []
        for perm in matching_permissions:
            op = str(perm.get("operation"))
            if op not in seen_ops:
                seen_ops.add(op)
                perms_out.append({"operation": op, "user_id": str(filters["user_id"])})

        return json.dumps({"success": True, "count": len(perms_out), "permissions": perms_out})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_permissions",
                "description": (
                    "Return permissions for a user on a specific space or page. "
                    "For pages, this includes both direct permissions (explicitly granted on the page itself) "
                    "and inherited permissions (cascaded from parent pages up the hierarchy and from the containing space). "
                    "Permissions flow down from parent to child pages automatically."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content_id": {
                            "type": "string",
                            "description": "Associated content identifier: 'space_id' or 'page_id'",
                        },
                        "content_type": {
                            "type": "string",
                            "description": "Type of content we want to check the permissions on: 'space' or 'page'",
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User identifier who holds the permission",
                        },
                    },
                    "required": ["user_id", "content_id", "content_type"],
                },
            },
        }
