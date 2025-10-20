import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleDepartmentOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, user_id: str = None, department_id: str = None, 
               department_name: str = None, department_code: str = None, manager_id: str = None, 
               budget: float = None, status: str = None) -> str:
        """
        Manage department operations for HR talent management system.
        
        Operations:
        - create_department: Create new department (requires department_name, department_code, manager_id)
        - update_department: Update existing department (requires department_id and field changes)
        - deactivate_department: Deactivate department (requires department_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if operation_type not in ["create_department", "update_department", "deactivate_department"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_department', 'update_department', or 'deactivate_department'"
            })
        
        # Access departments data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for departments"
            })
        
        departments = data.get("departments", {})
        users = data.get("users", {})
        
        if operation_type == "create_department":
            # Validate required fields for creation
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields: user_id"
                })
            if not department_name:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields: department_name"
                })
            if not department_code:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields: department_code"
                })
            if not manager_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields: manager_id"
                })
            
            # Verify user has appropriate role
            user = users.get(user_id)
            if not user or user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: User lacks authorization to perform this action"
                })
            
            valid_roles = ["hr_admin", "hr_manager", "hr_director"]
            if user.get("role") not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": "Halt: User lacks authorization to perform this action"
                })
            
            # Validate status enum if provided, otherwise default to active
            if status:
                valid_statuses = ["active", "inactive"]
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            else:
                status = "active"  # Default to active if not provided
            
            # Validate budget if provided (must be non-negative number)
            if budget is not None:
                try:
                    budget_value = float(budget)
                    if budget_value < 0:
                        return json.dumps({
                            "success": False,
                            "error": "Department budget must be a non-negative number"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Department budget must be a valid number"
                    })
            
            # Validate manager exists and is active Department Manager
            if manager_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Department Manager not found or inactive"
                })
            
            manager = users[manager_id]
            if manager.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Department Manager not found or inactive"
                })
            
            if manager.get("role") != "department_manager":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Department Manager not found or inactive"
                })
            
            # Check for duplicate department name
            department_name_clean = department_name.strip()
            for existing_department in departments.values():
                if existing_department.get("department_name", "").strip().lower() == department_name_clean.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Department with name '{department_name_clean}' already exists"
                    })
            
            # Check for duplicate department code
            department_code_clean = department_code.strip()
            for existing_department in departments.values():
                if existing_department.get("department_code", "").strip().lower() == department_code_clean.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Department with code '{department_code_clean}' already exists"
                    })
            
            # Generate new department ID
            new_department_id = generate_id(departments)
            
            # Create new department record
            new_department = {
                "department_id": str(new_department_id),
                "department_name": department_name,
                "department_code": department_code,
                "manager_id": manager_id,
                "budget": budget,
                "status": status,
                "created_at": "2025-10-10T12:00:00"
            }
            
            departments[str(new_department_id)] = new_department
            
            return json.dumps({
                "success": True,
                "operation_type": "create_department",
                "department_id": str(new_department_id),
                "message": f"Department {new_department_id} created successfully with name '{department_name_clean}'",
                "department_data": new_department
            })
        
        elif operation_type == "update_department":
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields: user_id"
                })
            if not department_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields: department_id"
                })
            
            if department_id not in departments:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Department not found"
                })
            
            # Verify user has appropriate role
            user = users.get(user_id)
            if not user or user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: User lacks authorization to perform this action"
                })
            
            valid_roles = ["hr_admin", "hr_manager", "hr_director"]
            if user.get("role") not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": "Halt: User lacks authorization to perform this action"
                })
            
            # Check if at least one field is provided for update
            update_fields = [department_name, department_code, manager_id, budget, status]
            if not any(field is not None for field in update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update_department operation"
                })
            
            # Validate status enum if provided
            if status is not None:
                valid_statuses = ["active", "inactive"]
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate budget if provided
            if budget is not None:
                try:
                    budget_value = float(budget)
                    if budget_value < 0:
                        return json.dumps({
                            "success": False,
                            "error": "Department budget must be a non-negative number"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Department budget must be a valid number"
                    })
            
            # Validate manager exists and is active Department Manager if provided
            if manager_id is not None:
                if manager_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Department Manager not found or inactive"
                    })
                
                manager = users[manager_id]
                if manager.get("employment_status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Department Manager not found or inactive"
                    })
                
                if manager.get("role") != "department_manager":
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Department Manager not found or inactive"
                    })
            
            # Check for duplicate department name if updating name
            if department_name is not None:
                new_department_name = department_name.strip()
                for existing_department_id, existing_department in departments.items():
                    if (existing_department_id != department_id and 
                        existing_department.get("department_name", "").strip().lower() == new_department_name.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Department with name '{new_department_name}' already exists"
                        })
            
            # Check for duplicate department code if updating code
            if department_code is not None:
                new_department_code = department_code.strip()
                for existing_department_id, existing_department in departments.items():
                    if (existing_department_id != department_id and 
                        existing_department.get("department_code", "").strip().lower() == new_department_code.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Department with code '{new_department_code}' already exists"
                        })
            
            # Update department record
            current_department = departments[department_id]
            updated_department = current_department.copy()
            
            if department_name is not None:
                updated_department["department_name"] = department_name
            if department_code is not None:
                updated_department["department_code"] = department_code
            if manager_id is not None:
                updated_department["manager_id"] = manager_id
            if budget is not None:
                updated_department["budget"] = budget
            if status is not None:
                updated_department["status"] = status
            
            departments[department_id] = updated_department
            
            return json.dumps({
                "success": True,
                "operation_type": "update_department",
                "department_id": str(department_id),
                "message": f"Department {department_id} updated successfully",
                "department_data": updated_department
            })
        
        elif operation_type == "deactivate_department":
            if not department_id:
                return json.dumps({
                    "success": False,
                    "error": "department_id is required for deactivate_department operation"
                })
            
            if department_id not in departments:
                return json.dumps({
                    "success": False,
                    "error": f"Department {department_id} not found"
                })
            
            # Update department status to inactive
            current_department = departments[department_id]
            if current_department.get("status") == "inactive":
                return json.dumps({
                    "success": False,
                    "error": f"Department {department_id} is already inactive"
                })
            
            updated_department = current_department.copy()
            updated_department["status"] = "inactive"
            departments[department_id] = updated_department
            
            return json.dumps({
                "success": True,
                "operation_type": "deactivate_department",
                "department_id": str(department_id),
                "message": f"Department {department_id} deactivated successfully",
                "department_data": updated_department
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_department_operations",
                "description": "Manage department operations in the HR talent management system. This tool handles department data management including creation of new organizational departments, updates to existing department information, and department deactivation. For creation, establishes new department records with comprehensive validation to ensure data integrity and prevent duplicates. For updates, modifies existing department records while maintaining referential integrity and organizational hierarchy. For deactivation, safely transitions departments to inactive status. Validates department names, codes, manager assignments, budget constraints, and enforces uniqueness constraints. Essential for organizational structure management, cost-center alignment, and maintaining accurate department records for reporting and administrative purposes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_department' to create new department, 'update_department' to modify existing department information, 'deactivate_department' to deactivate department",
                            "enum": ["create_department", "update_department", "deactivate_department"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID performing the operation (required for all operations, must be active HR Admin, HR Manager, or HR Director)"
                        },
                        "department_name": {
                            "type": "string",
                            "description": "Name of the department (required for create_department, optional for update_department, must be unique)"
                        },
                        "department_code": {
                            "type": "string",
                            "description": "Unique code for the department (required for create_department, optional for update_department, must be unique)"
                        },
                        "manager_id": {
                            "type": "string",
                            "description": "User ID of the department manager (required for create_department, optional for update_department, must be active user)"
                        },
                        "budget": {
                            "type": "number",
                            "description": "Department budget amount (optional for both create and update, must be non-negative)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Department status (optional for both create and update, defaults to active)",
                            "enum": ["active", "inactive"]
                        },
                        "department_id": {
                            "type": "string",
                            "description": "Unique identifier of the department (required for update_department and deactivate_department operations)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
