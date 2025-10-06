
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExecutePerformanceReview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, review_data: Dict[str, Any] = None, review_id: str = None) -> str:
        """
        Create or update performance review records.
        
        Actions:
        - create: Create new performance review (requires review_data with employee_id, reviewer_id, review_period_start, review_period_end, review_type, overall_rating)
        - update: Update existing performance review (requires review_id, review_data)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_valid_date_order(start_date: str, end_date: str) -> bool:
            """Check if start date is before end date - simplified for demo"""
            return start_date <= end_date
            
        def is_valid_status_progression(current_status: str, new_status: str) -> bool:
            """Validate status progression follows proper workflow"""
            # Define proper progression: draft → submitted → approved
            workflow_order = ["draft", "submitted", "approved"]
            
            if current_status not in workflow_order or new_status not in workflow_order:
                return False
            
            current_index = workflow_order.index(current_status)
            new_index = workflow_order.index(new_status)
            
            # Can only move forward or stay the same
            return new_index >= current_index
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for performance reviews"
            })
        
        performance_reviews = data.get("performance_reviews", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        if action == "create":
            if not review_data:
                return json.dumps({
                    "success": False,
                    "error": "review_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["employee_id", "reviewer_id", "review_period_start", "review_period_end", "review_type", "overall_rating"]
            missing_fields = [field for field in required_fields if field not in review_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists and has active status
            employee_id = str(review_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            # Validate that reviewer exists and has active status
            reviewer_id = str(review_data["reviewer_id"])
            if reviewer_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            reviewer = users[reviewer_id]
            if reviewer.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            # Validate that review period dates are logical (start date before end date)
            review_period_start = review_data["review_period_start"]
            review_period_end = review_data["review_period_end"]
            if not is_valid_date_order(review_period_start, review_period_end):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid review period dates or type - start date must be before end date"
                })
            
            # Validate review_type is within accepted categories according to schema
            valid_types = ["annual", "quarterly", "probationary", "project_based"]
            if review_data["review_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid review period dates or type - review_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate overall_rating according to schema
            valid_ratings = ["exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"]
            if review_data["overall_rating"] not in valid_ratings:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid rating or scores - overall_rating must be one of: {', '.join(valid_ratings)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "reviewer_id", "review_period_start", "review_period_end", 
                            "review_type", "overall_rating", "goals_achievement_score", "communication_score",
                            "teamwork_score", "leadership_score", "technical_skills_score", "status"]
            invalid_fields = [field for field in review_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for performance review creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new review ID
            new_review_id = generate_id(performance_reviews)
            
            # Create performance review with required information
            new_review = {
                "review_id": str(new_review_id),
                "employee_id": employee_id,
                "reviewer_id": reviewer_id,
                "review_period_start": review_period_start,
                "review_period_end": review_period_end,
                "review_type": review_data["review_type"],
                "overall_rating": review_data["overall_rating"],
                "goals_achievement_score": review_data.get("goals_achievement_score"),
                "communication_score": review_data.get("communication_score"),
                "teamwork_score": review_data.get("teamwork_score"),
                "leadership_score": review_data.get("leadership_score"),
                "technical_skills_score": review_data.get("technical_skills_score"),
                "status": review_data.get("status", "draft"),  # If status is not specified during creation, set it to draft
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            performance_reviews[str(new_review_id)] = new_review
            
            return json.dumps({
                "success": True,
                "action": "create",
                "review_id": str(new_review_id),
                "message": f"Performance review {new_review_id} created successfully",
                "review_data": new_review
            })
        
        elif action == "update":
            if not review_id:
                return json.dumps({
                    "success": False,
                    "error": "review_id is required for update action"
                })
            
            if review_id not in performance_reviews:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Performance review not found"
                })
            
            if not review_data:
                return json.dumps({
                    "success": False,
                    "error": "review_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["employee_id", "reviewer_id", "review_period_start", "review_period_end", "review_type", "overall_rating", "goals_achievement_score", "communication_score", "teamwork_score", "leadership_score", "technical_skills_score", "status"]
            provided_fields = [field for field in update_fields if field in review_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current review for validation
            current_review = performance_reviews[review_id]
            current_status = current_review.get("status", "draft")
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in review_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for performance review update: {', '.join(invalid_fields)}"
                })
            
            # Validate status transitions follow proper workflow if status is being updated
            if "status" in review_data:
                new_status = review_data["status"]
                valid_statuses = ["draft", "submitted", "approved"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - status must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Update status through proper progression (draft to submitted to approved)
                if not is_valid_status_progression(current_status, new_status):
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - invalid status transition from {current_status} to {new_status}"
                    })
            
            # Validate overall_rating if provided
            if "overall_rating" in review_data:
                valid_ratings = ["exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"]
                if review_data["overall_rating"] not in valid_ratings:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - overall_rating must be one of: {', '.join(valid_ratings)}"
                    })
            
            # Validate review_type if provided
            if "review_type" in review_data:
                valid_types = ["annual", "quarterly", "probationary", "project_based"]
                if review_data["review_type"] not in valid_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - review_type must be one of: {', '.join(valid_types)}"
                    })
            
            # Update performance review
            updated_review = current_review.copy()
            for key, value in review_data.items():
                updated_review[key] = value
            
            updated_review["updated_at"] = "2025-10-01T12:00:00"
            performance_reviews[review_id] = updated_review
            
            return json.dumps({
                "success": True,
                "action": "update",
                "review_id": review_id,
                "message": f"Performance review {review_id} updated successfully",
                "review_data": updated_review
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_performance_review",
                "description": "Create or update performance review records in the HR system. This tool manages performance review cycles with comprehensive validation and workflow controls. For creation, establishes new performance reviews with proper validation of employee/reviewer existence, review period logic, and competency scoring. For updates, modifies existing reviews while enforcing proper status progression. Validates review types against accepted categories, ensures proper date ordering, validates rating scales, and enforces status workflow progression (draft → submitted → approved). Essential for performance management, employee development tracking, and maintaining accurate review records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new performance review, 'update' to modify existing review",
                            "enum": ["create", "update"]
                        },
                        "review_data": {
                            "type": "object",
                            "description": "Performance review data object. For create: requires employee_id, reviewer_id, review_period_start, review_period_end, review_type, overall_rating. Optional: competency scores, status. For update: at least one of employee_id, reviewer_id, review_period_start, review_period_end, review_type, overall_rating, goals_achievement_score, communication_score, teamwork_score, leadership_score, technical_skills_score, status. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "employee_id": {
                                    "type": "string",
                                    "description": "Employee identifier (required for create, must exist with active status)"
                                },
                                "reviewer_id": {
                                    "type": "string",
                                    "description": "Reviewer identifier (required for create, must exist with active status)"
                                },
                                "review_period_start": {
                                    "type": "string",
                                    "description": "Review period start date in YYYY-MM-DD format (required for create, must be before end date)"
                                },
                                "review_period_end": {
                                    "type": "string",
                                    "description": "Review period end date in YYYY-MM-DD format (required for create, must be after start date)"
                                },
                                "review_type": {
                                    "type": "string",
                                    "description": "Type of performance review (required for create)",
                                    "enum": ["annual", "quarterly", "probationary", "project_based"]
                                },
                                "overall_rating": {
                                    "type": "string",
                                    "description": "Overall performance rating (required for create)",
                                    "enum": ["exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"]
                                },
                                "goals_achievement_score": {
                                    "type": "number",
                                    "description": "Goals achievement competency score"
                                },
                                "communication_score": {
                                    "type": "number",
                                    "description": "Communication skills competency score"
                                },
                                "teamwork_score": {
                                    "type": "number",
                                    "description": "Teamwork competency score"
                                },
                                "leadership_score": {
                                    "type": "number",
                                    "description": "Leadership competency score"
                                },
                                "technical_skills_score": {
                                    "type": "number",
                                    "description": "Technical skills competency score"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Review status (follows progression: draft → submitted → approved)",
                                    "enum": ["draft", "submitted", "approved"]
                                }
                            }
                        },
                        "review_id": {
                            "type": "string",
                            "description": "Unique identifier of the performance review (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
