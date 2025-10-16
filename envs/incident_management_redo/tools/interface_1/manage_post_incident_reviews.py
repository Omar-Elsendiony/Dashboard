import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManagePostIncidentReviews(Tool):
    """
    Create and update post-incident reviews for incident analysis and improvement.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        review_id: Optional[str] = None,
        incident_id: Optional[str] = None,
        reviewer_id: Optional[str] = None,
        review_type: Optional[str] = None,
        review_findings: Optional[str] = None,
        impact_assessment: Optional[str] = None,
        root_causes: Optional[list] = None,
        lessons_learned: Optional[str] = None,
        recommendations: Optional[str] = None,
        action_items: Optional[list] = None
    ) -> str:
        """
        Create or update post-incident review records.

        Actions:
        - create: Create new review (requires incident_id, reviewer_id, review_type, review_findings)
        - update: Update existing review (requires review_id and at least one field to update)
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def generate_review_number(review_id: str) -> str:
            """Generate a formatted review number."""
            return f"PIR{review_id.zfill(8)}"

        timestamp = "2025-10-01T12:00:00"
        reviews = data.get("post_incident_reviews", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        valid_review_types = ["Preliminary", "Detailed", "Final"]
        valid_statuses = ["Draft", "In_Review", "Approved", "Published"]
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": "Invalid action. Must be 'create' or 'update'"
            })

        if action == "update" and not review_id:
            return json.dumps({
                "success": False,
                "error": "review_id is required for update action"
            })

        if action == "create":
            if not all([incident_id, reviewer_id, review_type, review_findings]):
                return json.dumps({
                    "success": False,
                    "error": "incident_id, reviewer_id, review_type, and review_findings are required for create action"
                })

            # Validate incident exists
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident with ID {incident_id} not found"
                })

            # Validate user exists and is active
            if reviewer_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {reviewer_id} not found"
                })
            if users[reviewer_id]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {reviewer_id} is not active"
                })

            if review_type not in valid_review_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid review_type. Must be one of: {', '.join(valid_review_types)}"
                })

            if not review_findings.strip():
                return json.dumps({
                    "success": False,
                    "error": "review_findings cannot be empty"
                })

            new_id = generate_id(reviews)
            review_number = generate_review_number(new_id)
            new_review = {
                "review_id": new_id,
                "review_number": review_number,
                "incident_id": incident_id,
                "reviewer_id": reviewer_id,
                "review_type": review_type,
                "review_findings": review_findings,
                "impact_assessment": impact_assessment.strip() if impact_assessment else None,
                "root_causes": root_causes if root_causes else [],
                "lessons_learned": lessons_learned.strip() if lessons_learned else None,
                "recommendations": recommendations.strip() if recommendations else None,
                "action_items": action_items if action_items else [],
                "review_status": "Draft",
                "created_at": timestamp,
                "updated_at": timestamp,
                "last_modified_by": reviewer_id,
                "version": 1,
                "contributors": [reviewer_id]
            }
            reviews[new_id] = new_review

            return json.dumps({
                "success": True,
                "action": "create",
                "review_id": new_id,
                "review_number": review_number,
                "review_data": new_review
            })

        if action == "update":
            if review_id not in reviews:
                return json.dumps({
                    "success": False,
                    "error": f"Review with ID {review_id} not found"
                })

            # Validate at least one field is being updated
            update_fields = [
                review_type, review_findings, impact_assessment,
                root_causes, lessons_learned, recommendations, action_items
            ]
            if all(v is None for v in update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })

            existing_review = reviews[review_id]

            if reviewer_id is not None:
                if reviewer_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {reviewer_id} not found"
                    })
                if users[reviewer_id]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {reviewer_id} is not active"
                    })

            if review_type is not None:
                if review_type not in valid_review_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid review_type. Must be one of: {', '.join(valid_review_types)}"
                    })
                existing_review["review_type"] = review_type

            if review_findings is not None:
                if not review_findings.strip():
                    return json.dumps({
                        "success": False,
                        "error": "review_findings cannot be empty"
                    })
                existing_review["review_findings"] = review_findings.strip()
                existing_review["version"] += 1

            if impact_assessment is not None:
                existing_review["impact_assessment"] = impact_assessment.strip()

            if root_causes is not None:
                existing_review["root_causes"] = root_causes

            if lessons_learned is not None:
                existing_review["lessons_learned"] = lessons_learned.strip()

            if recommendations is not None:
                existing_review["recommendations"] = recommendations.strip()

            if action_items is not None:
                existing_review["action_items"] = action_items

            if reviewer_id is not None:
                existing_review["last_modified_by"] = reviewer_id
                if reviewer_id not in existing_review["contributors"]:
                    existing_review["contributors"].append(reviewer_id)

            existing_review["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "action": "update",
                "review_id": review_id,
                "review_number": existing_review["review_number"],
                "review_data": existing_review
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns comprehensive information about the tool's capabilities, parameters, and data schema.
        """
        return {
            "type": "function",
            "function": {
                "name": "manage_post_incident_reviews",
                "description": "Create/update post-incident reviews for formal analysis of incidents and identification of improvements. Actions: 'create' (requires incident_id, reviewer_id, review_type, review_findings; optional: impact_assessment, root_causes, lessons_learned, recommendations, action_items), 'update' (requires review_id; optional: review_type, review_findings, impact_assessment, root_causes, lessons_learned, recommendations, action_items, reviewer_id).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "review_id": {
                            "type": "string",
                            "description": "Required for update. ID of the review to update"
                        },
                        "incident_id": {
                            "type": "string",
                            "description": "Required for create. ID of the incident being reviewed"
                        },
                        "reviewer_id": {
                            "type": "string",
                            "description": "ID of the active primary reviewer"
                        },
                        "review_type": {
                            "type": "string",
                            "description": "Type of review: Preliminary (initial quick review), Detailed (comprehensive analysis), Final (complete review)",
                            "enum": ["Preliminary", "Detailed", "Final"]
                        },
                        "review_findings": {
                            "type": "string",
                            "description": "Primary findings and observations from the review (must not be empty)"
                        },
                        "impact_assessment": {
                            "type": "string",
                            "description": "Analysis of incident's impact on business, users, and systems"
                        },
                        "root_causes": {
                            "type": "array",
                            "description": "List of identified root causes (array of strings)",
                            "items": {"type": "string"}
                        },
                        "lessons_learned": {
                            "type": "string",
                            "description": "Key learnings and insights from the incident"
                        },
                        "recommendations": {
                            "type": "string",
                            "description": "Suggested improvements and preventive measures"
                        },
                        "action_items": {
                            "type": "array",
                            "description": "List of specific tasks to implement recommendations",
                            "items": {"type": "object"}
                        }
                    },
                    "required": ["action"]
                }
            }
        }