import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddressSpaces(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, space_key: Optional[str] = None,
               space_name: Optional[str] = None, created_by_user_id: Optional[str] = None,
               space_purpose: Optional[str] = None, space_id: Optional[str] = None,
               updates: Optional[Dict[str, Any]] = None, deletion_mode: Optional[str] = None) -> str:
        """
        Create, update, or delete spaces.
        
        Actions:
        - create: Create new space (requires space_key, space_name, created_by_user_id)
        - update: Update existing space (requires space_id and updates dict)
        - delete: Delete space (requires space_id and deletion_mode: 'soft_delete' or 'hard_delete')
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update", "delete"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create', 'update', or 'delete'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        if action == "create":
            # Validate required fields
            if not space_key or not space_key.strip():
                return json.dumps({
                    "success": False,
                    "error": "Space key is required and cannot be empty"
                })
            
            if not space_name or not space_name.strip():
                return json.dumps({
                    "success": False,
                    "error": "Space name is required and cannot be empty"
                })
            
            if not created_by_user_id:
                return json.dumps({
                    "success": False,
                    "error": "created_by_user_id is required"
                })
            
            # Validate user exists
            if created_by_user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {created_by_user_id} not found"
                })
            
            # Check for duplicate space key
            for existing_space in spaces.values():
                if existing_space.get("space_key") == space_key:
                    return json.dumps({
                        "success": False,
                        "error": f"Space with key '{space_key}' already exists"
                    })
            
            # Generate new space ID
            new_space_id = generate_id(spaces)
            timestamp = "2025-10-01T12:00:00"
            
            new_space = {
                "space_id": str(new_space_id),
                "space_key": space_key,
                "space_name": space_name,
                "space_purpose": space_purpose,
                "created_by_user_id": created_by_user_id,
                "created_at": timestamp,
                "is_deleted": False,
                "deleted_at": None
            }
            
            spaces[str(new_space_id)] = new_space
            
            return json.dumps({
                "success": True,
                "action": "create",
                "space_id": str(new_space_id),
                "message": f"Space created successfully with key '{space_key}'",
                "space_data": new_space
            })
        
        elif action == "update":
            if not space_id:
                return json.dumps({
                    "success": False,
                    "error": "space_id is required for update action"
                })
            
            if space_id not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {space_id} not found"
                })
            
            if not updates:
                return json.dumps({
                    "success": False,
                    "error": "updates dict is required for update action"
                })
            
            # Validate allowed update fields
            allowed_fields = ["space_name", "space_purpose", "space_key"]
            invalid_fields = [field for field in updates.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for space update: {', '.join(invalid_fields)}"
                })
            
            # Check for duplicate space key if updating
            if "space_key" in updates:
                new_key = updates["space_key"]
                for existing_space_id, existing_space in spaces.items():
                    if existing_space_id != space_id and existing_space.get("space_key") == new_key:
                        return json.dumps({
                            "success": False,
                            "error": f"Space with key '{new_key}' already exists"
                        })
            
            # Validate non-empty name if updating
            if "space_name" in updates:
                if not updates["space_name"] or not updates["space_name"].strip():
                    return json.dumps({
                        "success": False,
                        "error": "Space name cannot be empty"
                    })
            
            # Update space record
            updated_space = spaces[space_id].copy()
            for key, value in updates.items():
                updated_space[key] = value
            
            spaces[space_id] = updated_space
            
            return json.dumps({
                "success": True,
                "action": "update",
                "space_id": space_id,
                "message": f"Space {space_id} updated successfully",
                "space_data": updated_space
            })
        
        elif action == "delete":
            if not space_id:
                return json.dumps({
                    "success": False,
                    "error": "space_id is required for delete action"
                })
            
            if space_id not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {space_id} not found"
                })
            
            if not deletion_mode:
                return json.dumps({
                    "success": False,
                    "error": "deletion_mode is required for delete action"
                })
            
            if deletion_mode not in ["soft_delete", "hard_delete"]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid deletion_mode '{deletion_mode}'. Must be 'soft_delete' or 'hard_delete'"
                })
            
            if deletion_mode == "soft_delete":
                # Soft delete: mark as deleted
                timestamp = "2025-10-01T12:00:00"
                deleted_space = spaces[space_id].copy()
                deleted_space["is_deleted"] = True
                deleted_space["deleted_at"] = timestamp
                spaces[space_id] = deleted_space
                
                return json.dumps({
                    "success": True,
                    "action": "delete",
                    "deletion_mode": "soft_delete",
                    "space_id": space_id,
                    "message": f"Space {space_id} soft deleted successfully",
                    "space_data": deleted_space
                })
            else:
                # Hard delete: remove from database
                deleted_space = spaces[space_id].copy()
                del spaces[space_id]
                
                return json.dumps({
                    "success": True,
                    "action": "delete",
                    "deletion_mode": "hard_delete",
                    "space_id": space_id,
                    "message": f"Space {space_id} hard deleted successfully",
                    "space_data": deleted_space
                })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "address_spaces",
                "description": "Create, update, or delete spaces in the Confluence system. This tool manages the complete space lifecycle including creation of new content containers, updates to existing space configurations, and space deletion (both soft and hard delete). Spaces are top-level organizational units that contain pages and manage access control. Validates space key uniqueness, ensures proper user attribution, and supports both recoverable soft deletion and permanent hard deletion. Essential for organizing content, managing team workspaces, and maintaining system structure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new space, 'update' to modify existing space, 'delete' to remove space",
                            "enum": ["create", "update", "delete"]
                        },
                        "space_key": {
                            "type": "string",
                            "description": "Unique space key identifier (required for create, must be unique across all spaces)"
                        },
                        "space_name": {
                            "type": "string",
                            "description": "Human-readable space name (required for create)"
                        },
                        "created_by_user_id": {
                            "type": "string",
                            "description": "User ID of space creator (required for create)"
                        },
                        "space_purpose": {
                            "type": "string",
                            "description": "Description of space purpose (optional for create)"
                        },
                        "space_id": {
                            "type": "string",
                            "description": "Unique identifier of the space (required for update and delete actions)"
                        },
                        "updates": {
                            "type": "object",
                            "description": "Dictionary of fields to update for update action. Valid fields: space_name, space_purpose, space_key. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "space_name": {
                                    "type": "string",
                                    "description": "Updated space name (cannot be empty)"
                                },
                                "space_purpose": {
                                    "type": "string",
                                    "description": "Updated space purpose"
                                },
                                "space_key": {
                                    "type": "string",
                                    "description": "Updated space key (must be unique)"
                                }
                            }
                        },
                        "deletion_mode": {
                            "type": "string",
                            "description": "Deletion mode for delete action: 'soft_delete' marks space as deleted (recoverable), 'hard_delete' permanently removes space (required for delete action)",
                            "enum": ["soft_delete", "hard_delete"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }
