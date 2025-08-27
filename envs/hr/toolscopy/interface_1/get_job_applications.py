import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetJobApplications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], application_id: Optional[str] = None,
               candidate_id: Optional[str] = None, position_id: Optional[str] = None,
               status: Optional[str] = None, recruiter_id: Optional[str] = None) -> str:
        job_applications = data.get("job_applications", {})
        results = []
        
        for application in job_applications.values():
            if application_id and application.get("application_id") != application_id:
                continue
            if candidate_id and application.get("candidate_id") != candidate_id:
                continue
            if position_id and application.get("position_id") != position_id:
                continue
            if status and application.get("status") != status:
                continue
            if recruiter_id and application.get("recruiter_id") != recruiter_id:
                continue
            results.append(application)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_job_applications",
                "description": "Get job applications with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string", "description": "Filter by application ID"},
                        "candidate_id": {"type": "string", "description": "Filter by candidate ID"},
                        "position_id": {"type": "string", "description": "Filter by position ID"},
                        "status": {"type": "string", "description": "Filter by status (submitted, under_review, screening, interviewing, offer_made, accepted, rejected, withdrawn)"},
                        "recruiter_id": {"type": "string", "description": "Filter by recruiter ID"}
                    },
                    "required": []
                }
            }
        }
