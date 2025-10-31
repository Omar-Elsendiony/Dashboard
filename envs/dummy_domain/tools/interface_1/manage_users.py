import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageUsers(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        user_data: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> str:
        """
        Create or update user records.
        
        Actions:
        - create: Create new user record (requires user_data with first_name, last_name, email, role, timezone)
        - update: Update existing user record (requires user_id and user_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        timestamp = "2025-10-07T12:00:00"
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        users = data.get("users", {})
        clients = data.get("clients", {})
        
        if action == "create":
            if not user_data:
                return json.dumps({
                    "success": False,
                    "error": "user_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["first_name", "last_name", "email", "role", "timezone"]
            missing_fields = [field for field in required_fields if field not in user_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not user_data[field] or str(user_data[field]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
            
            # Validate allowed fields
            allowed_fields = ["first_name", "last_name", "email", "role", "timezone", "status", "client_id"]
            invalid_fields = [field for field in user_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields: {', '.join(invalid_fields)}"
                })
            
            # Validate role enum
            valid_roles = ["incident_manager", "technical_support", "account_manager", "executive", "system_administrator", "client_contact"]
            if user_data["role"] not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid role '{user_data['role']}'. Must be one of: {', '.join(valid_roles)}"
                })
            
            # Validate status enum if provided (schema only has 'active' and 'inactive')
            if "status" in user_data:
                if user_data["status"] is not None and str(user_data["status"]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": "Field 'status' cannot be empty if provided"
                    })
                valid_status = ["active", "inactive"]
                if user_data["status"] not in valid_status:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{user_data['status']}'. Must be one of: {', '.join(valid_status)}"
                    })
            
            # Check email uniqueness
            for user in users.values():
                if user.get("email") == user_data["email"]:
                    return json.dumps({
                        "success": False,
                        "error": "Email already exists"
                    })
            
            # Validate client_id if role is client_contact
            if user_data["role"] == "client_contact":
                if "client_id" not in user_data:
                    return json.dumps({
                        "success": False,
                        "error": "client_id is required for client_contact role"
                    })
                if not user_data["client_id"] or str(user_data["client_id"]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": "Field 'client_id' cannot be empty"
                    })
                if str(user_data["client_id"]) not in clients:
                    return json.dumps({
                        "success": False,
                        "error": "Client not found"
                    })
            
            # Validate optional fields are not empty if provided
            if "client_id" in user_data and user_data["client_id"] is not None:
                if str(user_data["client_id"]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": "Field 'client_id' cannot be empty if provided"
                    })
            
            # Create new user
            new_id = str(generate_id(users))
            new_user = {
                "user_id": new_id,
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "role": user_data["role"],
                "timezone": user_data["timezone"],
                "status": user_data.get("status", "active"),
                "client_id": str(user_data["client_id"]) if user_data.get("client_id") not in (None, "") else None,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            users[new_id] = new_user
            
            return json.dumps({
                "success": True,
                "action": "create",
                "user_id": new_id,
                "user_data": new_user
            })
        
        elif action == "update":
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "user_id is required for update action"
                })
            
            if str(user_id) not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} not found"
                })
            
            if not user_data:
                return json.dumps({
                    "success": False,
                    "error": "user_data is required for update action"
                })
            
            # Validate allowed fields
            allowed_fields = ["first_name", "last_name", "email", "role", "timezone", "status", "client_id"]
            invalid_fields = [field for field in user_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields
            for field, value in user_data.items():
                if field in ["client_id", "status"] and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty if provided"
                    })
                elif field not in ["client_id", "status"] and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
            
            # Validate role enum if provided
            if "role" in user_data:
                valid_roles = ["incident_manager", "technical_support", "account_manager", "executive", "system_administrator", "client_contact"]
                if user_data["role"] not in valid_roles:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                    })
            
            # Validate status enum if provided (schema only has 'active' and 'inactive')
            if "status" in user_data:
                valid_status = ["active", "inactive"]
                if user_data["status"] not in valid_status:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_status)}"
                    })
            
            # Check email uniqueness if being updated
            if "email" in user_data:
                for uid, user in users.items():
                    if uid != str(user_id) and user.get("email") == user_data["email"]:
                        return json.dumps({
                            "success": False,
                            "error": "New email already exists"
                        })
            
            # Get current user to check role
            current_user = users[str(user_id)]
            current_role = user_data.get("role", current_user.get("role"))
            
            # Validate client_id if role is client_contact
            if current_role == "client_contact" and "client_id" in user_data:
                if user_data["client_id"] and str(user_data["client_id"]) not in clients:
                    return json.dumps({
                        "success": False,
                        "error": "Client not found"
                    })
            
            # Update user
            updated_user = users[str(user_id)].copy()
            for key, value in user_data.items():
                if key == "client_id" and value:
                    updated_user[key] = str(value)
                elif key == "client_id" and value in (None, ""):
                    updated_user[key] = None
                else:
                    updated_user[key] = value
            updated_user["updated_at"] = timestamp
            users[str(user_id)] = updated_user
            
            return json.dumps({
                "success": True,
                "action": "update",
                "user_id": str(user_id),
                "user_data": updated_user
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_users",
                "description": "Create or update user records in the incident management system. Manages user lifecycle including role-based access control, client associations, and status management. Validates user roles, email uniqueness, and enforces role-specific requirements for client contacts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new user record, 'update' to modify existing user record"
                        },
                        "user_data": {
                            "type": "object",
                            "description": "User data object containing fields for creating or updating users",
                            "properties": {
                                "first_name": {
                                    "type": "string",
                                    "description": "User's first name (required for create, cannot be empty)"
                                },
                                "last_name": {
                                    "type": "string",
                                    "description": "User's last name (required for create, cannot be empty)"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "User's email address (required for create, cannot be empty, must be unique across all users)"
                                },
                                "role": {
                                    "type": "string",
                                    "description": "User's role in the system (required for create). Must be one of: incident_manager, technical_support, account_manager, executive, system_administrator, client_contact"
                                },
                                "timezone": {
                                    "type": "string",
                                    "description": "User's timezone (required for create, cannot be empty)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "User's status (optional, defaults to 'active'). Must be one of: active, inactive"
                                },
                                "client_id": {
                                    "type": "string",
                                    "description": "Associated client identifier (required for client_contact role, optional for others, must exist if provided)"
                                }
                            }
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user record. Required for update action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }