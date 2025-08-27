import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifyJobPosition(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str, title: Optional[str] = None,
               department_id: Optional[str] = None, job_level: Optional[str] = None,
               employment_type: Optional[str] = None, hourly_rate_min: Optional[float] = None,
               hourly_rate_max: Optional[float] = None, status: Optional[str] = None,
               hr_director_approval: Optional[bool] = None,
               hiring_manager_approval: Optional[bool] = None) -> str:
        
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        position = job_positions[str(position_id)]
        
        # Validate department if provided
        if department_id and str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        # Validate job level if provided
        if job_level:
            valid_levels = ['entry', 'junior', 'mid', 'senior', 'lead', 'manager', 'director', 'executive']
            if job_level not in valid_levels:
                raise ValueError(f"Invalid job_level. Must be one of {valid_levels}")
        
        # Validate employment type if provided
        if employment_type:
            valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
            if employment_type not in valid_types:
                raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Validate status if provided
        if status:
            valid_statuses = ['draft', 'open', 'closed']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            
            # Check approvals for open positions
            if status == 'open':
                if hr_director_approval is None or hiring_manager_approval is None:
                    return json.dumps({
                        "error": "HR Director and Hiring Manager approval required for open positions",
                        "halt": True
                    })
                if not hr_director_approval or not hiring_manager_approval:
                    return json.dumps({
                        "error": "Approval denied for position publication",
                        "halt": True
                    })
        
        # Validate hourly rates if provided
        min_rate = hourly_rate_min if hourly_rate_min is not None else position.get("hourly_rate_min")
        max_rate = hourly_rate_max if hourly_rate_max is not None else position.get("hourly_rate_max")
        if min_rate and max_rate and min_rate >= max_rate:
            raise ValueError("Minimum hourly rate must be less than maximum hourly rate")
        
        # Update fields
        if title:
            position["title"] = title
        if department_id:
            position["department_id"] = department_id
        if job_level:
            position["job_level"] = job_level
        if employment_type:
            position["employment_type"] = employment_type
        if hourly_rate_min is not None:
            position["hourly_rate_min"] = hourly_rate_min
        if hourly_rate_max is not None:
            position["hourly_rate_max"] = hourly_rate_max
        if status:
            position["status"] = status
        
        position["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Position updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_job_position",
                "description": "Update an existing job position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Position ID to update"},
                        "title": {"type": "string", "description": "Updated job title (optional)"},
                        "department_id": {"type": "string", "description": "Updated department ID (optional)"},
                        "job_level": {"type": "string", "description": "Updated job level (optional)"},
                        "employment_type": {"type": "string", "description": "Updated employment type (optional)"},
                        "hourly_rate_min": {"type": "number", "description": "Updated minimum hourly rate (optional)"},
                        "hourly_rate_max": {"type": "number", "description": "Updated maximum hourly rate (optional)"},
                        "status": {"type": "string", "description": "Updated status (optional)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval for publishable positions (True/False)"},
                        "hiring_manager_approval": {"type": "boolean", "description": "Hiring Manager approval for publishable positions (True/False)"}
                    },
                    "required": ["position_id"]
                }
            }
        }
