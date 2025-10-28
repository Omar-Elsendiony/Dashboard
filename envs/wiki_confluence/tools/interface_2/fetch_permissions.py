import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class FetchPermissions(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        entity_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Retrieve permissions for spaces or pages.
        If entity_id is provided, returns permissions for that specific entity.
        If omitted, returns all permissions for the entity_type across all entities.
        """
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        permissions = data.get("permissions", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})

        # Validate entity_type
        if entity_type not in ["space", "page"]:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid entity_type '{entity_type}'. "
                    "Must be 'space' or 'page'",
                }
            )

        # Validate entity exists if provided
        if entity_id is not None:
            if entity_type == "space":
                if entity_id not in spaces:
                    return json.dumps(
                        {"success": False, "error": f"Space {entity_id} not found"}
                    )
            elif entity_type == "page":
                if entity_id not in pages:
                    return json.dumps(
                        {"success": False, "error": f"Page {entity_id} not found"}
                    )

        # Determine the entity ID key for permissions
        entity_id_key = "space_id" if entity_type == "space" else "page_id"

        # Find matching permissions
        matching_permissions = []
        for permission_id, permission in permissions.items():
            # Skip if not for this entity_type
            perm_entity_id = permission.get(entity_id_key)
            if perm_entity_id is None:
                continue

            # Skip if entity_id provided but doesn't match
            if entity_id is not None and perm_entity_id != entity_id:
                continue

            # Apply filters if provided
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    perm_value = permission.get(filter_key)
                    if perm_value != filter_value:
                        match = False
                        break
                if not match:
                    continue

            matching_permissions.append(permission.copy())

        # Sort by granted_at descending
        matching_permissions.sort(
            key=lambda x: x.get("granted_at", ""), reverse=True
        )

        return json.dumps(
            {
                "success": True,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "count": len(matching_permissions),
                "permissions": matching_permissions,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_permissions",
                "description": (
                    "Retrieve permissions for spaces or pages in the Confluence system, "
                    "optionally filtered and scoped to a specific entity. Fetches access "
                    "control permissions including IDs, types (view/edit/admin), "
                    "grantees (users/groups), grantors, timestamps, status, and "
                    "expiration. Sorted by grant date (most recent first). Ideal for "
                    "auditing, management, security reviews."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": (
                                "Type of entity (required): 'space' or 'page'. "
                                "When entity_id omitted, returns ALL permissions "
                                "for this type across all entities."
                            ),
                            "enum": ["space", "page"],
                        },
                        "entity_id": {
                            "type": "string",
                            "description": (
                                "ID of specific space/page (optional). Omit for "
                                "ALL permissions of the entity_type."
                            ),
                        },
                        "filters": {
                            "type": "object",
                            "description": (
                                "Optional filters (JSON object, key-value pairs). "
                                "Single: {'key': 'value'}; Multiple: "
                                "{'key1': 'value1', 'key2': 'value2'} (AND logic). "
                                "Exact matches. Timestamps: ISO 8601. Booleans: "
                                "true/false. Fields: permission_id (str), type "
                                "('view'|'edit'|'admin'), grantee_type "
                                "('user'|'group'), grantee_id (str), grantor_id "
                                "(str), granted_at (timestamp), expires_at "
                                "(timestamp), is_active (bool)."
                            ),
                        },
                    },
                    "required": ["entity_type"],
                },
            },
        }