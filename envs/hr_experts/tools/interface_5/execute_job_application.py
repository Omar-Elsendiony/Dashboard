
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExecuteJobApplication(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, application_data: Dict[str, Any] = None, application_id: str = None) -> str:
        """
        Create or update job application records.
        
        Actions:
        - create: Create new application (requires candidate_id, position_id, application_date, recruiter_id)
        - update: Update existing application (requires application_id, application_data with status updates)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_future_date(date_str: str) -> bool:
            """Check if date is in future - simplified for demo"""
            # In real implementation, would compare with current date
            # For demo purposes, assume dates starting with "2026" or later are future
            return date_str.startswith("2026") or date_str.startswith("2027")
            
        def is_valid_status_transition(current_status: str, new_status: str) -> bool:
            """Validate status transitions follow proper workflow"""
            # Define the linear progression workflow
            workflow_order = ["submitted", "under_review", "screening", "interviewing", "offer_made", "accepted"]
            terminal_states = ["accepted", "rejected", "withdrawn"]
            exit_states = ["rejected", "withdrawn"]
            
            # Cannot transition from terminal states
            if current_status in terminal_states:
                return False
            
            # Can exit to rejected/withdrawn from any active stage
            if new_status in exit_states:
                return True
                
            # Cannot move backward in workflow
            if current_status in workflow_order and new_status in workflow_order:
                current_index = workflow_order.index(current_status)
                new_index = workflow_order.index(new_status)
                # Can only move forward one step or stay the same
                return new_index >= current_index and new_index <= current_index + 1
            
            return False
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for job applications"
            })
        
        applications = data.get("job_applications", {})
        candidates = data.get("candidates", {})
        job_positions = data.get("job_positions", {})
        users = data.get("users", {})
        
        if action == "create":
            if not application_data:
                return json.dumps({
                    "success": False,
                    "error": "application_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["candidate_id", "position_id", "application_date", "recruiter_id"]
            missing_fields = [field for field in required_fields if field not in application_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing or invalid inputs - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that candidate and position exist and are valid
            candidate_id = str(application_data["candidate_id"])
            if candidate_id not in candidates:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Candidate not found"
                })
            
            position_id = str(application_data["position_id"])
            if position_id not in job_positions:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Position not found"
                })
            
            # Validate that assigned recruiter exists and has recruiter role
            recruiter_id = str(application_data["recruiter_id"])
            if recruiter_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Recruiter not found"
                })
            
            recruiter = users[recruiter_id]
            if recruiter.get("role") != "recruiter":
                return json.dumps({
                    "success": False,
                    "error": f"User specified is not a recruiter"
                })
            
            # Validate that application date is not in future
            application_date = application_data["application_date"]
            if is_future_date(application_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid status transition - application date cannot be in future"
                })
            
            # Validate AI screening score if provided
            if "ai_screening_score" in application_data:
                score = application_data["ai_screening_score"]
                if score is not None and (not isinstance(score, (int, float)) or score < 0 or score > 100):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid status transition - AI screening score must be within 0-100 range"
                    })
            
            # Validate final_decision enum if provided
            if "final_decision" in application_data:
                valid_decisions = ["hire", "reject", "hold"]
                if application_data["final_decision"] not in valid_decisions:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status transition - final_decision must be one of: {', '.join(valid_decisions)}"
                    })
            
            # Validate allowed fields
            allowed_fields = ["candidate_id", "position_id", "application_date", "recruiter_id", 
                            "ai_screening_score", "final_decision", "status"]
            invalid_fields = [field for field in application_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for application creation: {', '.join(invalid_fields)}"
                })
            
            # Validate status if provided
            if "status" in application_data:
                valid_statuses = ["submitted", "under_review", "screening", "interviewing", "offer_made", "accepted", "rejected", "withdrawn"]
                if application_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status transition - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Generate new application ID
            new_app_id = generate_id(applications)
            
            # Create new application record
            new_application = {
                "application_id": str(new_app_id),
                "candidate_id": candidate_id,
                "position_id": position_id,
                "application_date": application_date,
                "status": application_data.get("status", "submitted"),  # If status is not specified during creation, set it to submitted
                "recruiter_id": recruiter_id,
                "ai_screening_score": application_data.get("ai_screening_score"),
                "final_decision": application_data.get("final_decision"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            applications[str(new_app_id)] = new_application
            
            return json.dumps({
                "success": True,
                "action": "create",
                "application_id": str(new_app_id),
                "message": f"Job application {new_app_id} created successfully",
                "application_data": new_application
            })
        
        elif action == "update":
            if not application_id:
                return json.dumps({
                    "success": False,
                    "error": "application_id is required for update action"
                })
            
            if application_id not in applications:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Application not found"
                })
            
            if not application_data:
                return json.dumps({
                    "success": False,
                    "error": "application_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["candidate_id", "position_id", "application_date", "recruiter_id", "status", "ai_screening_score", "final_decision"]
            provided_fields = [field for field in update_fields if field in application_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current application for validation
            current_application = applications[application_id]
            current_status = current_application.get("status", "submitted")
            
            # Validate allowed update fields
            invalid_fields = [field for field in application_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for application update: {', '.join(invalid_fields)}"
                })
            
            # Validate status transitions if status is being updated
            if "status" in application_data:
                new_status = application_data["status"]
                valid_statuses = ["submitted", "under_review", "screening", "interviewing", "offer_made", "accepted", "rejected", "withdrawn"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status transition - status must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Validate status transitions follow proper workflow
                if not is_valid_status_transition(current_status, new_status):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid status transition"
                    })
            
            # Validate AI screening score if provided
            if "ai_screening_score" in application_data:
                score = application_data["ai_screening_score"]
                if score is not None and (not isinstance(score, (int, float)) or score < 0 or score > 100):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Application stage management failed - AI screening score must be within 0-100 range"
                    })
            
            # Validate final_decision enum if provided
            if "final_decision" in application_data:
                valid_decisions = ["hire", "reject", "hold"]
                if application_data["final_decision"] not in valid_decisions:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Application stage management failed - final_decision must be one of: {', '.join(valid_decisions)}"
                    })
            
            # Update application record
            updated_application = current_application.copy()
            for key, value in application_data.items():
                updated_application[key] = value
            
            updated_application["updated_at"] = "2025-10-01T12:00:00"
            applications[application_id] = updated_application
            
            return json.dumps({
                "success": True,
                "action": "update",
                "application_id": application_id,
                "message": f"Job application {application_id} updated successfully",
                "application_data": updated_application
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_job_application",
                "description": "Create or update job application records in the HR recruitment system. This tool manages job applications with comprehensive validation and workflow controls. For creation, establishes new applications with proper validation of candidate/position/recruiter existence and application date requirements. For updates (stage management), modifies application status while enforcing linear workflow progression. Validates status transitions follow proper workflow (submitted → under_review → screening → interviewing → offer_made → accepted), prevents backward movement and terminal state transitions, validates AI screening scores, and ensures recruiter role verification. Essential for recruitment workflow management, candidate tracking, and maintaining accurate application records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new application, 'update' to manage application stage",
                            "enum": ["create", "update"]
                        },
                        "application_data": {
                            "type": "object",
                            "description": "Application data object. For create: requires candidate_id, position_id, application_date, recruiter_id. Optional: ai_screening_score, final_decision, status. For update: at least one of candidate_id, position_id, application_date, recruiter_id, status, ai_screening_score, final_decision. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "candidate_id": {
                                    "type": "string",
                                    "description": "Candidate identifier (required for create, must exist in system)"
                                },
                                "position_id": {
                                    "type": "string",
                                    "description": "Job position identifier (required for create, must exist in system)"
                                },
                                "application_date": {
                                    "type": "string",
                                    "description": "Application date in YYYY-MM-DD format (required for create, cannot be in future)"
                                },
                                "recruiter_id": {
                                    "type": "string",
                                    "description": "Assigned recruiter identifier (required for create, must exist and have recruiter role)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Application status (must follow linear workflow progression)",
                                    "enum": ["submitted", "under_review", "screening", "interviewing", "offer_made", "accepted", "rejected", "withdrawn"]
                                },
                                "ai_screening_score": {
                                    "type": "number",
                                    "description": "AI screening score percentage (0-100 range)"
                                },
                                "final_decision": {
                                    "type": "string",
                                    "description": "Final hiring decision",
                                    "enum": ["hire", "reject", "hold"]
                                }
                            }
                        },
                        "application_id": {
                            "type": "string",
                            "description": "Unique identifier of the job application (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
