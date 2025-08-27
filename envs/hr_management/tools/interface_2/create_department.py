import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateDepartment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_name: str, manager_id: str, 
               budget: float, status: str = "active", hr_director_approval: bool = False) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        departments = data.get("departments", {})
        employees = data.get("employees", {})
        
        # Validate required fields
        if not department_name or not manager_id:
            raise ValueError("Department name and manager ID are required")
        
        # Check HR Director approval
        if not hr_director_approval:
            return json.dumps({
                "error": "HR Director approval required for department creation",
                "halt": True
            })
        
        # Validate manager exists
        if str(manager_id) not in employees:
            raise ValueError(f"Manager with ID {manager_id} not found")
        
        # Validate status
        valid_statuses = ['active', 'inactive']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        department_id = generate_id(departments)
        timestamp = "2025-10-01T00:00:00"
        
        new_department = {
            "department_id": department_id,
            "department_name": department_name,
            "manager_id": manager_id,
            "budget": budget,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        departments[department_id] = new_department
        return json.dumps({"department_id": department_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_department",
                "description": "Create a new department",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_name": {"type": "string", "description": "Name of the department"},
                        "manager_id": {"type": "string", "description": "Employee ID of the department manager"},
                        "budget": {"type": "number", "description": "Quarterly budget"},
                        "status": {"type": "string", "description": "Status: active, inactive (defaults to active)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval required (True/False)"}
                    },
                    "required": ["department_name", "manager_id", "budget"]
                }
            }
        }
