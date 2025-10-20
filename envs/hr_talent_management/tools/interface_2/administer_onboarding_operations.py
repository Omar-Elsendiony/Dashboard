import json
import re
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AdministerOnboardingOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage employee onboarding operations including checklist creation and updates.
        
        Operations:
        - create_checklist: Create new onboarding checklist (requires employee_id, start_date, position, hiring_manager_id, user_id)
        - update_checklist: Update existing onboarding checklist (requires checklist_id and optional status fields)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                # Convert MM-DD-YYYY to YYYY-MM-DD for internal storage
                date_pattern = r'^\d{2}-\d{2}-\d{4}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be MM-DD-YYYY"
            return None
        
        def convert_date_format(date_str: str) -> str:
            """Convert MM-DD-YYYY to YYYY-MM-DD"""
            if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
                month, day, year = date_str.split('-')
                return f"{year}-{month}-{day}"
            return date_str
        
        def validate_status_field(status_value: str, field_name: str, valid_statuses: list) -> Optional[str]:
            """Validate status field against allowed values"""
            if status_value and status_value not in valid_statuses:
                return f"Invalid {field_name}. Must be one of: {', '.join(valid_statuses)}"
            return None
        
        # Validate operation_type
        valid_operations = ["create_checklist", "update_checklist"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "checklist_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "checklist_id": None,
                "message": "Invalid data format for onboarding operations"
            })
        
        onboarding_checklists = data.get("onboarding_checklists", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        if operation_type == "create_checklist":
            # Validate required fields for checklist creation
            required_fields = ["employee_id", "start_date", "position", "hiring_manager_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Missing required fields for checklist creation: {', '.join(missing_fields)}"
                })
            
            # Validate employee exists
            if str(kwargs["employee_id"]) not in employees:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Employee {kwargs['employee_id']} not found"
                })
            
            # Validate hiring manager exists
            if str(kwargs["hiring_manager_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Hiring manager {kwargs['hiring_manager_id']} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["start_date"], "start_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": date_error
                })
            
            # Check for existing checklist for this employee
            for checklist in onboarding_checklists.values():
                if checklist.get("employee_id") == str(kwargs["employee_id"]):
                    return json.dumps({
                        "success": False,
                        "checklist_id": None,
                        "message": f"Onboarding checklist already exists for employee {kwargs['employee_id']}"
                    })
            
            # Generate new checklist ID and create record
            new_checklist_id = generate_id(onboarding_checklists)
            timestamp = datetime.now().isoformat()
            
            new_checklist = {
                "checklist_id": str(new_checklist_id),
                "employee_id": str(kwargs["employee_id"]),
                "start_date": convert_date_format(kwargs["start_date"]),
                "position": kwargs["position"],
                "hiring_manager_id": str(kwargs["hiring_manager_id"]),
                "pre_onboarding_status": "pending",
                "background_check_status": "pending",
                "background_check_cleared_date": None,
                "document_verification_status": "pending",
                "it_provisioning_status": "pending",
                "orientation_completed": False,
                "orientation_date": None,
                "benefits_enrollment_status": "pending",
                "overall_status": "not_started",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            onboarding_checklists[str(new_checklist_id)] = new_checklist
            
            return json.dumps({
                "success": True,
                "checklist": new_checklist,
                "message": f"Onboarding checklist {new_checklist_id} created successfully for employee {kwargs['employee_id']}"
            })
        
        elif operation_type == "update_checklist":
            # Validate required fields for checklist update
            if "checklist_id" not in kwargs or kwargs["checklist_id"] is None:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": "checklist_id is required for checklist update"
                })
            
            # Validate checklist exists
            if str(kwargs["checklist_id"]) not in onboarding_checklists:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Checklist {kwargs['checklist_id']} not found"
                })
            
            # Validate status fields if provided
            status_validations = [
                ("pre_onboarding_status", ["pending", "in_progress", "completed"]),
                ("background_check_status", ["pending", "in_progress", "passed", "failed"]),
                ("document_verification_status", ["pending", "verified", "failed"]),
                ("it_provisioning_status", ["pending", "in_progress", "completed"]),
                ("benefits_enrollment_status", ["pending", "in_progress", "completed"]),
                ("overall_status", ["not_started", "in_progress", "completed"])
            ]
            
            for field_name, valid_statuses in status_validations:
                if field_name in kwargs and kwargs[field_name] is not None:
                    status_error = validate_status_field(kwargs[field_name], field_name, valid_statuses)
                    if status_error:
                        return json.dumps({
                            "success": False,
                            "checklist_id": None,
                            "message": status_error
                        })
            
            # Validate date fields if provided
            date_fields = ["background_check_cleared_date", "orientation_date"]
            for field_name in date_fields:
                if field_name in kwargs and kwargs[field_name] is not None:
                    date_error = validate_date_format(kwargs[field_name], field_name)
                    if date_error:
                        return json.dumps({
                            "success": False,
                            "checklist_id": None,
                            "message": date_error
                        })
            
            # Validate boolean field if provided
            if "orientation_completed" in kwargs and kwargs["orientation_completed"] is not None:
                if not isinstance(kwargs["orientation_completed"], bool):
                    return json.dumps({
                        "success": False,
                        "checklist_id": None,
                        "message": "orientation_completed must be a boolean value (True/False)"
                    })
            
            # Update checklist record
            checklist = onboarding_checklists[str(kwargs["checklist_id"])]
            
            # Define allowed update fields
            allowed_update_fields = [
                "pre_onboarding_status", "background_check_status", "background_check_cleared_date",
                "document_verification_status", "it_provisioning_status", "orientation_completed",
                "orientation_date", "benefits_enrollment_status", "overall_status"
            ]
            
            # Update only provided fields
            for field_name in allowed_update_fields:
                if field_name in kwargs and kwargs[field_name] is not None:
                    if field_name in ["background_check_cleared_date", "orientation_date"]:
                        checklist[field_name] = convert_date_format(kwargs[field_name])
                    else:
                        checklist[field_name] = kwargs[field_name]
            
            checklist["updated_at"] = "2025-10-01T12:00:00"
            
            return json.dumps({
                "success": True,
                "checklist_id": str(kwargs["checklist_id"]),
                "message": f"Onboarding checklist {kwargs['checklist_id']} updated successfully"
            })
        
        return json.dumps({
            "success": False,
            "checklist_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_onboarding_operations",
                "description": "Manage employee onboarding operations including checklist creation and updates in the HR talent management system. This tool handles the complete onboarding workflow from initial checklist creation through ongoing progress tracking and completion. For creation, establishes new onboarding checklists with comprehensive validation to ensure employee, hiring manager, and user existence before proceeding. Prevents duplicate checklist creation for the same employee. For updates, modifies existing checklist records while maintaining data integrity and enforcing proper status transitions. Validates status fields against predefined enums, ensures proper date formatting, and handles boolean field validation. Essential for onboarding process management, compliance tracking, and ensuring new employees complete all required steps. Supports the complete onboarding lifecycle from initial checklist creation through final completion tracking.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_checklist' to establish new onboarding checklist, 'update_checklist' to modify existing checklist progress",
                            "enum": ["create_checklist", "update_checklist"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee for whom the onboarding checklist is being created. Enter the employee ID as a string (e.g., '3001', '5042'). This field is required only when operation_type is 'create_checklist'. The system validates that this employee exists in the database. Only one checklist can exist per employee - the system will prevent duplicate checklist creation. Example: '4008'"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Employee's scheduled first day of work. Enter date in MM-DD-YYYY format (e.g., '04-01-2025' for April 1, 2025). This field is required only when operation_type is 'create_checklist'. Must follow the exact format MM-DD-YYYY with hyphens as separators. The system validates the date format. Used for scheduling onboarding activities and tracking timelines. Example: '05-15-2025'"
                        },
                        "position": {
                            "type": "string",
                            "description": "Employee's job position or title. Enter the position name as text (e.g., 'Software Engineer', 'Marketing Manager', 'Data Analyst'). This field is required only when operation_type is 'create_checklist'. Should match the employee's official job title. Used for position-specific onboarding requirements. Example: 'Senior Product Designer'"
                        },
                        "hiring_manager_id": {
                            "type": "string",
                            "description": "Unique identifier of the hiring manager responsible for this employee's onboarding. Enter the manager's user ID as a string (e.g., '7001', '8005'). This field is required only when operation_type is 'create_checklist'. The system validates that this user exists in the database. Used for onboarding coordination and manager notifications. Example: '6003'"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the HR user creating the onboarding checklist. Enter the user ID as a string (e.g., '5001', '9002'). This field is required only when operation_type is 'create_checklist'. The system validates that this user exists in the database. Used for audit trail to track who initiated the onboarding process. Example: '7004'"
                        },
                        "checklist_id": {
                            "type": "string",
                            "description": "Unique identifier of an existing onboarding checklist to be updated. Enter the checklist ID as a string (e.g., '101', '205'). This field is required only when operation_type is 'update_checklist'. The system validates that this checklist exists in the database. Used to identify which checklist to modify with status updates. Example: '142'"
                        },
                        "pre_onboarding_status": {
                            "type": "string",
                            "description": "Status of pre-onboarding activities completed before the start date. Select from: 'pending' for not yet started, 'in_progress' for currently being worked on, or 'completed' for finished. This field is optional and only applies when operation_type is 'update_checklist'. Must be exactly one of these three values. Pre-onboarding includes tasks like paperwork submission and equipment ordering before day one. Example: 'in_progress'",
                            "enum": ["pending", "in_progress", "completed"]
                        },
                        "background_check_status": {
                            "type": "string",
                            "description": "Status of the employment background verification process. Select from: 'pending' for not yet started, 'in_progress' for verification in process, 'passed' for successful clearance, or 'failed' for unsuccessful verification. This field is optional and only applies when operation_type is 'update_checklist'. Must be exactly one of these four values. Critical for employment authorization and compliance. Example: 'passed'",
                            "enum": ["pending", "in_progress", "passed", "failed"]
                        },
                        "background_check_cleared_date": {
                            "type": "string",
                            "description": "Date when the background check was successfully completed and cleared. Enter date in MM-DD-YYYY format (e.g., '03-10-2025' for March 10, 2025). This field is optional and only applies when operation_type is 'update_checklist'. Must follow the exact format MM-DD-YYYY with hyphens as separators. Typically set when background_check_status changes to 'passed'. Example: '04-05-2025'"
                        },
                        "document_verification_status": {
                            "type": "string",
                            "description": "Status of employment eligibility document verification (e.g., I-9 forms, work authorization). Select from: 'pending' for documents not yet verified, 'verified' for documents approved and compliant, or 'failed' for documents rejected or incomplete. This field is optional and only applies when operation_type is 'update_checklist'. Must be exactly one of these three values. Required for legal employment compliance. Example: 'verified'",
                            "enum": ["pending", "verified", "failed"]
                        },
                        "it_provisioning_status": {
                            "type": "string",
                            "description": "Status of IT equipment and access setup for the new employee. Select from: 'pending' for not yet started, 'in_progress' for equipment being prepared, or 'completed' for all IT resources ready. This field is optional and only applies when operation_type is 'update_checklist'. Must be exactly one of these three values. Includes computer, email, software licenses, and system access. Example: 'completed'",
                            "enum": ["pending", "in_progress", "completed"]
                        },
                        "orientation_completed": {
                            "type": "boolean",
                            "description": "Whether the employee has completed the company orientation program. Enter true if orientation is finished, false if not yet completed. This field is optional and only applies when operation_type is 'update_checklist'. Must be a boolean value (true or false, not as strings). Orientation typically covers company policies, culture, and introductory training. Example: true"
                        },
                        "orientation_date": {
                            "type": "string",
                            "description": "Date when the employee completed the orientation program. Enter date in MM-DD-YYYY format (e.g., '04-02-2025' for April 2, 2025). This field is optional and only applies when operation_type is 'update_checklist'. Must follow the exact format MM-DD-YYYY with hyphens as separators. Typically set when orientation_completed is marked as true. Example: '05-16-2025'"
                        },
                        "benefits_enrollment_status": {
                            "type": "string",
                            "description": "Status of employee benefits enrollment process (health insurance, retirement plans, etc.). Select from: 'pending' for enrollment not started, 'in_progress' for employee currently enrolling, or 'completed' for enrollment finished. This field is optional and only applies when operation_type is 'update_checklist'. Must be exactly one of these three values. Tracks completion of benefits selection and enrollment. Example: 'completed'",
                            "enum": ["pending", "in_progress", "completed"]
                        },
                        "overall_status": {
                            "type": "string",
                            "description": "Overall completion status of the entire onboarding process. Select from: 'not_started' for onboarding not yet begun, 'in_progress' for onboarding underway, or 'completed' for all onboarding tasks finished. This field is optional and only applies when operation_type is 'update_checklist'. Must be exactly one of these three values. Provides high-level view of onboarding progress. Example: 'in_progress'",
                            "enum": ["not_started", "in_progress", "completed"]
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
