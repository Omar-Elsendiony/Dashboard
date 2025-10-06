import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class FindRecruitmentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Uretrieve recruitment entities.
        
        Supported entities:
        - candidates: Candidate records by candidate_id, first_name, last_name, email, phone_number, address, source, status, created_at, updated_at
        - job_applications: Job application records by application_id, candidate_id, position_id, application_date, status, recruiter_id, ai_screening_score, final_decision, created_at, updated_at
        - interviews: Interview records by interview_id, application_id, interviewer_id, interview_type, scheduled_date, duration_minutes, status, overall_rating, technical_score, communication_score, cultural_fit_score, recommendation, created_at, updated_at
        """
        if entity_type not in ["candidates", "job_applications", "interviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: 'candidates', 'job_applications', 'interviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        # Determine ID field based on entity type
        id_field_map = {
            "candidates": "candidate_id",
            "job_applications": "application_id", 
            "interviews": "interview_id"
        }
        id_field = id_field_map[entity_type]
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_recruitment_entities",
                "description": "Uretrieve recruitment entities. Entity types: 'candidates' (candidate records; filterable by candidate_id (string), first_name (string), last_name (string), email (string), phone_number (string), address (string), source (enum: 'job_board', 'referral', 'company_website', 'recruiter', 'social_media', 'career_fair'), status (enum: 'new', 'screening', 'interviewing', 'offer', 'hired', 'rejected', 'withdrawn'), created_at (timestamp), updated_at (timestamp)), 'job_applications' (job application records; filterable by application_id (string), candidate_id (string), position_id (string), application_date (date), status (enum: 'submitted', 'under_review', 'screening', 'interviewing', 'offer_made', 'accepted', 'rejected', 'withdrawn'), recruiter_id (string), ai_screening_score (decimal), final_decision (enum: 'hire', 'reject', 'hold'), created_at (timestamp), updated_at (timestamp)), 'interviews' (interview records; filterable by interview_id (string), application_id (string), interviewer_id (string), interview_type (enum: 'phone_screening', 'technical', 'behavioral', 'panel', 'final'), scheduled_date (timestamp), duration_minutes (integer), status (enum: 'scheduled', 'completed', 'cancelled', 'no_show'), overall_rating (enum: 'excellent', 'good', 'average', 'below_average', 'poor'), technical_score (decimal), communication_score (decimal), cultural_fit_score (decimal), recommendation (enum: 'strong_hire', 'hire', 'no_hire', 'strong_no_hire'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'candidates', 'job_applications', or 'interviews'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For candidates: candidate_id (string), first_name (string), last_name (string), email (string), phone_number (string), address (string), source (enum: 'job_board', 'referral', 'company_website', 'recruiter', 'social_media', 'career_fair'), status (enum: 'new', 'screening', 'interviewing', 'offer', 'hired', 'rejected', 'withdrawn'), created_at (timestamp), updated_at (timestamp). For job_applications: application_id (string), candidate_id (string), position_id (string), application_date (date), status (enum: 'submitted', 'under_review', 'screening', 'interviewing', 'offer_made', 'accepted', 'rejected', 'withdrawn'), recruiter_id (string), ai_screening_score (decimal), final_decision (enum: 'hire', 'reject', 'hold'), created_at (timestamp), updated_at (timestamp). For interviews: interview_id (string), application_id (string), interviewer_id (string), interview_type (enum: 'phone_screening', 'technical', 'behavioral', 'panel', 'final'), scheduled_date (timestamp), duration_minutes (integer), status (enum: 'scheduled', 'completed', 'cancelled', 'no_show'), overall_rating (enum: 'excellent', 'good', 'average', 'below_average', 'poor'), technical_score (decimal), communication_score (decimal), cultural_fit_score (decimal), recommendation (enum: 'strong_hire', 'hire', 'no_hire', 'strong_no_hire'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
