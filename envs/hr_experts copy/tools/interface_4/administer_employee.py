import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AdministerEmployee(Tool):
    """
    Execute employee records including onboarding, profile updates, and offboarding.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        employee_id: Optional[str] = None,
        user_id: Optional[str] = None,
        position_id: Optional[str] = None,
        hire_date: Optional[str] = None,
        manager_id: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        address: Optional[str] = None,
        hourly_rate: Optional[float] = None,
        employment_status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on employee records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def validate_date_format(date_str: str, field_name: str) -> bool:
            """Validates date format YYYY-MM-DD"""
            if not date_str:
                return True
            try:
                parts = date_str.split('-')
                if len(parts) != 3:
                    return False
                year, month, day = map(int, parts)
                if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                    return False
                return True
            except ValueError:
                return False

        timestamp = "2025-10-01T12:00:00"
        employees = data.get("employees", {})
        users = data.get("users", {})
        job_positions = data.get("job_positions", {})

        # Validate supported employment statuses
        supported_employment_statuses = ["active", "inactive", "terminated"]

        if action == "create":
            # Required fields for employee creation (onboarding)
            if not all([user_id, position_id, hire_date]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: user_id, position_id, hire_date"
                })

            # Validate user exists
            if user_id not in users:
                return json.dumps({
                    "error": f"User with ID '{user_id}' not found"
                })

            # Validate position exists
            if position_id not in job_positions:
                return json.dumps({
                    "error": f"Job position with ID '{position_id}' not found"
                })

            # Check if employee record already exists for this user
            for existing_employee in employees.values():
                if existing_employee.get("user_id") == user_id:
                    return json.dumps({
                        "error": f"Employee record already exists for user ID '{user_id}'"
                    })

            # Validate manager exists if provided
            if manager_id:
                manager_exists = False
                for employee in employees.values():
                    if employee.get("employee_id") == manager_id and employee.get("employment_status") == "active":
                        manager_exists = True
                        break
                if not manager_exists:
                    return json.dumps({
                        "error": f"Active manager with employee ID '{manager_id}' not found"
                    })

            # Validate hire_date format
            if not validate_date_format(hire_date, "hire_date"):
                return json.dumps({
                    "error": "Invalid hire_date format. Use YYYY-MM-DD"
                })

            # Validate date_of_birth format if provided
            if date_of_birth and not validate_date_format(date_of_birth, "date_of_birth"):
                return json.dumps({
                    "error": "Invalid date_of_birth format. Use YYYY-MM-DD"
                })

            # Validate employment_status if provided
            if employment_status and employment_status not in supported_employment_statuses:
                return json.dumps({
                    "error": f"Invalid employment_status '{employment_status}'. Must be one of: {', '.join(supported_employment_statuses)}"
                })

            # Validate hourly_rate if provided
            if hourly_rate is not None:
                try:
                    hourly_rate = float(hourly_rate)
                    if hourly_rate < 0:
                        return json.dumps({
                            "error": "Hourly rate must be non-negative"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "error": "Invalid hourly_rate value. Must be a number"
                    })

            # Generate new employee ID
            new_employee_id = generate_id(employees)

            # Create new employee record
            new_employee = {
                "employee_id": new_employee_id,
                "user_id": user_id,
                "position_id": position_id,
                "hire_date": hire_date,
                "employment_status": employment_status if employment_status else "active",
                "manager_id": manager_id,
                "date_of_birth": date_of_birth,
                "address": address,
                "hourly_rate": hourly_rate,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add to employees data
            employees[new_employee_id] = new_employee

            return json.dumps({
                "success": True,
                "message": f"Employee record created successfully for user ID '{user_id}'",
                "employee_id": new_employee_id,
                "employee_data": new_employee
            })

        elif action == "update":
            # Required field for employee update
            if not employee_id:
                return json.dumps({
                    "error": "Missing required parameter 'employee_id' for update operation"
                })

            # At least one optional field must be provided
            optional_fields = [position_id, employment_status, manager_id, date_of_birth, address, hourly_rate]
            if not any(field is not None for field in optional_fields):
                return json.dumps({
                    "error": "At least one optional parameter (position_id, employment_status, manager_id, date_of_birth, address, hourly_rate) must be provided for update operation"
                })

            # Check if employee exists
            if employee_id not in employees:
                return json.dumps({
                    "error": f"Employee with ID '{employee_id}' not found"
                })

            # Validate position exists if provided
            if position_id and position_id not in job_positions:
                return json.dumps({
                    "error": f"Job position with ID '{position_id}' not found"
                })

            # Validate manager exists if provided
            if manager_id:
                manager_exists = False
                for employee in employees.values():
                    if employee.get("employee_id") == manager_id and employee.get("employment_status") == "active":
                        manager_exists = True
                        break
                if not manager_exists:
                    return json.dumps({
                        "error": f"Active manager with employee ID '{manager_id}' not found"
                    })

            # Validate date_of_birth format if provided
            if date_of_birth and not validate_date_format(date_of_birth, "date_of_birth"):
                return json.dumps({
                    "error": "Invalid date_of_birth format. Use YYYY-MM-DD"
                })

            # Validate employment_status if provided
            if employment_status and employment_status not in supported_employment_statuses:
                return json.dumps({
                    "error": f"Invalid employment_status '{employment_status}'. Must be one of: {', '.join(supported_employment_statuses)}"
                })

            # Validate hourly_rate if provided
            if hourly_rate is not None:
                try:
                    hourly_rate = float(hourly_rate)
                    if hourly_rate < 0:
                        return json.dumps({
                            "error": "Hourly rate must be non-negative"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "error": "Invalid hourly_rate value. Must be a number"
                    })

            # Update employee record
            employee_record = employees[employee_id]
            
            if position_id:
                employee_record["position_id"] = position_id
            if employment_status:
                employee_record["employment_status"] = employment_status
            if manager_id is not None:  # Allow setting to None
                employee_record["manager_id"] = manager_id
            if date_of_birth:
                employee_record["date_of_birth"] = date_of_birth
            if address:
                employee_record["address"] = address
            if hourly_rate is not None:
                employee_record["hourly_rate"] = hourly_rate
            
            employee_record["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "message": f"Employee with ID '{employee_id}' updated successfully",
                "employee_id": employee_id,
                "employee_data": employee_record
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
                "name": "administer_employee",
                "description": "Execute employee records including onboarding, profile updates, and offboarding. For onboarding (create), requires user_id, position_id, and hire_date, with optional fields for manager_id, date_of_birth, address, hourly_rate, and employment_status. For updates, requires employee_id and at least one optional field (position_id, employment_status, manager_id, date_of_birth, address, hourly_rate). Used for employee lifecycle management including onboarding, profile updates, and status changes for offboarding.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform: 'create' for employee onboarding, 'update' for profile updates or offboarding",
                            "enum": ["create", "update"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Employee ID (required for update operations)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID (required for create operations)"
                        },
                        "position_id": {
                            "type": "string",
                            "description": "Job position ID (required for create, optional for update)"
                        },
                        "hire_date": {
                            "type": "string",
                            "description": "Hire date in YYYY-MM-DD format (required for create operations)"
                        },
                        "manager_id": {
                            "type": "string",
                            "description": "Manager's employee ID (optional for both create and update)"
                        },
                        "date_of_birth": {
                            "type": "string",
                            "description": "Date of birth in YYYY-MM-DD format (optional for both create and update)"
                        },
                        "address": {
                            "type": "string",
                            "description": "Employee address (optional for both create and update)"
                        },
                        "hourly_rate": {
                            "type": "number",
                            "description": "Hourly rate (optional for both create and update)"
                        },
                        "employment_status": {
                            "type": "string",
                            "description": "Employment status: 'active', 'inactive', or 'terminated' (optional for both create and update)",
                            "enum": ["active", "inactive", "terminated"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }