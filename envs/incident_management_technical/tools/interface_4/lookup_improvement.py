import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class LookupImprovement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover improvement entities (root_cause_analyses, post_incident_reviews). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - root_cause_analyses: Root Cause Analysis records
        - post_incident_reviews: Post Incident Review records
        """
        if entity_type not in ["root_cause_analyses", "post_incident_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'root_cause_analyses' or 'post_incident_reviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    if entity_type == "root_cause_analyses":
                        id_field = "rca_id"
                    else:  # post_incident_reviews
                        id_field = "review_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "root_cause_analyses":
                    id_field = "rca_id"
                else:  # post_incident_reviews
                    id_field = "review_id"
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
                "name": "lookup_improvement",
                "description": "Discover improvement entities (root cause analyses, post incident reviews). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'root_cause_analyses' or 'post_incident_reviews'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "rca_id": {
                                    "type": "string",
                                    "description": "Root cause analysis ID (for root_cause_analyses)"
                                },
                                "rca_number": {
                                    "type": "string",
                                    "description": "RCA number, e.g., RCA0001234 (for root_cause_analyses)"
                                },
                                "rca_title": {
                                    "type": "string",
                                    "description": "RCA title (for root_cause_analyses)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID (for root_cause_analyses and post_incident_reviews)."
                                },
                                "problem_ticket_id": {
                                    "type": "string",
                                    "description": "Associated problem ticket ID (for root_cause_analyses)."
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "User ID assigned to the RCA (for root_cause_analyses)"
                                },
                                "analysis_method": {
                                    "type": "string",
                                    "description": "Analysis method: '5_whys', 'fishbone', 'timeline', 'fault_tree', 'kepner_tregoe' (for root_cause_analyses)"
                                },
                                "root_cause_summary": {
                                    "type": "string",
                                    "description": "Summary of root cause findings (for root_cause_analyses)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'assigned', 'in_progress', 'completed', 'approved', 'scheduled', 'cancelled'"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Due date in YYYY-MM-DD format (for root_cause_analyses)"
                                },
                                "completed_at": {
                                    "type": "string",
                                    "description": "Completion timestamp in YYYY-MM-DD format (for root_cause_analyses)"
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User ID who approved the RCA (for root_cause_analyses)"
                                },
                                "reported_by": {
                                    "type": "string",
                                    "description": "User ID who reported (for root_cause_analyses)"
                                },
                                "review_id": {
                                    "type": "string",
                                    "description": "Post incident review ID (for post_incident_reviews)"
                                },
                                "scheduled_date": {
                                    "type": "string",
                                    "description": "Scheduled date in YYYY-MM-DD format (for post_incident_reviews)"
                                },
                                "facilitator": {
                                    "type": "string",
                                    "description": "User ID of facilitator (for post_incident_reviews)"
                                },
                                "review_notes": {
                                    "type": "string",
                                    "description": "Notes from the review (for post_incident_reviews)"
                                },
                                "lessons_learned": {
                                    "type": "string",
                                    "description": "Lessons learned (for post_incident_reviews)"
                                },
                                "action_items": {
                                    "type": "string",
                                    "description": "Action items from the review (for post_incident_reviews)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID who created (for post_incident_reviews)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for root_cause_analyses)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }