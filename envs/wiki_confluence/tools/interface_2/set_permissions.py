import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SetPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, permission_type: str,
               granted_by_user_id: str, entity_type: Optional[str] = None,
               entity_id: Optional[str] = None, grantee_type: Optional[str] = None,
               grantee_id: Optional[str] = None, permission_id: Optional[str] = None,
               expires_at: Optional[str] = None) -> str:
        """
        Grant or revoke permissions.
        
        Actions:
        - grant: Grant permission (requires entity_type, entity_id, grantee_type, grantee_id, permission_type, granted_by_user_id)
        - revoke: Revoke permission (requires permission_id, granted_by_user_id as revoked_by_user_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["grant", "revoke"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'grant' or 'revoke'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        permissions = data.get("permissions", {})
        users = data.get("users", {})
        groups = data.get("groups", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        
        # Validate user exists
        if granted_by_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {granted_by_user_id} not found"
            })
        
        if action == "grant":
            # Validate required fields
            if not entity_type:
                return json.dumps({
                    "success": False,
                    "error": "entity_type is required for grant action"
                })
            
            if not entity_id:
                return json.dumps({
                    "success": False,
                    "error": "entity_id is required for grant action"
                })
            
            if not grantee_type:
                return json.dumps({
                    "success": False,
                    "error": "grantee_type is required for grant action"
                })
            
            if not grantee_id:
                return json.dumps({
                    "success": False,
                    "error": "grantee_id is required for grant action"
                })
            
            # Validate entity_type
            if entity_type not in ["space", "page"]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid entity_type '{entity_type}'. Must be 'space' or 'page'"
                })
            
            # Validate grantee_type
            if grantee_type not in ["user", "group"]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid grantee_type '{grantee_type}'. Must be 'user' or 'group'"
                })
            
            # Validate permission_type enum
            valid_permissions = ["view", "edit", "admin"]
            if permission_type not in valid_permissions:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid permission_type. Must be one of: {', '.join(valid_permissions)}"
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
            
            # Validate grantee exists
            if grantee_type == "user":
                if grantee_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User {grantee_id} not found"
                    })
            elif grantee_type == "group":
                if grantee_id not in groups:
                    return json.dumps({
                        "success": False,
                        "error": f"Group {grantee_id} not found"
                    })
            
            # Check for duplicate permission
            for perm_id, perm in permissions.items():
                if perm.get("is_active", True):
                    matches_entity = (
                        (entity_type == "space" and perm.get("space_id") == entity_id) or
                        (entity_type == "page" and perm.get("page_id") == entity_id)
                    )
                    matches_grantee = (
                        (grantee_type == "user" and perm.get("user_id") == grantee_id) or
                        (grantee_type == "group" and perm.get("group_id") == grantee_id)
                    )
                    if matches_entity and matches_grantee and perm.get("permission_type") == permission_type:
                        return json.dumps({
                            "success": False,
                            "error": f"Permission already exists for {grantee_type} {grantee_id} on {entity_type} {entity_id}"
                        })
            
            # Generate new permission ID
            new_permission_id = generate_id(permissions)
            timestamp = "2025-10-01T12:00:00"
            
            new_permission = {
                "permission_id": str(new_permission_id),
                "space_id": entity_id if entity_type == "space" else None,
                "page_id": entity_id if entity_type == "page" else None,
                "user_id": grantee_id if grantee_type == "user" else None,
                "group_id": grantee_id if grantee_type == "group" else None,
                "permission_type": permission_type,
                "granted_by_user_id": granted_by_user_id,
                "granted_at": timestamp,
                "is_active": True,
                "revoked_by_user_id": None,
                "revoked_at": None,
                "expires_at": expires_at
            }
            
            permissions[str(new_permission_id)] = new_permission
            
            return json.dumps({
                "success": True,
                "action": "grant",
                "permission_id": str(new_permission_id),
                "message": f"Permission '{permission_type}' granted to {grantee_type} {grantee_id} on {entity_type} {entity_id}",
                "permission_data": new_permission
            })
        
        elif action == "revoke":
            if not permission_id:
                return json.dumps({
                    "success": False,
                    "error": "permission_id is required for revoke action"
                })
            
            if permission_id not in permissions:
                return json.dumps({
                    "success": False,
                    "error": f"Permission {permission_id} not found"
                })
            
            timestamp = "2025-10-01T12:00:00"
            revoked_permission = permissions[permission_id].copy()
            revoked_permission["is_active"] = False
            revoked_permission["revoked_by_user_id"] = granted_by_user_id
            revoked_permission["revoked_at"] = timestamp
            
            permissions[permission_id] = revoked_permission
            
            return json.dumps({
                "success": True,
                "action": "revoke",
                "permission_id": permission_id,
                "message": f"Permission {permission_id} revoked successfully",
                "permission_data": revoked_permission
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "set_permissions",
                "description": "Grant or revoke permissions in the Confluence system. This tool manages access control by granting specific permission levels (view, edit, admin) to users or groups on spaces or pages, and revoking existing permissions. Validates entity existence, prevents duplicate permissions, and maintains complete permission audit trails with grantor attribution. Supports optional expiration dates for temporary access. Essential for access control, security management, collaborative workflows, and compliance with authorization policies.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'grant' to assign permission, 'revoke' to remove permission",
                            "enum": ["grant", "revoke"]
                        },
                        "permission_type": {
                            "type": "string",
                            "description": "Type of permission (required)",
                            "enum": ["view", "edit", "admin"]
                        },
                        "granted_by_user_id": {
                            "type": "string",
                            "description": "User ID granting the permission (for grant) or revoking the permission (for revoke) (required)"
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to grant permission on (required for grant action)",
                            "enum": ["space", "page"]
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "ID of the space or page (required for grant action)"
                        },
                        "grantee_type": {
                            "type": "string",
                            "description": "Type of grantee receiving permission (required for grant action)",
                            "enum": ["user", "group"]
                        },
                        "grantee_id": {
                            "type": "string",
                            "description": "ID of the user or group receiving permission (required for grant action)"
                        },
                        "permission_id": {
                            "type": "string",
                            "description": "ID of permission to revoke (required for revoke action)"
                        },
                        "expires_at": {
                            "type": "string",
                            "description": "Expiration timestamp for temporary permissions (optional, format: YYYY-MM-DDTHH:MM:SS)"
                        }
                    },
                    "required": ["action", "permission_type", "granted_by_user_id"]
                }
            }
        }
