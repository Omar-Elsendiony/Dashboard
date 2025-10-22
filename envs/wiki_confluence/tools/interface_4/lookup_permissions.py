import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LookupPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, entity_id: str) -> str:
        """
        Retrieve all permissions for a space or page.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        permissions = data.get("permissions", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        
        # Validate entity_type
        if entity_type not in ["space", "page"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'space' or 'page'"
            })
        
        # Validate entity exists
        if entity_type == "space":
            if entity_id not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {entity_id} not found"
                })
        elif entity_type == "page":
            if entity_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {entity_id} not found"
                })
        
        # Find all permissions for the entity
        matching_permissions = []
        for permission_id, permission in permissions.items():
            if entity_type == "space" and permission.get("space_id") == entity_id:
                matching_permissions.append(permission.copy())
            elif entity_type == "page" and permission.get("page_id") == entity_id:
                matching_permissions.append(permission.copy())
        
        # Sort by granted_at descending
        matching_permissions.sort(key=lambda x: x.get("granted_at", ""), reverse=True)
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "count": len(matching_permissions),
            "permissions": matching_permissions
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_permissions",
                "description": "Retrieve all permissions for a space or page in the Confluence system. This tool fetches the complete list of access control permissions including permission IDs, types (view, edit, admin), grantees (users or groups), grantors, timestamps, active status, and expiration dates. Returns permissions sorted by grant date with most recent first. Essential for access control auditing, permission management, security reviews, and understanding who has access to content.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to get permissions for (required)",
                            "enum": ["space", "page"]
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "ID of the space or page (required)"
                        }
                    },
                    "required": ["entity_type", "entity_id"]
                }
            }
        }
