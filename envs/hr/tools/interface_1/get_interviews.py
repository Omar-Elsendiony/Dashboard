import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInterviews(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], interview_id: Optional[str] = None,
               application_id: Optional[str] = None, interviewer_id: Optional[str] = None,
               interview_type: Optional[str] = None, status: Optional[str] = None) -> str:
        interviews = data.get("interviews", {})
        results = []
        
        for interview in interviews.values():
            if interview_id and interview.get("interview_id") != interview_id:
                continue
            if application_id and interview.get("application_id") != application_id:
                continue
            if interviewer_id and interview.get("interviewer_id") != interviewer_id:
                continue
            if interview_type and interview.get("interview_type") != interview_type:
                continue
            if status and interview.get("status") != status:
                continue
            results.append(interview)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_interviews",
                "description": "Get interviews with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "interview_id": {"type": "string", "description": "Filter by interview ID"},
                        "application_id": {"type": "string", "description": "Filter by application ID"},
                        "interviewer_id": {"type": "string", "description": "Filter by interviewer ID"},
                        "interview_type": {"type": "string", "description": "Filter by interview type (phone_screening, technical, behavioral, panel, final)"},
                        "status": {"type": "string", "description": "Filter by status (scheduled, completed, cancelled, no_show)"}
                    },
                    "required": []
                }
            }
        }
