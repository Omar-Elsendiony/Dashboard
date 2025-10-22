import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, email: Optional[str] = None,
               full_name: Optional[str] = None, global_role: Optional[str] = None,
               user_id: Optional[str] = None, account_id: Optional[str] = None,
               updates: Optional[Dict[str, Any]] = None) -> str:
        """
        Create, update, or delete user accounts.
        
        Actions:
        - create: Create new user (requires email, full_name, global_role)
        - update: Update existing user (requires user_id and updates dict)
        - delete: Delete user (requires user_id)
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
        
        users = data.get("users", {})
        
        if action == "create":
            # Validate required fields
            if not email or not email.strip():
                return json.dumps({
                    "success": False,
                    "error": "Email is required and cannot be empty"
                })
            
            if not full_name or not full_name.strip():
                return json.dumps({
                    "success": False,
                    "error": "Full name is required and cannot be empty"
                })
            
            if not global_role:
                return json.dumps({
                    "success": False,
                    "error": "Global role is required"
                })
            
            # Validate global_role enum
            valid_roles = ["global_admin", "space_admin", "space_member", "anonymous", 
                          "reviewer_approver", "guest", "project_team_admin", "content_contributor"]
            if global_role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid global_role. Must be one of: {', '.join(valid_roles)}"
                })
            
            # Check for duplicate email
            for existing_user in users.values():
                if existing_user.get("email") == email:
                    return json.dumps({
                        "success": False,
                        "error": f"User with email '{email}' already exists"
                    })
            
            # Generate new user ID
            new_user_id = generate_id(users)
            timestamp = "2025-10-01T12:00:00"
            
            new_user = {
                "user_id": str(new_user_id),
                "email": email,
                "account_id": account_id,
                "full_name": full_name,
                "global_role": global_role,
                "created_at": timestamp
            }
            
            users[str(new_user_id)] = new_user
            
            return json.dumps({
                "success": True,
                "action": "create",
                "user_id": str(new_user_id),
                "message": f"User created successfully with email '{email}'",
                "user_data": new_user
            })
        
        elif action == "update":
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "user_id is required for update action"
                })
            
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} not found"
                })
            
            if not updates:
                return json.dumps({
                    "success": False,
                    "error": "updates dict is required for update action"
                })
            
            # Validate allowed update fields
            allowed_fields = ["email", "full_name", "global_role", "account_id"]
            invalid_fields = [field for field in updates.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for user update: {', '.join(invalid_fields)}"
                })
            
            # Validate global_role if being updated
            if "global_role" in updates:
                valid_roles = ["global_admin", "space_admin", "space_member", "anonymous",
                              "reviewer_approver", "guest", "project_team_admin", "content_contributor"]
                if updates["global_role"] not in valid_roles:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid global_role. Must be one of: {', '.join(valid_roles)}"
                    })
            
            # Check for duplicate email if updating email
            if "email" in updates:
                new_email = updates["email"]
                for existing_user_id, existing_user in users.items():
                    if existing_user_id != user_id and existing_user.get("email") == new_email:
                        return json.dumps({
                            "success": False,
                            "error": f"User with email '{new_email}' already exists"
                        })
            
            # Update user record
            updated_user = users[user_id].copy()
            for key, value in updates.items():
                updated_user[key] = value
            
            users[user_id] = updated_user
            
            return json.dumps({
                "success": True,
                "action": "update",
                "user_id": user_id,
                "message": f"User {user_id} updated successfully",
                "user_data": updated_user
            })
        
        elif action == "delete":
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "user_id is required for delete action"
                })
            
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} not found"
                })
            
            deleted_user = users[user_id].copy()
            del users[user_id]
            
            return json.dumps({
                "success": True,
                "action": "delete",
                "user_id": user_id,
                "message": f"User {user_id} deleted successfully",
                "user_data": deleted_user
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_users",
                "description": "Create, update, or delete user accounts in the Confluence system. This tool manages the complete user lifecycle including creation of new user accounts with validation, updates to existing user profiles, and user account deletion. For creation, establishes new user records with email uniqueness validation and role assignment. For updates, modifies user attributes while maintaining email uniqueness. For deletion, permanently removes user accounts from the system. Validates user roles and ensures data integrity across all operations. Essential for user administration, access control, and system security management.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new user account, 'update' to modify existing user record, 'delete' to remove user account",
                            "enum": ["create", "update", "delete"]
                        },
                        "email": {
                            "type": "string",
                            "description": "User email address (required for create, must be unique across all users)"
                        },
                        "full_name": {
                            "type": "string",
                            "description": "User's full name (required for create)"
                        },
                        "global_role": {
                            "type": "string",
                            "description": "User's global role (required for create)",
                            "enum": ["global_admin", "space_admin", "space_member", "anonymous", "reviewer_approver", "guest", "project_team_admin", "content_contributor"]
                        },
                        "account_id": {
                            "type": "string",
                            "description": "External account identifier (optional for create/update)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user (required for update and delete actions)"
                        },
                        "updates": {
                            "type": "object",
                            "description": "Dictionary of fields to update for update action. Valid fields: email, full_name, global_role, account_id. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "description": "New email address (must be unique)"
                                },
                                "full_name": {
                                    "type": "string",
                                    "description": "Updated full name"
                                },
                                "global_role": {
                                    "type": "string",
                                    "description": "Updated global role",
                                    "enum": ["global_admin", "space_admin", "space_member", "anonymous", "reviewer_approver", "guest", "project_team_admin", "content_contributor"]
                                },
                                "account_id": {
                                    "type": "string",
                                    "description": "Updated account identifier"
                                }
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }
