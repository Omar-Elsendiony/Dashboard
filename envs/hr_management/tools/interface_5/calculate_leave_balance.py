import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateLeaveBalance(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, leave_type: str, 
               annual_allocation: float = 15) -> str:
        employees = data.get("employees", {})
        leave_requests = data.get("leave_requests", {})
        
        if employee_id not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Calculate used leave days
        used_days = 0
        for leave in leave_requests.values():
            if (leave.get("employee_id") == employee_id and 
                leave.get("leave_type") == leave_type and 
                leave.get("status") == "approved"):
                used_days += leave.get("days_requested", 0)
        
        remaining_balance = annual_allocation - used_days
        
        balance_info = {
            "employee_id": employee_id,
            "leave_type": leave_type,
            "annual_allocation": annual_allocation,
            "used_days": used_days,
            "remaining_balance": remaining_balance
        }
        
        return json.dumps(balance_info)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_leave_balance",
                "description": "Calculate remaining leave balance for an employee. It can be used to calculate remaining balance without creating a request.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "leave_type": {"type": "string", "description": "Type of leave to calculate"},
                        "annual_allocation": {"type": "number", "description": "Annual leave allocation for this type for this employee (15 by default)"}
                    },
                    "required": ["employee_id", "leave_type"]
                }
            }
        }
