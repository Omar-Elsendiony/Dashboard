import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class ManipulatePostIncidentReviews(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, pir_data: Dict[str, Any] = None, pir_id: str = None) -> str:
        """
        Create or update post-incident review records.

        pir_data must include:
        - action (required): 'create' or 'update'
        For create:
            - incident_id (required)
            - scheduled_date (required)
            - facilitator_id (required)
            - Optional: timeline_accuracy_rating, communication_effectiveness_rating, technical_response_rating, status
        For update:
            - pir_id (required)
            - Optional: scheduled_date, facilitator_id, timeline_accuracy_rating, communication_effectiveness_rating, technical_response_rating, status
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False, 
                "error": f"Invalid {action}. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for communications"
            })

        post_incident_reviews = data.get("post_incident_reviews", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})

        incident_id = pir_data.get("incident_id")
        scheduled_date = pir_data.get("scheduled_date")
        facilitator_id = pir_data.get("facilitator_id")
        timeline_accuracy_rating = pir_data.get("timeline_accuracy_rating")
        communication_effectiveness_rating = pir_data.get("communication_effectiveness_rating")
        technical_response_rating = pir_data.get("technical_response_rating")
        status = pir_data.get("status")

        valid_statuses = ["scheduled", "completed", "cancelled"]

        def validate_date(date_str: str) -> bool:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except (ValueError, TypeError):
                return False

        def validate_rating(rating: int) -> bool:
            return isinstance(rating, int) and 1 <= rating <= 10

        

        if action == "create":
            # Validate required fields
            if not all([incident_id, scheduled_date, facilitator_id]):
                return json.dumps({
                    "success": False,
                    "error": "incident_id, scheduled_date, and facilitator_id are required for create action"
                })

            if not validate_date(scheduled_date):
                return json.dumps({"success": False, "error": "scheduled_date must be in format YYYY-MM-DD"})

            if incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})
            if incidents[incident_id].get("status") not in ["resolved", "closed"]:
                return json.dumps({
                    "success": False,
                    "error": f"Incident must be resolved or closed, current status: {incidents[incident_id].get('status')}"
                })

            if facilitator_id not in users:
                return json.dumps({"success": False, "error": f"Facilitator {facilitator_id} not found"})
            if users[facilitator_id].get("role") not in ["incident_manager", "executive"]:
                return json.dumps({"success": False, "error": "Facilitator must have role 'incident_manager' or 'executive'"})

            # Validate ratings
            for rating_field, rating_value in [
                ("timeline_accuracy_rating", timeline_accuracy_rating),
                ("communication_effectiveness_rating", communication_effectiveness_rating),
                ("technical_response_rating", technical_response_rating)
            ]:
                if rating_value is not None and not validate_rating(rating_value):
                    return json.dumps({"success": False, "error": f"{rating_field} must be integer 1-10"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            new_pir_id = generate_id(post_incident_reviews)
            new_pir = {
                "pir_id": str(new_pir_id),
                "incident_id": incident_id,
                "scheduled_date": scheduled_date,
                "facilitator_id": facilitator_id,
                "timeline_accuracy_rating": timeline_accuracy_rating,
                "communication_effectiveness_rating": communication_effectiveness_rating,
                "technical_response_rating": technical_response_rating,
                "status": status if status else "scheduled",
                "created_at": "2025-10-02T12:00:00"
            }

            post_incident_reviews[str(new_pir_id)] = new_pir

            return json.dumps({
                "success": True, 
                "action": "create", 
                "pir_id": str(new_pir_id),
                "message": f"Post incident review {new_pir_id} created successfully", 
                "pir_data": new_pir})

        elif action == "update":
            if not pir_id:
                return json.dumps({"success": False, "error": "pir_id is required for update action"})
            if pir_id not in post_incident_reviews:
                return json.dumps({"success": False, "error": f"Post-incident review {pir_id} not found"})

            # Validate at least one optional field
            if all(field is None for field in [scheduled_date, facilitator_id, timeline_accuracy_rating,
                                               communication_effectiveness_rating, technical_response_rating, status]):
                return json.dumps({"success": False, "error": "At least one optional field must be provided for update"})

            if scheduled_date and not validate_date(scheduled_date):
                return json.dumps({"success": False, "error": "scheduled_date must be in format YYYY-MM-DD"})

            if facilitator_id:
                if facilitator_id not in users:
                    return json.dumps({"success": False, "error": f"Facilitator {facilitator_id} not found"})
                if users[facilitator_id].get("role") not in ["incident_manager", "executive"]:
                    return json.dumps({"success": False, "error": "Facilitator must have role 'incident_manager' or 'executive'"})

            for rating_field, rating_value in [
                ("timeline_accuracy_rating", timeline_accuracy_rating),
                ("communication_effectiveness_rating", communication_effectiveness_rating),
                ("technical_response_rating", technical_response_rating)
            ]:
                if rating_value is not None and not validate_rating(rating_value):
                    return json.dumps({"success": False, "error": f"{rating_field} must be integer 1-10"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            current_pir = post_incident_reviews[pir_id].copy()
            for field_name, field_value in pir_data.items():
                if field_name in ["scheduled_date", "facilitator_id", "timeline_accuracy_rating",
                                  "communication_effectiveness_rating", "technical_response_rating", "status"]:
                    if field_value is not None:
                        current_pir[field_name] = field_value

            post_incident_reviews[pir_id] = current_pir

            return json.dumps({
                "success": True, 
                "action": "update", 
                "pir_id": pir_id,
                "message": f"Post incident review {pir_id} updated successfully", 
                "pir_data": current_pir})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_post_incident_reviews",
                "description": "Create or update post-incident review (PIR) records. Supports scheduling, facilitator assignment, and rating evaluations. Validates incident status, facilitator role, ratings (1-10), and scheduled dates. Required for continuous improvement, incident analysis, and organizational learning.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["create", "update"], "description": "Action to perform"},
                        "pir_data": {
                            "type": "object",
                            "description": "Post-incident review data",
                            "properties": {
                                "incident_id": {"type": "string", "description": "Incident ID (required for create, must be resolved or closed)"},
                                "scheduled_date": {"type": "string", "description": "Scheduled date YYYY-MM-DD (required for create)"},
                                "facilitator_id": {"type": "string", "description": "Facilitator ID (required for create, must be incident_manager or executive)"},
                                "timeline_accuracy_rating": {"type": "integer", "description": "Rating 1-10 (optional)"},
                                "communication_effectiveness_rating": {"type": "integer", "description": "Rating 1-10 (optional)"},
                                "technical_response_rating": {"type": "integer", "description": "Rating 1-10 (optional)"},
                                "status": {"type": "string", "enum": ["scheduled", "completed", "cancelled"], "description": "Status (optional, default scheduled for create)"}
                            },
                        },
                        "pir_id": {"type": "string", "description": "ID of the Post incident review (required for update)"},
                    },
                    "required": ["action"]
                }
            }
        }
