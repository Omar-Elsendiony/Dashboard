import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class OnboardEmployee(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, user_id: str, position_id: str,
               hire_date: str, employment_type: str, hr_manager_approval: bool,
               compliance_verification: bool, manager_id: Optional[str] = None,
               date_of_birth: Optional[str] = None, address: Optional[str] = None,
               emergency_contact_name: Optional[str] = None,
               emergency_contact_phone: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        users = data.get("users", {})
        job_positions = data.get("job_positions", {})
        
        # Check approvals
        if not hr_manager_approval:
            return json.dumps({
                "error": "HR Manager approval required for employee onboarding",
                "halt": True
            })
        
        if not compliance_verification:
            return json.dumps({
                "error": "Compliance verification required for eligibility documents",
                "halt": True
            })
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        # Validate manager exists if provided
        if manager_id and str(manager_id) not in employees:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate employment type
        valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
        if employment_type not in valid_types:
            raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Check if employee already exists
        if str(employee_id) in employees:
            raise ValueError(f"Employee {employee_id} already exists")
        
        timestamp = "2025-10-01T00:00:00"
        
        new_employee = {
            "employee_id": employee_id,
            "user_id": user_id,
            "position_id": position_id,
            "hire_date": hire_date,
            "employment_status": "active",
            "employment_type": employment_type,
            "manager_id": manager_id,
            "date_of_birth": date_of_birth,
            "address": address,
            "emergency_contact_name": emergency_contact_name,
            "emergency_contact_phone": emergency_contact_phone,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        employees[employee_id] = new_employee
        return json.dumps({"success": True, "message": "Employee onboarded successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "onboard_employee",
                "description": "Onboard a new employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "user_id": {"type": "string", "description": "Associated user ID"},
                        "position_id": {"type": "string", "description": "Position ID"},
                        "hire_date": {"type": "string", "description": "Hire date"},
                        "employment_type": {"type": "string", "description": "Employment type: full_time, part_time, contract, intern, temporary"},
                        "manager_id": {"type": "string", "description": "Manager employee ID (optional)"},
                        "date_of_birth": {"type": "string", "description": "Date of birth (optional)"},
                        "address": {"type": "string", "description": "Address (optional)"},
                        "emergency_contact_name": {"type": "string", "description": "Emergency contact name (optional)"},
                        "emergency_contact_phone": {"type": "string", "description": "Emergency contact phone (optional)"},
                        "hr_manager_approval": {"type": "boolean", "description": "HR Manager approval (True/False)"},
                        "compliance_verification": {"type": "boolean", "description": "Compliance verification for eligibility documents (True/False)"}
                    },
                    "required": ["employee_id", "user_id", "position_id", "hire_date", "employment_type", "hr_manager_approval", "compliance_verification"]
                }
            }
        }
