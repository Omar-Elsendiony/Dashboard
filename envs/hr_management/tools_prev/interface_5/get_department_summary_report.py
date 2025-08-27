import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDepartmentSummaryReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_id: str) -> str:
        departments = data.get("departments", {})
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        users = data.get("users", {})
        
        if department_id not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        department = departments[department_id]
        
        # Count positions in department
        position_count = sum(1 for position in job_positions.values() 
                           if position.get("department_id") == department_id)
        
        # Count employees in department
        department_positions = [pos_id for pos_id, pos in job_positions.items() 
                               if pos.get("department_id") == department_id]
        
        employee_count = sum(1 for employee in employees.values() 
                           if (employee.get("position_id") in department_positions and 
                               employee.get("employment_status") == "active"))
        
        # Get manager info
        manager = employees.get(department.get("manager_id"), {})
        manager_user = users.get(manager.get("user_id"), {})
        
        summary = {
            "department_id": department_id,
            "department_name": department.get("department_name"),
            "manager_name": f"{manager_user.get('first_name', '')} {manager_user.get('last_name', '')}",
            "budget": department.get("budget"),
            "status": department.get("status"),
            "total_positions": position_count,
            "active_employees": employee_count,
            "created_at": department.get("created_at")
        }
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_department_summary_report",
                "description": "Get a comprehensive summary report for a department",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_id": {"type": "string", "description": "ID of the department"}
                    },
                    "required": ["department_id"]
                }
            }
        }
