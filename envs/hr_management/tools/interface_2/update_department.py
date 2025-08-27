import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateDepartment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_id: str, hr_director_approval: bool,
               department_name: Optional[str] = None, manager_id: Optional[str] = None,
               budget: Optional[float] = None, status: Optional[str] = None) -> str:
        
        departments = data.get("departments", {})
        employees = data.get("employees", {})
        
        # Check HR Director approval
        if not hr_director_approval:
            return json.dumps({
                "error": "HR Director approval required for department updates",
                "halt": True
            })
        
        # Validate department exists
        if str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        department = departments[str(department_id)]
        
        # Validate manager exists if provided
        if manager_id and str(manager_id) not in employees:
            raise ValueError(f"Manager with ID {manager_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ['active', 'inactive']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update fields
        if department_name:
            department["department_name"] = department_name
        if manager_id:
            department["manager_id"] = manager_id
        if budget is not None:
            department["budget"] = budget
        if status:
            department["status"] = status
        
        department["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Department updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_department",
                "description": "Update an existing department",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_id": {"type": "string", "description": "ID of the department to update"},
                        "department_name": {"type": "string", "description": "Updated department name (optional)"},
                        "manager_id": {"type": "string", "description": "Updated manager employee ID (optional)"},
                        "budget": {"type": "number", "description": "Updated budget (optional)"},
                        "status": {"type": "string", "description": "Updated status: active, inactive (optional)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval required (True/False)"}
                    },
                    "required": ["department_id", "hr_director_approval"]
                }
            }
        }
