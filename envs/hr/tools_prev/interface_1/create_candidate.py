import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateCandidate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], first_name: str, last_name: str, email: str,
               source: str, phone_number: Optional[str] = None, address: Optional[str] = None,
               status: str = "new") -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        candidates = data.get("candidates", {})
        
        # Validate required fields
        if not all([first_name, last_name, email, source]):
            raise ValueError("First name, last name, email, and source are required")
        
        # Validate source
        valid_sources = ['job_board', 'referral', 'company_website', 'recruiter', 'social_media', 'career_fair']
        if source not in valid_sources:
            raise ValueError(f"Invalid source. Must be one of {valid_sources}")
        
        # Validate status
        valid_statuses = ['new', 'screening', 'interviewing', 'offer', 'hired', 'rejected', 'withdrawn']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        candidate_id = generate_id(candidates)
        timestamp = "2025-10-01T00:00:00"
        
        new_candidate = {
            "candidate_id": candidate_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "source": source,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        candidates[candidate_id] = new_candidate
        return json.dumps({"candidate_id": candidate_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_candidate",
                "description": "Create a new candidate record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "First name"},
                        "last_name": {"type": "string", "description": "Last name"},
                        "email": {"type": "string", "description": "Email address"},
                        "phone_number": {"type": "string", "description": "Phone number (optional)"},
                        "address": {"type": "string", "description": "Address (optional)"},
                        "source": {"type": "string", "description": "Source: job_board, referral, company_website, recruiter, social_media, career_fair"},
                        "status": {"type": "string", "description": "Status: new, screening, interviewing, offer, hired, rejected, withdrawn (defaults to new)"}
                    },
                    "required": ["first_name", "last_name", "email", "source"]
                }
            }
        }
