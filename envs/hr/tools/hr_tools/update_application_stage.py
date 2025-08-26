import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateApplicationStage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], application_id: str, status: str,
               ai_screening_score: Optional[float] = None, screening_notes: Optional[str] = None,
               recruiter_approval: Optional[bool] = None, hiring_manager_approval: Optional[bool] = None,
               compliance_review_required: Optional[bool] = None) -> str:
        
        job_applications = data.get("job_applications", {})
        
        # Validate application exists
        if str(application_id) not in job_applications:
            raise ValueError(f"Application {application_id} not found")
        
        # Validate status
        valid_statuses = ['submitted', 'under_review', 'screening', 'interviewing', 'offer_made', 'accepted', 'rejected', 'withdrawn']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        application = job_applications[str(application_id)]
        
        # Check compliance review for automated screening
        if ai_screening_score is not None and ai_screening_score < 60 and status == 'rejected':
            if compliance_review_required is None or not compliance_review_required:
                return json.dumps({
                    "error": "Compliance review required when automated screening used for adverse action",
                    "halt": True
                })
        
        # Check approvals for certain stage transitions
        if status in ['interviewing', 'offer_made'] and recruiter_approval is None:
            return json.dumps({
                "error": "Recruiter approval required for stage transition",
                "halt": True
            })
        
        if status == 'offer_made' and hiring_manager_approval is None:
            return json.dumps({
                "error": "Hiring Manager approval required for offer stage",
                "halt": True
            })
        
        if recruiter_approval is False or hiring_manager_approval is False:
            return json.dumps({
                "error": "Approval denied for stage transition",
                "halt": True
            })
        
        # Update application
        application["status"] = status
        if ai_screening_score is not None:
            application["ai_screening_score"] = ai_screening_score
        application["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Application stage updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_application_stage",
                "description": "Update the stage/status of a job application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string", "description": "Application ID"},
                        "status": {"type": "string", "description": "New status"},
                        "ai_screening_score": {"type": "number", "description": "AI screening score 0-100 (optional)"},
                        "screening_notes": {"type": "string", "description": "Screening notes (optional)"},
                        "recruiter_approval": {"type": "boolean", "description": "Recruiter approval for stage transition (True/False)"},
                        "hiring_manager_approval": {"type": "boolean", "description": "Hiring manager approval (True/False)"},
                        "compliance_review_required": {"type": "boolean", "description": "Required if automated screening used for adverse action (True/False)"}
                    },
                    "required": ["application_id", "status"]
                }
            }
        }
