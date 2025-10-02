import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExecuteInterview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, interview_data: Dict[str, Any] = None, interview_id: str = None) -> str:
        """
        Create or update interview records.
        
        Actions:
        - create: Schedule new interview (requires interview_data with application_id, interviewer_id, interview_type, scheduled_date)
        - update: Record interview outcome (requires interview_id and interview_data with outcome details)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_future_datetime(datetime_str: str) -> bool:
            """Check if datetime is in future - simplified for demo"""
            # In real implementation, would compare with current datetime
            # For demo purposes, assume dates starting with "2024" or earlier are not future
            return not (datetime_str.startswith("2024") or datetime_str.startswith("2023"))
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for interviews"
            })
        
        interviews = data.get("interviews", {})
        job_applications = data.get("job_applications", {})
        users = data.get("users", {})
        
        if action == "create":
            if not interview_data:
                return json.dumps({
                    "success": False,
                    "error": "interview_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["application_id", "interviewer_id", "interview_type", "scheduled_date"]
            missing_fields = [field for field in required_fields if field not in interview_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid interview scheduling details - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that application exists
            application_id = str(interview_data["application_id"])
            if application_id not in job_applications:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Application or interviewer not found"
                })
            
            # Validate that interviewer exists
            interviewer_id = str(interview_data["interviewer_id"])
            if interviewer_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Application or interviewer not found"
                })
            
            # Validate interview_type enum according to schema
            valid_types = ["phone_screening", "technical", "behavioral", "panel", "final"]
            if interview_data["interview_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid interview type or scheduled date - interview_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate that scheduled date and time is in the future
            scheduled_date = interview_data["scheduled_date"]
            if not is_future_datetime(scheduled_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid interview type or scheduled date - scheduled date must be in the future"
                })
            
            # Validate that duration is positive time value with reasonable default
            duration_minutes = interview_data.get("duration_minutes", 60)  # Standard duration default
            if not isinstance(duration_minutes, (int, float)) or duration_minutes <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid interview scheduling details - duration must be positive"
                })
            
            # Validate only allowed fields are present for creation
            allowed_fields = ["application_id", "interviewer_id", "interview_type", "scheduled_date", 
                            "duration_minutes", "status"]
            invalid_fields = [field for field in interview_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for interview creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new interview ID
            new_interview_id = generate_id(interviews)
            
            # Create new interview record
            new_interview = {
                "interview_id": str(new_interview_id),
                "application_id": application_id,
                "interviewer_id": interviewer_id,
                "interview_type": interview_data["interview_type"],
                "scheduled_date": scheduled_date,
                "duration_minutes": duration_minutes,
                "status": interview_data.get("status", "scheduled"),  # If status is not specified, set it to scheduled
                "overall_rating": None,
                "technical_score": None,
                "communication_score": None,
                "cultural_fit_score": None,
                "recommendation": None,
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            interviews[str(new_interview_id)] = new_interview
            
            return json.dumps({
                "success": True,
                "action": "create",
                "interview_id": str(new_interview_id),
                "message": f"Interview {new_interview_id} scheduled successfully",
                "interview_data": new_interview
            })
        
        elif action == "update":
            if not interview_id:
                return json.dumps({
                    "success": False,
                    "error": "interview_id is required for update action"
                })
            
            if interview_id not in interviews:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Interview not found or invalid status"
                })
            
            if not interview_data:
                return json.dumps({
                    "success": False,
                    "error": "interview_data is required for update action"
                })
            
            # Get current interview for validation
            current_interview = interviews[interview_id]
            current_status = current_interview.get("status")
            
            # Validate that interview has scheduled or completed status
            if current_status not in ["scheduled", "completed"]:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Interview not found or invalid status"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["overall_rating", "technical_score", "communication_score", 
                           "cultural_fit_score", "recommendation", "status"]
            provided_fields = [field for field in update_fields if field in interview_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Validate only allowed fields for updates (outcome recording)
            invalid_fields = [field for field in interview_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for interview outcome recording: {', '.join(invalid_fields)}"
                })
            
            # Validate overall rating is within accepted scale if provided
            if "overall_rating" in interview_data:
                valid_ratings = ["excellent", "good", "average", "below_average", "poor"]
                if interview_data["overall_rating"] not in valid_ratings:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid rating, scores, or recommendation - overall_rating must be one of: {', '.join(valid_ratings)}"
                    })
            
            # Validate individual scores are within acceptable numeric range if provided
            score_fields = ["technical_score", "communication_score", "cultural_fit_score"]
            for score_field in score_fields:
                if score_field in interview_data:
                    score = interview_data[score_field]
                    if score is not None and (not isinstance(score, (int, float)) or score < 0 or score > 10):
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid rating, scores, or recommendation - {score_field} must be within 0-10 range"
                        })
            
            # Validate recommendation is within accepted options if provided
            if "recommendation" in interview_data:
                valid_recommendations = ["strong_hire", "hire", "no_hire", "strong_no_hire"]
                if interview_data["recommendation"] not in valid_recommendations:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid rating, scores, or recommendation - recommendation must be one of: {', '.join(valid_recommendations)}"
                    })
            
            # Validate status if provided
            if "status" in interview_data:
                valid_statuses = ["scheduled", "completed", "cancelled", "no_show"]
                if interview_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status - must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Update interview record with outcome information
            updated_interview = current_interview.copy()
            for key, value in interview_data.items():
                updated_interview[key] = value
            
            # If status is not specified, set it to completed when outcome is being recorded
            if "status" not in interview_data and any(field in interview_data for field in ["overall_rating", "recommendation"]):
                updated_interview["status"] = "completed"
            
            updated_interview["updated_at"] = "2025-10-01T12:00:00"
            interviews[interview_id] = updated_interview
            
            # Update related job application status based on interview outcome
            application_id = current_interview.get("application_id")
            if application_id and application_id in job_applications:
                application = job_applications[application_id]
                current_app_status = application.get("status")
                new_app_status = current_app_status
                
                recommendation = updated_interview.get("recommendation")
                overall_rating = updated_interview.get("overall_rating")
                interview_type = updated_interview.get("interview_type")
                
                # Update job application status based on interview outcome per policy
                if recommendation in ["strong_hire", "hire"]:
                    if current_app_status == "interviewing":
                        new_app_status = "offer_made"
                elif recommendation in ["no_hire", "strong_no_hire"]:
                    new_app_status = "rejected"
                elif not recommendation and overall_rating:
                    # When no recommendation provided, use rating
                    if overall_rating in ["poor", "below_average"]:
                        new_app_status = "rejected"
                    # excellent/good ratings remain at interviewing for potential additional interviews
                
                # Final interviews with positive recommendations automatically advance to offer_made
                if interview_type == "final" and recommendation in ["strong_hire", "hire"]:
                    new_app_status = "offer_made"
                
                # Update application status if changed
                if new_app_status != current_app_status:
                    updated_application = application.copy()
                    updated_application["status"] = new_app_status
                    updated_application["updated_at"] = "2025-10-01T12:00:00"
                    job_applications[application_id] = updated_application
            
            return json.dumps({
                "success": True,
                "action": "update",
                "interview_id": interview_id,
                "message": f"Interview {interview_id} outcome recorded successfully",
                "interview_data": updated_interview
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_interview",
                "description": "Create or update interview records in the HR recruitment system. This tool manages interview scheduling and outcome recording with comprehensive validation and workflow controls. For creation (scheduling), establishes new interviews with proper validation of application/interviewer existence, future date requirements. For updates (outcome recording), captures interview results and automatically updates related job application status based on recommendations and ratings. Validates interview types, ensures scheduled dates are in future, validates score ranges, and enforces proper status transitions. Essential for recruitment workflow management, candidate evaluation tracking, and maintaining accurate hiring records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to schedule new interview, 'update' to record interview outcome",
                            "enum": ["create", "update"]
                        },
                        "interview_data": {
                            "type": "object",
                            "description": "Interview data object. For create: requires application_id, interviewer_id, interview_type, scheduled_date. Optional: duration_minutes, status. For update: at least one of overall_rating, technical_score, communication_score, cultural_fit_score, recommendation, status. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "application_id": {
                                    "type": "string",
                                    "description": "Job application identifier (required for create, must exist in system)"
                                },
                                "interviewer_id": {
                                    "type": "string",
                                    "description": "Interviewer user identifier (required for create, must exist in system)"
                                },
                                "interview_type": {
                                    "type": "string",
                                    "description": "Type of interview being scheduled",
                                    "enum": ["phone_screening", "technical", "behavioral", "panel", "final"]
                                },
                                "scheduled_date": {
                                    "type": "string",
                                    "description": "Interview date and time in YYYY-MM-DDTHH:MM:SS format (must be in future)"
                                },
                                "duration_minutes": {
                                    "type": "integer",
                                    "description": "Interview duration in minutes (positive value, defaults to 60)"
                                },
                                "overall_rating": {
                                    "type": "string",
                                    "description": "Overall interview rating (for outcome recording)",
                                    "enum": ["excellent", "good", "average", "below_average", "poor"]
                                },
                                "technical_score": {
                                    "type": "number",
                                    "description": "Technical skills score (0-10 range, for outcome recording)"
                                },
                                "communication_score": {
                                    "type": "number",
                                    "description": "Communication skills score (0-10 range, for outcome recording)"
                                },
                                "cultural_fit_score": {
                                    "type": "number",
                                    "description": "Cultural fit score (0-10 range, for outcome recording)"
                                },
                                "recommendation": {
                                    "type": "string",
                                    "description": "Hiring recommendation (affects job application status)",
                                    "enum": ["strong_hire", "hire", "no_hire", "strong_no_hire"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Interview status",
                                    "enum": ["scheduled", "completed", "cancelled", "no_show"]
                                }
                            }
                        },
                        "interview_id": {
                            "type": "string",
                            "description": "Unique identifier of the interview (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
