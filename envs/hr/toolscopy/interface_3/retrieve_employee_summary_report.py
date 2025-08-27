import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveEmployeeSummaryReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str) -> str:
        employees = data.get("employees", {})
        users = data.get("users", {})
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})
        performance_reviews = data.get("performance_reviews", {})
        employee_training = data.get("employee_training", {})
        leave_requests = data.get("leave_requests", {})
        
        if employee_id not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = employees[employee_id]
        user = users.get(employee.get("user_id"), {})
        position = job_positions.get(employee.get("position_id"), {})
        department = departments.get(position.get("department_id"), {})
        
        # Count performance reviews
        review_count = sum(1 for review in performance_reviews.values() 
                          if review.get("employee_id") == employee_id)
        
        # Count completed training
        training_count = sum(1 for training in employee_training.values() 
                           if (training.get("employee_id") == employee_id and 
                               training.get("status") == "completed"))
        
        # Count leave requests
        leave_count = sum(1 for leave in leave_requests.values() 
                         if leave.get("employee_id") == employee_id)
        
        summary = {
            "employee_id": employee_id,
            "name": f"{user.get('first_name', '')} {user.get('last_name', '')}",
            "email": user.get("email"),
            "position_title": position.get("title"),
            "department_name": department.get("department_name"),
            "hire_date": employee.get("hire_date"),
            "employment_status": employee.get("employment_status"),
            "performance_reviews_count": review_count,
            "completed_training_count": training_count,
            "leave_requests_count": leave_count
        }
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_employee_summary_report",
                "description": "Get a comprehensive summary report for an employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"}
                    },
                    "required": ["employee_id"]
                }
            }
        }
