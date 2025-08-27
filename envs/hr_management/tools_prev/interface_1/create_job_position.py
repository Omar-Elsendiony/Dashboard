import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateJobPosition(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, department_id: str, job_level: str,
               employment_type: str, hourly_rate_min: float, hourly_rate_max: float,
               status: str = "draft", hr_director_approval: Optional[bool] = None,
               hiring_manager_approval: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})
        
        # Validate required fields
        if not all([title, department_id, job_level, employment_type]):
            raise ValueError("Title, department_id, job_level, and employment_type are required")
        
        # Validate department exists
        if str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        # Validate job level
        valid_levels = ['entry', 'junior', 'mid', 'senior', 'lead', 'manager', 'director', 'executive']
        if job_level not in valid_levels:
            raise ValueError(f"Invalid job_level. Must be one of {valid_levels}")
        
        # Validate employment type
        valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
        if employment_type not in valid_types:
            raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Validate status
        valid_statuses = ['draft', 'open', 'closed']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check approvals for publishable positions
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
        
        # Validate hourly rates
        if hourly_rate_min >= hourly_rate_max:
            raise ValueError("Minimum hourly rate must be less than maximum hourly rate")
        
        position_id = generate_id(job_positions)
        timestamp = "2025-10-01T00:00:00"
        
        new_position = {
            "position_id": position_id,
            "title": title,
            "department_id": department_id,
            "job_level": job_level,
            "employment_type": employment_type,
            "hourly_rate_min": hourly_rate_min,
            "hourly_rate_max": hourly_rate_max,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        job_positions[position_id] = new_position
        return json.dumps({"position_id": position_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_job_position",
                "description": "Create a new job position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Job title"},
                        "department_id": {"type": "string", "description": "Department ID"},
                        "job_level": {"type": "string", "description": "Job level: entry, junior, mid, senior, lead, manager, director, executive"},
                        "employment_type": {"type": "string", "description": "Employment type: full_time, part_time, contract, intern, temporary"},
                        "hourly_rate_min": {"type": "number", "description": "Minimum hourly rate"},
                        "hourly_rate_max": {"type": "number", "description": "Maximum hourly rate"},
                        "status": {"type": "string", "description": "Status: draft, open, closed (defaults to draft)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval for publishable positions (True/False)"},
                        "hiring_manager_approval": {"type": "boolean", "description": "Hiring Manager approval for publishable positions (True/False)"}
                    },
                    "required": ["title", "department_id", "job_level", "employment_type", "hourly_rate_min", "hourly_rate_max"]
                }
            }
        }
