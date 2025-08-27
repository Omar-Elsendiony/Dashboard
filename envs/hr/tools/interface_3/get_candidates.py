import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCandidates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], candidate_id: Optional[str] = None,
               email: Optional[str] = None, source: Optional[str] = None,
               status: Optional[str] = None) -> str:
        candidates = data.get("candidates", {})
        results = []
        
        for candidate in candidates.values():
            if candidate_id and candidate.get("candidate_id") != candidate_id:
                continue
            if email and candidate.get("email", "").lower() != email.lower():
                continue
            if source and candidate.get("source") != source:
                continue
            if status and candidate.get("status") != status:
                continue
            results.append(candidate)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_candidates",
                "description": "Get candidates with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_id": {"type": "string", "description": "Filter by candidate ID"},
                        "email": {"type": "string", "description": "Filter by email address"},
                        "source": {"type": "string", "description": "Filter by source (job_board, referral, company_website, recruiter, social_media, career_fair)"},
                        "status": {"type": "string", "description": "Filter by status (new, screening, interviewing, offer, hired, rejected, withdrawn)"}
                    },
                    "required": []
                }
            }
        }
