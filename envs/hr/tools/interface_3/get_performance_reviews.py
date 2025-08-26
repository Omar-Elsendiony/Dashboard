import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPerformanceReviews(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], review_id: Optional[str] = None,
               employee_id: Optional[str] = None, reviewer_id: Optional[str] = None,
               review_type: Optional[str] = None, status: Optional[str] = None) -> str:
        performance_reviews = data.get("performance_reviews", {})
        results = []
        
        for review in performance_reviews.values():
            if review_id and review.get("review_id") != review_id:
                continue
            if employee_id and review.get("employee_id") != employee_id:
                continue
            if reviewer_id and review.get("reviewer_id") != reviewer_id:
                continue
            if review_type and review.get("review_type") != review_type:
                continue
            if status and review.get("status") != status:
                continue
            results.append(review)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_performance_reviews",
                "description": "Get performance reviews with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "review_id": {"type": "string", "description": "Filter by review ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "reviewer_id": {"type": "string", "description": "Filter by reviewer ID"},
                        "review_type": {"type": "string", "description": "Filter by review type (annual, quarterly, probationary, project_based)"},
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved)"}
                    },
                    "required": []
                }
            }
        }
