import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class OffboardEmployee(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, termination_date: str,
               termination_reason: str, hr_manager_approval: bool,
               compliance_officer_approval: bool) -> str:
        
        employees = data.get("employees", {})
        
        # Check approvals
        if not hr_manager_approval:
            return json.dumps({
                "error": "HR Manager approval required for employee offboarding",
                "halt": True
            })
        
        if not compliance_officer_approval:
            return json.dumps({
                "error": "Compliance Officer approval required for employee offboarding",
                "halt": True
            })
        
        # Validate employee exists
        if str(employee_id) not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = employees[str(employee_id)]
        
        # Update employee status
        employee["employment_status"] = "terminated"
        employee["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Employee offboarded successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "offboard_employee",
                "description": "Offboard an employee (terminate employment)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "termination_date": {"type": "string", "description": "Termination date"},
                        "termination_reason": {"type": "string", "description": "Reason for termination"},
                        "hr_manager_approval": {"type": "boolean", "description": "HR Manager approval (True/False)"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval (True/False)"}
                    },
                    "required": ["employee_id", "termination_date", "termination_reason", "hr_manager_approval", "compliance_officer_approval"]
                }
            }
        }
EOFd": ["first_name", "last_name", "email", "role"]
                }
            }
        }
