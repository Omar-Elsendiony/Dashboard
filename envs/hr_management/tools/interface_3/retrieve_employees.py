import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveEmployees(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        employee_id: Optional[str] = None,
        user_id: Optional[str] = None,
        position_id: Optional[str] = None,
        employment_status: Optional[str] = None,
        manager_id: Optional[str] = None,
    ) -> str:
        """
        Returns employees filtered by any combination of:
        employee_id, user_id, position_id, employment_status, manager_id.
        """
        employees = data.get("employees", {})
        results = []

        for employee in employees.values():
            if employee_id and employee.get("employee_id") != employee_id:
                continue
            if user_id and employee.get("user_id") != user_id:
                continue
            if position_id and employee.get("position_id") != position_id:
                continue
            if employment_status and employee.get("employment_status") != employment_status:
                continue
            if manager_id and employee.get("manager_id") != manager_id:
                continue
            results.append(employee)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_employees",
                "description": "Get employees with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "position_id": {"type": "string", "description": "Filter by position ID"},
                        "employment_status": {"type": "string", "description": "Filter by employment status"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"}
                    },
                    "required": []
                }
            }
        }