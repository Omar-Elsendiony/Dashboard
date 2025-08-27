import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ScheduleInterview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], application_id: str, interviewer_id: str,
               interview_type: str, scheduled_date: str, duration_minutes: int = 60,
               status: str = "scheduled") -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        interviews = data.get("interviews", {})
        job_applications = data.get("job_applications", {})
        users = data.get("users", {})
        
        # Validate application exists
        if str(application_id) not in job_applications:
            raise ValueError(f"Application {application_id} not found")
        
        # Validate interviewer exists
        if str(interviewer_id) not in users:
            raise ValueError(f"Interviewer {interviewer_id} not found")
        
        # Validate interview type
        valid_types = ['phone_screening', 'technical', 'behavioral', 'panel', 'final']
        if interview_type not in valid_types:
            raise ValueError(f"Invalid interview_type. Must be one of {valid_types}")
        
        # Validate status
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no_show']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        interview_id = generate_id(interviews)
        timestamp = "2025-10-01T00:00:00"
        
        new_interview = {
            "interview_id": interview_id,
            "application_id": application_id,
            "interviewer_id": interviewer_id,
            "interview_type": interview_type,
            "scheduled_date": scheduled_date,
            "duration_minutes": duration_minutes,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        interviews[interview_id] = new_interview
        return json.dumps({"interview_id": interview_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "schedule_interview",
                "description": "Schedule a new interview",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string", "description": "Application ID"},
                        "interviewer_id": {"type": "string", "description": "Interviewer user ID"},
                        "interview_type": {"type": "string", "description": "Interview type: phone_screening, technical, behavioral, panel, final"},
                        "scheduled_date": {"type": "string", "description": "ISO timestamp for interview"},
                        "duration_minutes": {"type": "integer", "description": "Duration in minutes (defaults to 60)"},
                        "status": {"type": "string", "description": "Status: scheduled, completed, cancelled, no_show (defaults to scheduled)"}
                    },
                    "required": ["application_id", "interviewer_id", "interview_type", "scheduled_date"]
                }
            }
        }
