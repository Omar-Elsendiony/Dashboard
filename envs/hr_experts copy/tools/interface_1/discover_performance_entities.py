import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverPerformanceEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover performance entities.
        
        Supported entities:
        - performance_reviews: Performance reviews by review_id, employee_id, reviewer_id, review_period_start, review_period_end, review_type, overall_rating, goals_achievement_score, communication_score, teamwork_score, leadership_score, technical_skills_score, status, created_at, updated_at
        """
        if entity_type not in ["performance_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'performance_reviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("performance_reviews", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "review_id": entity_id})
            else:
                results.append({**entity_data, "review_id": entity_id})
        
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
                "name": "discover_performance_entities",
                "description": "Discover performance entities. Entity types: 'performance_reviews' (performance reviews; filterable by review_id (string), employee_id (string), reviewer_id (string), review_period_start (date), review_period_end (date), review_type (enum: 'annual', 'quarterly', 'probationary', 'project_based'), overall_rating (enum: 'exceeds_expectations', 'meets_expectations', 'below_expectations', 'unsatisfactory'), goals_achievement_score (decimal), communication_score (decimal), teamwork_score (decimal), leadership_score (decimal), technical_skills_score (decimal), status (enum: 'draft', 'submitted', 'approved'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'performance_reviews'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For performance_reviews, filters are: review_id (string), employee_id (string), reviewer_id (string), review_period_start (date), review_period_end (date), review_type (enum: 'annual', 'quarterly', 'probationary', 'project_based'), overall_rating (enum: 'exceeds_expectations', 'meets_expectations', 'below_expectations', 'unsatisfactory'), goals_achievement_score (decimal), communication_score (decimal), teamwork_score (decimal), leadership_score (decimal), technical_skills_score (decimal), status (enum: 'draft', 'submitted', 'approved'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
