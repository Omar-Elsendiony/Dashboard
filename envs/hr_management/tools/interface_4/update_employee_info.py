import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateEmployeeInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, position_id: Optional[str] = None,
               employment_status: Optional[str] = None, employment_type: Optional[str] = None,
               manager_id: Optional[str] = None, address: Optional[str] = None,
               emergency_contact_name: Optional[str] = None,
               emergency_contact_phone: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        
        # Validate employee exists
        if str(employee_id) not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = employees[str(employee_id)]
        
        # Validate position if provided
        if position_id and str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        # Validate manager if provided
        if manager_id and str(manager_id) not in employees:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate employment status if provided
        if employment_status:
            valid_statuses = ['active', 'terminated', 'on_leave', 'suspended']
            if employment_status not in valid_statuses:
                raise ValueError(f"Invalid employment_status. Must be one of {valid_statuses}")
        
        # Validate employment type if provided
        if employment_type:
            valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
            if employment_type not in valid_types:
                raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Update fields
        if position_id:
            employee["position_id"] = position_id
        if employment_status:
            employee["employment_status"] = employment_status
        if employment_type:
            employee["employment_type"] = employment_type
        if manager_id:
            employee["manager_id"] = manager_id
        if address:
            employee["address"] = address
        if emergency_contact_name:
            employee["emergency_contact_name"] = emergency_contact_name
        if emergency_contact_phone:
            employee["emergency_contact_phone"] = emergency_contact_phone
        
        employee["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Employee profile updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_employee_info",
                "description": "Update an employee's profile information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "position_id": {"type": "string", "description": "Updated position ID (optional)"},
                        "employment_status": {"type": "string", "description": "Employment status: active, terminated, on_leave, suspended (optional)"},
                        "employment_type": {"type": "string", "description": "Employment type (optional)"},
                        "manager_id": {"type": "string", "description": "Updated manager employee ID (optional)"},
                        "address": {"type": "string", "description": "Updated address (optional)"},
                        "emergency_contact_name": {"type": "string", "description": "Updated emergency contact name (optional)"},
                        "emergency_contact_phone": {"type": "string", "description": "Updated emergency contact phone (optional)"}
                    },
                    "required": ["employee_id"]
                }
            }
        }
