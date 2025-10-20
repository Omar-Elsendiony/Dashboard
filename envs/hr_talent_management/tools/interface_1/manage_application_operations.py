import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageApplicationOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage application operations including creation and status updates.
        
        Operations:
        - create_application: Create new job application
        - update_application_status: Update application status
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                # Accept both MM-DD-YYYY and YYYY-MM-DD formats
                date_pattern_1 = r'^\d{2}-\d{2}-\d{4}$'
                date_pattern_2 = r'^\d{4}-\d{2}-\d{2}$'
                if not (re.match(date_pattern_1, date_str) or re.match(date_pattern_2, date_str)):
                    return f"Invalid {field_name} format. Must be MM-DD-YYYY or YYYY-MM-DD"
            return None
        
        def convert_date_format(date_str: str) -> str:
            """Convert MM-DD-YYYY to YYYY-MM-DD"""
            if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
                month, day, year = date_str.split('-')
                return f"{year}-{month}-{day}"
            return date_str
        
        # Validate operation_type
        valid_operations = ["create_application", "update_application_status"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "application_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "application_id": None,
                "message": "Invalid data format for application operations"
            })
        
        applications = data.get("applications", {})
        candidates = data.get("candidates", {})
        job_postings = data.get("job_postings", {})
        documents = data.get("documents", {})
        users = data.get("users", {})
        
        if operation_type == "create_application":
            # Validate required fields
            required_fields = ["created_by", "candidate_id", "posting_id", "resume_file_id", "application_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: Missing mandatory fields ({', '.join(missing_fields)})"
                })
            
            # Validate creator exists, is active, and has appropriate role
            created_by_str = str(kwargs["created_by"])
            if created_by_str not in users:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: User not authorized"
                })
            
            creator = users[created_by_str]
            if creator.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: User not authorized"
                })
            
            valid_creator_roles = ["hr_recruiter", "hr_manager", "hr_director", "hr_admin"]
            if creator.get("role") not in valid_creator_roles:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: User not authorized"
                })
            
            # Validate candidate exists and is active
            cand_id = str(kwargs["candidate_id"])
            if cand_id not in candidates:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: Candidate not found or inactive"
                })
            
            candidate = candidates[cand_id]
            if candidate.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: Candidate not found or inactive"
                })
            
            # Validate posting exists and is active
            posting_id = str(kwargs["posting_id"])
            if posting_id not in job_postings:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: Posting not found or not in 'active' status"
                })
            
            posting = job_postings[posting_id]
            if posting.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: Posting not found or not in 'active' status"
                })
            
            # Validate resume file exists and is active
            resume_file_id = str(kwargs["resume_file_id"])
            if resume_file_id not in documents:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: Resume file not found or archived/expired"
                })
            
            resume_file = documents[resume_file_id]
            if resume_file.get("status") in ["archived", "expired"]:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Halt: Resume file not found or archived/expired"
                })
            
            # Validate cover letter file if provided
            if "cover_letter_file_id" in kwargs and kwargs["cover_letter_file_id"]:
                cover_letter_id = str(kwargs["cover_letter_file_id"])
                if cover_letter_id not in documents:
                    return json.dumps({
                        "success": False,
                        "application_id": None,
                        "message": f"Halt: Cover letter file not found or archived/expired"
                    })
                
                cover_letter_file = documents[cover_letter_id]
                if cover_letter_file.get("status") in ["archived", "expired"]:
                    return json.dumps({
                        "success": False,
                        "application_id": None,
                        "message": f"Halt: Cover letter file not found or archived/expired"
                    })
            
            # Check for duplicate application (candidate already applied to this posting)
            for check_app_id, check_app in applications.items():
                if check_app.get("candidate_id") == cand_id and check_app.get("posting_id") == posting_id:
                    return json.dumps({
                        "success": False,
                        "application_id": None,
                        "message": f"Halt: Duplicate application (candidate already applied to this posting)"
                    })
            
            # Validate date format
            date_error = validate_date_format(kwargs["application_date"], "application_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": date_error
                })
            
            # Generate new application ID and create record
            new_application_id = generate_id(applications)
            timestamp = "2025-10-10T12:00:00"
            
            new_application = {
                "application_id": str(new_application_id),
                "candidate_id": cand_id,
                "posting_id": posting_id,
                "resume_file_id": resume_file_id,
                "cover_letter_file_id": str(kwargs["cover_letter_file_id"]) if kwargs.get("cover_letter_file_id") else None,
                "application_date": convert_date_format(kwargs["application_date"]),
                "status": "applied",
                "screened_by": None,
                "screened_date": None,
                "shortlist_approved_by": None,
                "shortlist_approval_date": None,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            applications[str(new_application_id)] = new_application
            
            return json.dumps({
                "success": True,
                "application_id": str(new_application_id),
                "message": f"Application {new_application_id} created successfully"
            })
        
        elif operation_type == "update_application_status":
            # Validate required fields
            required_fields = ["application_id", "status", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Missing required fields for application status update: {', '.join(missing_fields)}"
                })
            
            # Validate application exists
            app_id = str(kwargs["application_id"])
            if app_id not in applications:
                return json.dumps({
                    "success": False,
                    "application_id": app_id,
                    "message": f"Application {app_id} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "application_id": app_id,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            application = applications[app_id]
            
            # Validate status
            valid_statuses = ["pending_review", "incomplete", "screening_passed", "shortlisted", 
                            "interview_scheduled", "interview_completed", "selected", "rejected", 
                            "offer_issued", "offer_accepted", "onboarding"]
            if kwargs["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "application_id": app_id,
                    "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Update status
            application["status"] = kwargs["status"]
            
            # Update optional fields if provided
            if "screened_date" in kwargs and kwargs["screened_date"]:
                date_error = validate_date_format(kwargs["screened_date"], "screened_date")
                if date_error:
                    return json.dumps({
                        "success": False,
                        "application_id": app_id,
                        "message": date_error
                    })
                application["screened_date"] = convert_date_format(kwargs["screened_date"])
                application["screened_by"] = str(kwargs["user_id"])
            
            if "shortlist_approval_date" in kwargs and kwargs["shortlist_approval_date"]:
                date_error = validate_date_format(kwargs["shortlist_approval_date"], "shortlist_approval_date")
                if date_error:
                    return json.dumps({
                        "success": False,
                        "application_id": app_id,
                        "message": date_error
                    })
                application["shortlist_approval_date"] = convert_date_format(kwargs["shortlist_approval_date"])
                application["shortlist_approved_by"] = str(kwargs["user_id"])
            
            return json.dumps({
                "success": True,
                "application_id": app_id,
                "message": f"Application {app_id} status updated to {kwargs['status']}"
            })
        
        return json.dumps({
            "success": False,
            "application_id": None,
            "message": "Operation not implemented"
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_application_operations",
                "description": "Manage candidate applications including creation and status updates. For create_application, system auto-generates application_id - do not provide application_id as input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Operation to perform. Values: create_application, update_application_status"
                        },
                        "created_by": {
                            "type": "string", 
                            "description": "User ID creating the application. Required for: create_application"
                        },
                        "candidate_id": {
                            "type": "string", 
                            "description": "Candidate ID. Required for: create_application"
                        },
                        "posting_id": {
                            "type": "string", 
                            "description": "Job posting ID. Required for: create_application"
                        },
                        "resume_file_id": {
                            "type": "string", 
                            "description": "Resume document ID. Required for: create_application"
                        },
                        "cover_letter_file_id": {
                            "type": "string", 
                            "description": "Cover letter document ID. Optional for: create_application"
                        },
                        "application_date": {
                            "type": "string", 
                            "description": "Application date. Format: MM-DD-YYYY or YYYY-MM-DD. Required for: create_application"
                        },
                        "application_id": {
                            "type": "string", 
                            "description": "Application ID to update (auto-generated during creation, only used for updates). Required for: update_application_status"
                        },
                        "user_id": {
                            "type": "string", 
                            "description": "User ID. Required for: update_application_status"
                        },
                        "status": {
                            "type": "string", 
                            "description": "Application status. Values: pending_review, incomplete, screening_passed, shortlisted, interview_scheduled, interview_completed, selected, rejected, offer_issued, offer_accepted, onboarding. Required for: update_application_status"
                        },
                        "screened_date": {
                            "type": "string", 
                            "description": "Screened date. Format: MM-DD-YYYY or YYYY-MM-DD. Optional for: update_application_status"
                        },
                        "shortlist_approval_date": {
                            "type": "string", 
                            "description": "Shortlist approval date. Format: MM-DD-YYYY or YYYY-MM-DD. Optional for: update_application_status"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }

