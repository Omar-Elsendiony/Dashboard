import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class HandleJobOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage job operations including requisitions and postings.
        
        Operations:
        - create_requisition: Create new job requisition
        - update_requisition: Update job requisition details
        - approve_requisition: Approve job requisition
        - create_posting: Create job posting from requisition
        - update_posting: Update job posting details
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                # Accept YYYY-MM-DD format
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
            return None
        
        def convert_date_format(date_str: str) -> str:
            """Convert YYYY-MM-DD format for internal storage"""
            if date_str and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str
            return date_str
        
        # Validate operation_type
        valid_operations = ["create_requisition", "update_requisition", "approve_requisition", 
                          "create_posting", "update_posting"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "requisition_id": None,
                "posting_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "requisition_id": None,
                "posting_id": None,
                "message": "Invalid data format for job operations"
            })
        
        job_requisitions = data.get("job_requisitions", {})
        job_postings = data.get("job_postings", {})
        users = data.get("users", {})
        departments = data.get("departments", {})
        locations = data.get("locations", {})
        
        if operation_type == "create_requisition":
            # Validate required fields
            required_fields = ["job_title", "department_id", "location_id", "employment_type", 
                             "hiring_manager_id", "budgeted_salary_min", "budgeted_salary_max", "created_by"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Missing required fields for requisition creation: {', '.join(missing_fields)}"
                })
            
            # Validate user exists and is active with appropriate role
            created_by_str = str(kwargs["created_by"])
            if created_by_str not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"User {kwargs['created_by']} not found"
                })
            
            creator = users[created_by_str]
            if creator.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"User {kwargs['created_by']} is not active"
                })
            
            # Validate user has appropriate role
            valid_creator_roles = ["hr_recruiter", "hr_manager", "hr_admin", "hr_director", "department_manager"]
            if creator.get("role") not in valid_creator_roles:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"User lacks authorization. Required roles: {', '.join(valid_creator_roles)}"
                })
            
            # Validate department exists and is active
            department_id_str = str(kwargs["department_id"])
            if department_id_str not in departments:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Department {kwargs['department_id']} not found"
                })
            
            department = departments[department_id_str]
            if department.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Department {kwargs['department_id']} is not active"
                })
            
            # Validate location exists and is active
            location_id_str = str(kwargs["location_id"])
            if location_id_str not in locations:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Location {kwargs['location_id']} not found"
                })
            
            location = locations[location_id_str]
            if location.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Location {kwargs['location_id']} is not active"
                })
            
            # Validate hiring manager exists and is active
            hiring_manager_id_str = str(kwargs["hiring_manager_id"])
            if hiring_manager_id_str not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Hiring manager {kwargs['hiring_manager_id']} not found"
                })
            
            hiring_manager = users[hiring_manager_id_str]
            if hiring_manager.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Hiring manager {kwargs['hiring_manager_id']} is not active"
                })
            
            # Validate salary range
            try:
                min_salary = float(kwargs["budgeted_salary_min"])
                max_salary = float(kwargs["budgeted_salary_max"])
                if min_salary < 0 or max_salary < 0:
                    return json.dumps({
                        "success": False,
                        "requisition_id": None,
                        "message": "Salary values must be non-negative"
                    })
                if min_salary > max_salary:
                    return json.dumps({
                        "success": False,
                        "requisition_id": None,
                        "message": "Minimum salary cannot exceed maximum salary"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": "Invalid salary format"
                })
            
            # Validate employment type
            valid_employment_types = ["full_time", "part_time", "contract", "intern"]
            if kwargs["employment_type"] not in valid_employment_types:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Invalid employment_type. Must be one of: {', '.join(valid_employment_types)}"
                })
            
            # Generate new requisition ID and create record
            new_requisition_id = generate_id(job_requisitions)
            timestamp = "2025-10-10T12:00:00"
            
            new_requisition = {
                "requisition_id": str(new_requisition_id),
                "job_title": kwargs["job_title"],
                "department_id": department_id_str,
                "location_id": location_id_str,
                "employment_type": kwargs["employment_type"],
                "hiring_manager_id": hiring_manager_id_str,
                "budgeted_salary_min": float(kwargs["budgeted_salary_min"]),
                "budgeted_salary_max": float(kwargs["budgeted_salary_max"]),
                "job_description": kwargs.get("job_description", ""),
                "grade": kwargs.get("grade", ""),
                "shift_type": kwargs.get("shift_type", ""),
                "remote_indicator": kwargs.get("remote_indicator", ""),
                "status": "draft",
                "hr_manager_approver": None,
                "hr_manager_approval_date": None,
                "finance_manager_approver": None,
                "finance_manager_approval_date": None,
                "dept_head_approver": None,
                "dept_head_approval_date": None,
                "created_by": created_by_str,
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00"
            }
            
            job_requisitions[str(new_requisition_id)] = new_requisition
            
            return json.dumps({
                "success": True,
                "requisition_id": str(new_requisition_id),
                "message": f"Job requisition {new_requisition_id} created successfully"
            })
        
        elif operation_type == "update_requisition":
            # Validate required fields
            required_fields = ["requisition_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Missing required fields for requisition update: {', '.join(missing_fields)}"
                })
            
            # Validate requisition exists
            req_id = str(kwargs["requisition_id"])
            if req_id not in job_requisitions:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"Job requisition {req_id} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            requisition = job_requisitions[req_id]
            user = users[str(kwargs["user_id"])]
            
            # Handle status update separately with special validation
            if "status" in kwargs and kwargs["status"] is not None:
                new_status = kwargs["status"]
                
                # If changing status to "approved", verify all approvals are present
                if new_status == "approved":
                    # Only HR Admin or HR Director can approve
                    if user.get("role") not in ["hr_admin", "hr_director"]:
                        return json.dumps({
                            "success": False,
                            "requisition_id": req_id,
                            "message": "Only HR Admin or HR Director can change status to approved"
                        })
                    
                    # Verify requisition is in pending_approval status
                    if requisition.get("status") != "pending_approval":
                        return json.dumps({
                            "success": False,
                            "requisition_id": req_id,
                            "message": f"Cannot approve requisition in '{requisition.get('status')}' status"
                        })
                    
                    # Verify all three approvals are present with dates
                    if not requisition.get("hr_manager_approver") or not requisition.get("hr_manager_approval_date"):
                        return json.dumps({
                            "success": False,
                            "requisition_id": req_id,
                            "message": "HR Manager approval is required before changing status to approved"
                        })
                    
                    if not requisition.get("finance_manager_approver") or not requisition.get("finance_manager_approval_date"):
                        return json.dumps({
                            "success": False,
                            "requisition_id": req_id,
                            "message": "Finance Manager approval is required before changing status to approved"
                        })
                    
                    if not requisition.get("dept_head_approver") or not requisition.get("dept_head_approval_date"):
                        return json.dumps({
                            "success": False,
                            "requisition_id": req_id,
                            "message": "Department Head approval is required before changing status to approved"
                        })
                
                # Update the status
                requisition["status"] = new_status
            
            # For non-status updates, check role authorization
            valid_roles = ["hr_recruiter", "hr_manager", "hr_admin", "hr_director", "hiring_manager"]
            if user.get("role") not in valid_roles:
                return json.dumps({"success": False, "error": "Halt: User lacks authorization to perform this action"})
            
            # Update fields if provided
            updatable_fields = ["job_title", "department_id", "location_id", "employment_type", "hiring_manager_id", 
                              "budgeted_salary_min", "budgeted_salary_max", "job_description", "grade", "shift_type", "remote_indicator"]
            for field in updatable_fields:
                if kwargs.get(field) is not None:
                    requisition[field] = kwargs[field]
            
            requisition["updated_at"] = "2025-10-10T12:00:00"
            
            return json.dumps({"success": True, "requisition_id": kwargs["requisition_id"], "message": f"Requisition {kwargs['requisition_id']} updated successfully"})
        
        elif operation_type == "approve_requisition":
            # Validate required fields
            required_fields = ["requisition_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Missing required fields for requisition approval: {', '.join(missing_fields)}"
                })
            
            # Validate requisition exists
            req_id = str(kwargs["requisition_id"])
            if req_id not in job_requisitions:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"Job requisition {req_id} not found"
                })
            
            # Validate user exists
            user_id = str(kwargs["user_id"])
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"User {user_id} not found"
                })
            
            requisition = job_requisitions[req_id]
            user = users[user_id]
            user_role = user.get("role", "")
            
            # Validate requisition status
            if requisition.get("status") != "pending_approval":
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"Cannot approve requisition in '{requisition.get('status')}' status"
                })
            
            # Determine approval type based on user role
            approval_date = kwargs.get("approval_date", "2025-10-10")
            approval_date_converted = convert_date_format(approval_date)
            
            if user_role == "hr_manager":
                requisition["hr_manager_approver"] = user_id
                requisition["hr_manager_approval_date"] = approval_date_converted
            elif user_role == "finance_manager":
                requisition["finance_manager_approver"] = user_id
                requisition["finance_manager_approval_date"] = approval_date_converted
            elif user_role == "department_manager" or user_role == "hiring_manager":
                requisition["dept_head_approver"] = user_id
                requisition["dept_head_approval_date"] = approval_date_converted
            else:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"User with role '{user_role}' is not authorized to approve requisitions"
                })
            
            requisition["updated_at"] = "2025-10-10T12:00:00"
            
            # Check if all three approvals are now present
            has_all_approvals = (
                requisition.get("hr_manager_approver") and requisition.get("hr_manager_approval_date") and
                requisition.get("finance_manager_approver") and requisition.get("finance_manager_approval_date") and
                requisition.get("dept_head_approver") and requisition.get("dept_head_approval_date")
            )
            
            if has_all_approvals:
                return json.dumps({
                    "success": True,
                    "requisition_id": req_id,
                    "message": f"Job requisition {req_id} approved by {user_role}. All three approvals now complete. An HR Admin or HR Director can now change the status to 'approved' using update_requisition."
                })
            else:
                return json.dumps({
                    "success": True,
                    "requisition_id": req_id,
                    "message": f"Job requisition {req_id} approved by {user_role}. Additional approvals still required before status can be changed to 'approved'."
                })
        
        elif operation_type == "create_posting":
            # Validate required fields
            required_fields = ["requisition_id", "posted_date", "portal_type", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Missing required fields for posting creation: {', '.join(missing_fields)}"
                })
            
            # Validate requisition exists
            req_id = str(kwargs["requisition_id"])
            if req_id not in job_requisitions:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Job requisition {req_id} not found"
                })
            
            requisition = job_requisitions[req_id]
            
            # Validate requisition is approved
            if requisition.get("status") != "approved":
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Cannot create posting for requisition in '{requisition.get('status')}' status"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            # Validate portal type
            valid_portal_types = ["internal", "external", "both"]
            if kwargs["portal_type"] not in valid_portal_types:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Invalid portal_type. Must be one of: {', '.join(valid_portal_types)}"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["posted_date"], "posted_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": date_error
                })
            
            # Generate new posting ID and create record
            new_posting_id = generate_id(job_postings)
            timestamp = "2025-10-10T12:00:00"
            
            new_posting = {
                "posting_id": str(new_posting_id),
                "requisition_id": req_id,
                "posted_date": convert_date_format(kwargs["posted_date"]),
                "portal_type": kwargs["portal_type"],
                "status": "active",
                "created_at": timestamp
            }
            
            job_postings[str(new_posting_id)] = new_posting
            
            return json.dumps({
                "success": True,
                "posting_id": str(new_posting_id),
                "message": f"Job posting {new_posting_id} created successfully"
            })
        
        elif operation_type == "update_posting":
            # Validate required fields
            required_fields = ["posting_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Missing required fields for posting update: {', '.join(missing_fields)}"
                })
            
            # Validate posting exists
            posting_id = str(kwargs["posting_id"])
            if posting_id not in job_postings:
                return json.dumps({
                    "success": False,
                    "posting_id": posting_id,
                    "message": f"Job posting {posting_id} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "posting_id": posting_id,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            posting = job_postings[posting_id]
            
            # Validate posting is in updatable status
            if posting.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "posting_id": posting_id,
                    "message": f"Cannot update posting in '{posting.get('status')}' status"
                })
            
            # Update fields
            updateable_fields = ["portal_type", "status"]
            
            for field in updateable_fields:
                if field in kwargs and kwargs[field] is not None:
                    if field == "portal_type":
                        valid_portal_types = ["internal", "external", "both"]
                        if kwargs[field] not in valid_portal_types:
                            return json.dumps({
                                "success": False,
                                "posting_id": posting_id,
                                "message": f"Invalid portal_type. Must be one of: {', '.join(valid_portal_types)}"
                            })
                    elif field == "status":
                        valid_statuses = ["active", "closed", "archived"]
                        if kwargs[field] not in valid_statuses:
                            return json.dumps({
                                "success": False,
                                "posting_id": posting_id,
                                "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                            })
                    posting[field] = kwargs[field]
            
            return json.dumps({
                "success": True,
                "posting_id": posting_id,
                "message": f"Job posting {posting_id} updated successfully"
            })
        
        return json.dumps({
            "success": False,
            "requisition_id": None,
            "posting_id": None,
            "message": "Operation not implemented"
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_job_operations",
                "description": "Manage job requisitions and postings including creation, updates, approvals, and posting operations. For create_requisition and create_posting, system auto-generates IDs - do not provide requisition_id or posting_id as input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Operation to perform. Values: create_requisition, update_requisition, approve_requisition, create_posting, update_posting"
                        },
                        "requisition_id": {
                            "type": "string",
                            "description": "Requisition ID. Required for: update_requisition, approve_requisition, create_posting"
                        },
                        "posting_id": {
                            "type": "string",
                            "description": "Posting ID. Required for: update_posting"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID. Required for: update_requisition, approve_requisition, create_posting, update_posting"
                        },
                        "job_title": {
                            "type": "string",
                            "description": "Job title. Required for: create_requisition. Optional for: update_requisition"
                        },
                        "department_id": {
                            "type": "string",
                            "description": "Department ID. Required for: create_requisition. Optional for: update_requisition"
                        },
                        "location_id": {
                            "type": "string",
                            "description": "Location ID. Required for: create_requisition. Optional for: update_requisition"
                        },
                        "employment_type": {
                            "type": "string",
                            "description": "Employment type. Values: full_time, part_time, contract, intern. Required for: create_requisition. Optional for: update_requisition"
                        },
                        "hiring_manager_id": {
                            "type": "string",
                            "description": "Hiring manager user ID. Required for: create_requisition. Optional for: update_requisition"
                        },
                        "budgeted_salary_min": {
                            "type": "number",
                            "description": "Minimum budgeted salary in USD. Required for: create_requisition. Optional for: update_requisition"
                        },
                        "budgeted_salary_max": {
                            "type": "number",
                            "description": "Maximum budgeted salary in USD. Required for: create_requisition. Optional for: update_requisition"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "User ID creating the requisition. Required for: create_requisition"
                        },
                        "job_description": {
                            "type": "string",
                            "description": "Job description text. Optional for: create_requisition, update_requisition"
                        },
                        "grade": {
                            "type": "string",
                            "description": "Job grade or level. Optional for: create_requisition, update_requisition"
                        },
                        "shift_type": {
                            "type": "string",
                            "description": "Shift type. Optional for: create_requisition, update_requisition"
                        },
                        "remote_indicator": {
                            "type": "string",
                            "description": "Remote work indicator. Optional for: create_requisition, update_requisition"
                        },
                        "approval_date": {
                            "type": "string",
                            "description": "Approval date. Format: YYYY-MM-DD. Optional for: approve_requisition"
                        },
                        "posted_date": {
                            "type": "string",
                            "description": "Posting date. Format: YYYY-MM-DD. Required for: create_posting"
                        },
                        "portal_type": {
                            "type": "string",
                            "description": "Portal type. Values: internal, external, both. Required for: create_posting. Optional for: update_posting"
                        },
                        "status": {
                            "type": "string",
                            "description": "Status value. Optional for: update_requisition, update_posting"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }

