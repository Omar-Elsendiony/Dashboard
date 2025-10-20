import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessUserOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, user_id: str = None, 
               employee_id: str = None, first_name: str = None, last_name: str = None, 
               email: str = None, phone_number: str = None, role: str = None, 
               employment_status: str = None, created_by: str = None) -> str:
        """
        Manage user operations for HR talent management system.
        
        Operations:
        - create_user: Create new user (requires employee_id, role, and created_by). Validates employee exists and is active,
          ensures no duplicate user account exists for the employee, inherits first_name, last_name, 
          and email from employee data, and validates that created_by user has appropriate role permissions.
        - update_user: Update existing user (requires user_id and field changes)
        - deactivate_user: Deactivate user account (requires user_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if operation_type not in ["create_user", "update_user", "deactivate_user"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_user', 'update_user', or 'deactivate_user'"
            })
        
        # Access users data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for users"
            })
        
        users = data.get("users", {})
        employees = data.get("employees", {})
        
        if operation_type == "create_user":
            # Validate required fields for creation
            if not employee_id:
                return json.dumps({
                    "success": False,
                    "error": "employee_id is required for create_user operation"
                })
            if not role:
                return json.dumps({
                    "success": False,
                    "error": "role is required for create_user operation"
                })
            if not created_by:
                return json.dumps({
                    "success": False,
                    "error": "created_by is required for create_user operation"
                })
            
            # Validate that created_by user exists and has appropriate role
            if created_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User with created_by '{created_by}' does not exist"
                })
            
            creator_user = users[created_by]
            if creator_user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User with created_by '{created_by}' is not active"
                })
            
            # Check if creator has appropriate role to create users
            creator_role = creator_user.get("role")
            valid_creator_roles = ["hr_admin", "hr_manager", "hr_director"]
            if creator_role not in valid_creator_roles:
                return json.dumps({
                    "success": False,
                    "error": f"User with created_by '{created_by}' does not have permission to create users. Required roles: {', '.join(valid_creator_roles)}"
                })
            
            # Validate that employee exists and is active
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Employee with employee_id '{employee_id}' does not exist"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Employee with employee_id '{employee_id}' is not active (status: {employee.get('employment_status', 'unknown')})"
                })
            
            # Check for duplicate user account for this employee_id
            for existing_user in users.values():
                if existing_user.get("employee_id") == employee_id:
                    return json.dumps({
                        "success": False,
                        "error": f"User account already exists for employee_id '{employee_id}'"
                    })
            
            # When employee_id is provided, inherit data from employee record
            # Override any provided first_name, last_name, email with employee data
            first_name = employee.get("first_name")
            last_name = employee.get("last_name")
            email = employee.get("work_email")
            
            # Validate that employee has required data
            if not first_name:
                return json.dumps({
                    "success": False,
                    "error": f"Employee {employee_id} missing first_name in employee record"
                })
            if not last_name:
                return json.dumps({
                    "success": False,
                    "error": f"Employee {employee_id} missing last_name in employee record"
                })
            if not email:
                return json.dumps({
                    "success": False,
                    "error": f"Employee {employee_id} missing work_email in employee record"
                })
            
            # Validate role enum
            valid_roles = ["hr_recruiter", "hiring_manager", "hr_onboarding_specialist", "hr_payroll_administrator", 
                          "hr_manager", "hr_admin", "compliance_officer", "finance_manager", "it_administrator", "employee"]
            if role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                })
            
            # Validate employment_status enum if provided, otherwise default to active
            if employment_status:
                valid_statuses = ["active", "inactive", "suspended"]
                if employment_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid employment_status. Must be one of: {', '.join(valid_statuses)}"
                    })
            else:
                employment_status = "active"  # Default to active if not provided
            
            # Validate email format (basic validation)
            if "@" not in email or "." not in email.split("@")[1]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid email format"
                })
            
            # Check for duplicate email
            for existing_user in users.values():
                if existing_user.get("email", "").lower() == email.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"User with email '{email}' already exists"
                    })
            
            # Check for duplicate employee_id
            for existing_user in users.values():
                if existing_user.get("employee_id") == employee_id:
                    return json.dumps({
                        "success": False,
                        "error": f"User with employee_id '{employee_id}' already exists"
                    })
            
            # Generate new user ID
            new_user_id = generate_id(users)
            
            # Create new user record
            new_user = {
                "user_id": str(new_user_id),
                "employee_id": employee_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "role": role,
                "employment_status": employment_status,
                "created_at": "2025-10-10T12:00:00",
                "updated_at": "2025-10-10T12:00:00"
            }
            
            users[str(new_user_id)] = new_user
            
            return json.dumps({
                "success": True,
                "operation_type": "create_user",
                "user_id": str(new_user_id),
                "message": f"User {new_user_id} created successfully with email '{email}' by user {created_by}",
                "user_data": new_user
            })
        
        elif operation_type == "update_user":
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "user_id is required for update_user operation"
                })
            
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} not found"
                })
            
            # Check if at least one field is provided for update
            update_fields = [first_name, last_name, email, phone_number, role, employment_status]
            if not any(field is not None for field in update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update_user operation"
                })
            
            # Validate role enum if provided
            if role is not None:
                valid_roles = ["hr_recruiter", "hiring_manager", "hr_onboarding_specialist", "hr_payroll_administrator", 
                              "hr_manager", "hr_admin", "compliance_officer", "finance_manager", "it_administrator", "employee"]
                if role not in valid_roles:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                    })
            
            # Validate employment_status enum if provided
            if employment_status is not None:
                valid_statuses = ["active", "inactive", "suspended"]
                if employment_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid employment_status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate email format if provided
            if email is not None:
                if "@" not in email or "." not in email.split("@")[1]:
                    return json.dumps({
                        "success": False,
                        "error": "Invalid email format"
                    })
                
                # Check for duplicate email (excluding current user)
                for existing_user_id, existing_user in users.items():
                    if (existing_user_id != user_id and 
                        existing_user.get("email", "").lower() == email.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"User with email '{email}' already exists"
                        })
            
            # Update user record
            current_user = users[user_id]
            updated_user = current_user.copy()
            
            if first_name is not None:
                updated_user["first_name"] = first_name
            if last_name is not None:
                updated_user["last_name"] = last_name
            if email is not None:
                updated_user["email"] = email
            if phone_number is not None:
                updated_user["phone_number"] = phone_number
            if role is not None:
                updated_user["role"] = role
            if employment_status is not None:
                updated_user["employment_status"] = employment_status
            
            updated_user["updated_at"] = "2025-10-10T12:00:00"
            users[user_id] = updated_user
            
            return json.dumps({
                "success": True,
                "operation_type": "update_user",
                "user_id": str(user_id),
                "message": f"User {user_id} updated successfully",
                "user_data": updated_user
            })
        
        elif operation_type == "deactivate_user":
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "user_id is required for deactivate_user operation"
                })
            
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} not found"
                })
            
            # Update user status to inactive
            current_user = users[user_id]
            if current_user.get("employment_status") == "inactive":
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} is already inactive"
                })
            
            updated_user = current_user.copy()
            updated_user["employment_status"] = "inactive"
            updated_user["updated_at"] = "2025-10-10T12:00:00"
            users[user_id] = updated_user
            
            return json.dumps({
                "success": True,
                "operation_type": "deactivate_user",
                "user_id": str(user_id),
                "message": f"User {user_id} deactivated successfully",
                "user_data": updated_user
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_user_operations",
                "description": "Manage user operations in the HR talent management system. This tool handles user account lifecycle management including creation of new user accounts, updates to existing user information, and user account deactivation. For creation, validates that the employee_id exists and is active, ensures no duplicate user account exists for the employee, inherits first_name, last_name, and email from the employee record, and validates that the created_by user has appropriate role permissions (hr_admin, hr_manager, or hr_director). Establishes new user records with comprehensive validation to ensure data integrity and prevent duplicates. For updates, modifies existing user records while maintaining referential integrity. For deactivation, safely transitions user accounts to inactive status. Validates user roles, employment status, email formats, and enforces uniqueness constraints. Essential for user administration, access control, and maintaining accurate user records throughout the employee lifecycle.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_user' to create new user account, 'update_user' to modify existing user information, 'deactivate_user' to deactivate user account",
                            "enum": ["create_user", "update_user", "deactivate_user"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Employee identifier (required for create_user, must exist and be active, cannot be updated). When provided, first_name, last_name, and email are inherited from employee data."
                        },
                        "first_name": {
                            "type": "string",
                            "description": "User's first name (inherited from employee data when employee_id is provided, optional for update_user)"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "User's last name (inherited from employee data when employee_id is provided, optional for update_user)"
                        },
                        "email": {
                            "type": "string",
                            "description": "User's email address (inherited from employee work_email when employee_id is provided, optional for update_user, must be unique)"
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "User's phone number (optional for both create and update)"
                        },
                        "role": {
                            "type": "string",
                            "description": "User's role in the system (required for create_user, optional for update_user)",
                            "enum": ["hr_recruiter", "hiring_manager", "hr_onboarding_specialist", "hr_payroll_administrator", "hr_manager", "hr_admin", "compliance_officer", "finance_manager", "it_administrator", "employee"]
                        },
                        "employment_status": {
                            "type": "string",
                            "description": "User's employment status (optional for create_user, defaults to 'active', optional for update_user)",
                            "enum": ["active", "inactive", "suspended"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user (required for update_user and deactivate_user operations)"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "Unique identifier of the user creating the new user account (required for create_user operation, must have hr_admin, hr_manager, or hr_director role)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
