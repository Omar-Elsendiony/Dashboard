import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RecordInterviewOutcome(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], interview_id: str, overall_rating: str,
               recommendation: str, status: str = "completed",
               technical_score: Optional[float] = None, communication_score: Optional[float] = None,
               cultural_fit_score: Optional[float] = None, notes: Optional[str] = None) -> str:
        
        interviews = data.get("interviews", {})
        
        # Validate interview exists
        if str(interview_id) not in interviews:
            raise ValueError(f"Interview {interview_id} not found")
        
        # Validate overall rating
        valid_ratings = ['excellent', 'good', 'average', 'below_average', 'poor']
        if overall_rating not in valid_ratings:
            raise ValueError(f"Invalid overall_rating. Must be one of {valid_ratings}")
        
        # Validate recommendation
        valid_recommendations = ['strong_hire', 'hire', 'no_hire', 'strong_no_hire']
        if recommendation not in valid_recommendations:
            raise ValueError(f"Invalid recommendation. Must be one of {valid_recommendations}")
        
        # Validate status
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no_show']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate scores (1.0-5.0)
        for score, name in [(technical_score, "technical_score"), (communication_score, "communication_score"), (cultural_fit_score, "cultural_fit_score")]:
            if score is not None and (score < 1.0 or score > 5.0):
                raise ValueError(f"{name} must be between 1.0 and 5.0")
        
        interview = interviews[str(interview_id)]
        
        # Update interview record
        interview["overall_rating"] = overall_rating
        interview["recommendation"] = recommendation
        interview["status"] = status
        if technical_score is not None:
            interview["technical_score"] = technical_score
        if communication_score is not None:
            interview["communication_score"] = communication_score
        if cultural_fit_score is not None:
            interview["cultural_fit_score"] = cultural_fit_score
        interview["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Interview outcome recorded"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_interview_outcome",
                "description": "Record the outcome of a completed interview",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "interview_id": {"type": "string", "description": "Interview ID"},
                        "overall_rating": {"type": "string", "description": "Overall rating: excellent, good, average, below_average, poor"},
                        "technical_score": {"type": "number", "description": "Technical score 1.0-5.0 (optional)"},
                        "communication_score": {"type": "number", "description": "Communication score 1.0-5.0 (optional)"},
                        "cultural_fit_score": {"type": "number", "description": "Cultural fit score 1.0-5.0 (optional)"},
                        "notes": {"type": "string", "description": "Interview notes (optional)"},
                        "recommendation": {"type": "string", "description": "Recommendation: strong_hire, hire, no_hire, strong_no_hire"},
                        "status": {"type": "string", "description": "Updated status (defaults to completed)"}
                    },
                    "required": ["interview_id", "overall_rating", "recommendation"]
                }
            }
        }
