import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageDepartment(Tool):
    """
    Manages department records including creation and updates.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        department_id: Optional[str] = None,
        department_name: Optional[str] = None,
        manager_id: Optional[str] = None,
        budget: Optional[float] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on department records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        departments = data.get("departments", {})
        users = data.get("users", {})

        # Validate supported statuses
        supported_statuses = ["active", "inactive"]

        if action == "create":
            # Required fields for department creation
            if not all([department_name, manager_id]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: department_name, manager_id"
                })

            # Validate manager_id exists in users
            if manager_id not in users:
                return json.dumps({
                    "error": f"Manager with ID '{manager_id}' not found in users"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate department name
            for existing_dept in departments.values():
                if existing_dept.get("department_name") == department_name:
                    return json.dumps({
                        "error": f"Department with name '{department_name}' already exists"
                    })

            # Generate new department ID
            new_department_id = generate_id(departments)

            # Create new department record
            new_department = {
                "department_id": new_department_id,
                "department_name": department_name,
                "manager_id": manager_id,
                "status": status or "active",  # Default to active if not specified
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add budget if provided
            if budget is not None:
                if budget < 0:
                    return json.dumps({
                        "error": "Budget must be a non-negative value"
                    })
                new_department["budget"] = budget

            # Add to departments data
            departments[new_department_id] = new_department

            return json.dumps({
                "success": True,
                "message": f"Department created successfully with ID {new_department_id}",
                "department_id": new_department_id,
                "department_data": new_department
            })

        elif action == "update":
            # department_id is required for update
            if not department_id:
                return json.dumps({
                    "error": "Missing required parameter 'department_id' for update operation"
                })

            # Check if department exists
            if department_id not in departments:
                return json.dumps({
                    "error": f"Department with ID {department_id} not found"
                })

            department_to_update = departments[department_id]

            # Validate manager_id if being updated
            if manager_id and manager_id not in users:
                return json.dumps({
                    "error": f"Manager with ID '{manager_id}' not found in users"
                })

            # Validate status if being updated
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate department name if name is being changed
            if department_name and department_name != department_to_update.get("department_name"):
                for existing_dept in departments.values():
                    if existing_dept.get("department_name") == department_name:
                        return json.dumps({
                            "error": f"Department with name '{department_name}' already exists"
                        })

            # Validate budget if provided
            if budget is not None and budget < 0:
                return json.dumps({
                    "error": "Budget must be a non-negative value"
                })

            # Track what fields are being updated
            updated_fields = []

            # Update fields if provided
            if department_name:
                department_to_update["department_name"] = department_name
                updated_fields.append("department_name")
            
            if manager_id:
                department_to_update["manager_id"] = manager_id
                updated_fields.append("manager_id")
            
            if budget is not None:
                department_to_update["budget"] = budget
                updated_fields.append("budget")
            
            if status:
                department_to_update["status"] = status
                updated_fields.append("status")

            # Update timestamp
            department_to_update["updated_at"] = timestamp

            if not updated_fields:
                return json.dumps({
                    "error": "No fields provided to update. At least one optional field must be provided"
                })

            return json.dumps({
                "success": True,
                "message": f"Department {department_id} updated successfully",
                "updated_fields": updated_fields,
                "department_data": department_to_update
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_department",
                "description": "Manages department records for organizational structure operations. Supports creating new departments with proper validation and updating existing departments. For creation, validates required fields (department_name, manager_id) and optional fields (budget, status). For updates, validates department existence and allows modification of any department field. Validates manager IDs against users table and prevents duplicate department names. Supported statuses: active, inactive. Budget must be non-negative if provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform: 'create' for new department, 'update' for modifying existing department",
                            "enum": ["create", "update"]
                        },
                        "department_id": {
                            "type": "string",
                            "description": "Department ID (required for update operations)"
                        },
                        "department_name": {
                            "type": "string",
                            "description": "Department name (required for create, must be unique)"
                        },
                        "manager_id": {
                            "type": "string",
                            "description": "ID of the department manager (required for create, must exist in users)"
                        },
                        "budget": {
                            "type": "number",
                            "description": "Department budget (optional, must be non-negative)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Department status (optional, defaults to 'active' for new departments)",
                            "enum": ["active", "inactive"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }