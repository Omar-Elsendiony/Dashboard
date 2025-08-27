import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateJobApplication(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], candidate_id: str, position_id: str,
               application_date: str, recruiter_id: str, status: str = 'submitted') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        candidates = data.get("candidates", {})
        job_positions = data.get("job_positions", {})
        users = data.get("users", {})
        job_applications = data.get("job_applications", {})
        
        # Validate candidate exists
        if str(candidate_id) not in candidates:
            raise ValueError(f"Candidate {candidate_id} not found")
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        # Validate recruiter exists
        if str(recruiter_id) not in users:
            raise ValueError(f"Recruiter {recruiter_id} not found")
        
        # Validate status
        valid_statuses = ["submitted", "under_review", "screening", "interviewing", 
                         "offer_made", "accepted", "rejected", "withdrawn"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        application_id = generate_id(job_applications)
        timestamp = "2025-10-01T00:00:00"
        
        new_application = {
            "application_id": str(application_id),
            "candidate_id": candidate_id,
            "position_id": position_id,
            "application_date": application_date,
            "status": status,
            "recruiter_id": recruiter_id,
            "ai_screening_score": None,
            "final_decision": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        job_applications[str(application_id)] = new_application
        return json.dumps({"application_id": str(application_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_job_application",
                "description": "Create a new job application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_id": {"type": "string", "description": "Candidate ID (required)"},
                        "position_id": {"type": "string", "description": "Position ID (required)"},
                        "application_date": {"type": "string", "description": "Application date (required)"},
                        "recruiter_id": {"type": "string", "description": "Recruiter user ID (required)"},
                        "status": {"type": "string", "description": "Status enum: submitted, under_review, screening, interviewing, offer_made, accepted, rejected, withdrawn (defaults to submitted)"}
                    },
                    "required": ["candidate_id", "position_id", "application_date", "recruiter_id"]
                }
            }
        }