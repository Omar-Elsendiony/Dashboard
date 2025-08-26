#!/bin/bash

# Create directory for tools if it doesn't exist
mkdir -p hr_tools

# Tool 1: create_user.py
cat > hr_tools/create_user.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], first_name: str, last_name: str, email: str, 
               phone_number: Optional[str] = None, role: str = "employee", 
               status: str = "active", mfa_enabled: bool = True,
               hr_director_approval: Optional[bool] = None, 
               it_admin_approval: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        
        # Validate required fields
        if not first_name or not last_name or not email:
            raise ValueError("First name, last name, and email are required")
        
        # Check email uniqueness
        for user in users.values():
            if user.get("email", "").lower() == email.lower():
                raise ValueError(f"Email {email} already exists")
        
        # Validate role
        valid_roles = ['hr_director', 'hr_manager', 'recruiter', 'payroll_administrator', 
                      'hiring_manager', 'finance_officer', 'it_administrator', 
                      'compliance_officer', 'employee']
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status
        valid_statuses = ['active', 'inactive', 'suspended']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check approval requirements for elevated roles
        elevated_roles = ['hr_director', 'hr_manager', 'payroll_administrator', 
                         'finance_officer', 'it_administrator', 'compliance_officer']
        if role in elevated_roles:
            if hr_director_approval is None or it_admin_approval is None:
                return json.dumps({
                    "error": "HR Director and IT Administrator approval required for elevated roles",
                    "halt": True
                })
            if not hr_director_approval or not it_admin_approval:
                return json.dumps({
                    "error": "Approval denied for elevated role creation",
                    "halt": True
                })
        
        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "role": role,
            "status": status,
            "mfa_enabled": mfa_enabled,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[user_id] = new_user
        return json.dumps({"user_id": user_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Create a new user in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "First name of the user"},
                        "last_name": {"type": "string", "description": "Last name of the user"},
                        "email": {"type": "string", "description": "Email address (must be unique)"},
                        "phone_number": {"type": "string", "description": "Phone number (optional)"},
                        "role": {"type": "string", "description": "Role: hr_director, hr_manager, recruiter, payroll_administrator, hiring_manager, finance_officer, it_administrator, compliance_officer, employee"},
                        "status": {"type": "string", "description": "Status: active, inactive, suspended (defaults to active)"},
                        "mfa_enabled": {"type": "boolean", "description": "Multi-factor authentication enabled (True/False, defaults to True)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval for elevated roles (True/False)"},
                        "it_admin_approval": {"type": "boolean", "description": "IT Administrator approval for elevated roles (True/False)"}
                    },
                    "required": ["candidate_id", "position_id", "application_date", "recruiter_id"]
                }
            }
        }
EOF

# Tool 10: update_application_stage.py
cat > hr_tools/update_application_stage.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateApplicationStage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], application_id: str, status: str,
               ai_screening_score: Optional[float] = None, screening_notes: Optional[str] = None,
               recruiter_approval: Optional[bool] = None, hiring_manager_approval: Optional[bool] = None,
               compliance_review_required: Optional[bool] = None) -> str:
        
        job_applications = data.get("job_applications", {})
        
        # Validate application exists
        if str(application_id) not in job_applications:
            raise ValueError(f"Application {application_id} not found")
        
        # Validate status
        valid_statuses = ['submitted', 'under_review', 'screening', 'interviewing', 'offer_made', 'accepted', 'rejected', 'withdrawn']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        application = job_applications[str(application_id)]
        
        # Check compliance review for automated screening
        if ai_screening_score is not None and ai_screening_score < 60 and status == 'rejected':
            if compliance_review_required is None or not compliance_review_required:
                return json.dumps({
                    "error": "Compliance review required when automated screening used for adverse action",
                    "halt": True
                })
        
        # Check approvals for certain stage transitions
        if status in ['interviewing', 'offer_made'] and recruiter_approval is None:
            return json.dumps({
                "error": "Recruiter approval required for stage transition",
                "halt": True
            })
        
        if status == 'offer_made' and hiring_manager_approval is None:
            return json.dumps({
                "error": "Hiring Manager approval required for offer stage",
                "halt": True
            })
        
        if recruiter_approval is False or hiring_manager_approval is False:
            return json.dumps({
                "error": "Approval denied for stage transition",
                "halt": True
            })
        
        # Update application
        application["status"] = status
        if ai_screening_score is not None:
            application["ai_screening_score"] = ai_screening_score
        application["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Application stage updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_application_stage",
                "description": "Update the stage/status of a job application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string", "description": "Application ID"},
                        "status": {"type": "string", "description": "New status"},
                        "ai_screening_score": {"type": "number", "description": "AI screening score 0-100 (optional)"},
                        "screening_notes": {"type": "string", "description": "Screening notes (optional)"},
                        "recruiter_approval": {"type": "boolean", "description": "Recruiter approval for stage transition (True/False)"},
                        "hiring_manager_approval": {"type": "boolean", "description": "Hiring manager approval (True/False)"},
                        "compliance_review_required": {"type": "boolean", "description": "Required if automated screening used for adverse action (True/False)"}
                    },
                    "required": ["application_id", "status"]
                }
            }
        }
EOF

# Tool 11: schedule_interview.py
cat > hr_tools/schedule_interview.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ScheduleInterview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], application_id: str, interviewer_id: str,
               interview_type: str, scheduled_date: str, duration_minutes: int = 60,
               status: str = "scheduled") -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        interviews = data.get("interviews", {})
        job_applications = data.get("job_applications", {})
        users = data.get("users", {})
        
        # Validate application exists
        if str(application_id) not in job_applications:
            raise ValueError(f"Application {application_id} not found")
        
        # Validate interviewer exists
        if str(interviewer_id) not in users:
            raise ValueError(f"Interviewer {interviewer_id} not found")
        
        # Validate interview type
        valid_types = ['phone_screening', 'technical', 'behavioral', 'panel', 'final']
        if interview_type not in valid_types:
            raise ValueError(f"Invalid interview_type. Must be one of {valid_types}")
        
        # Validate status
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no_show']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        interview_id = generate_id(interviews)
        timestamp = "2025-10-01T00:00:00"
        
        new_interview = {
            "interview_id": interview_id,
            "application_id": application_id,
            "interviewer_id": interviewer_id,
            "interview_type": interview_type,
            "scheduled_date": scheduled_date,
            "duration_minutes": duration_minutes,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        interviews[interview_id] = new_interview
        return json.dumps({"interview_id": interview_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "schedule_interview",
                "description": "Schedule a new interview",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string", "description": "Application ID"},
                        "interviewer_id": {"type": "string", "description": "Interviewer user ID"},
                        "interview_type": {"type": "string", "description": "Interview type: phone_screening, technical, behavioral, panel, final"},
                        "scheduled_date": {"type": "string", "description": "ISO timestamp for interview"},
                        "duration_minutes": {"type": "integer", "description": "Duration in minutes (defaults to 60)"},
                        "status": {"type": "string", "description": "Status: scheduled, completed, cancelled, no_show (defaults to scheduled)"}
                    },
                    "required": ["application_id", "interviewer_id", "interview_type", "scheduled_date"]
                }
            }
        }
EOF

# Tool 12: record_interview_outcome.py
cat > hr_tools/record_interview_outcome.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RecordInterviewOutcome(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], interview_id: str, overall_rating: str,
               recommendation: str, status: str = "completed",
               technical_score: Optional[float] = None, communication_score: Optional[float] = None,
               cultural_fit_score: Optional[float] = None, notes: Optional[str] = None) -> str:
        
        interviews = data.get("interviews", {})
        
        # Validate interview exists
        if str(interview_id) not in interviews:
            raise ValueError(f"Interview {interview_id} not found")
        
        # Validate overall rating
        valid_ratings = ['excellent', 'good', 'average', 'below_average', 'poor']
        if overall_rating not in valid_ratings:
            raise ValueError(f"Invalid overall_rating. Must be one of {valid_ratings}")
        
        # Validate recommendation
        valid_recommendations = ['strong_hire', 'hire', 'no_hire', 'strong_no_hire']
        if recommendation not in valid_recommendations:
            raise ValueError(f"Invalid recommendation. Must be one of {valid_recommendations}")
        
        # Validate status
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no_show']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate scores (1.0-5.0)
        for score, name in [(technical_score, "technical_score"), (communication_score, "communication_score"), (cultural_fit_score, "cultural_fit_score")]:
            if score is not None and (score < 1.0 or score > 5.0):
                raise ValueError(f"{name} must be between 1.0 and 5.0")
        
        interview = interviews[str(interview_id)]
        
        # Update interview record
        interview["overall_rating"] = overall_rating
        interview["recommendation"] = recommendation
        interview["status"] = status
        if technical_score is not None:
            interview["technical_score"] = technical_score
        if communication_score is not None:
            interview["communication_score"] = communication_score
        if cultural_fit_score is not None:
            interview["cultural_fit_score"] = cultural_fit_score
        interview["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Interview outcome recorded"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_interview_outcome",
                "description": "Record the outcome of a completed interview",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "interview_id": {"type": "string", "description": "Interview ID"},
                        "overall_rating": {"type": "string", "description": "Overall rating: excellent, good, average, below_average, poor"},
                        "technical_score": {"type": "number", "description": "Technical score 1.0-5.0 (optional)"},
                        "communication_score": {"type": "number", "description": "Communication score 1.0-5.0 (optional)"},
                        "cultural_fit_score": {"type": "number", "description": "Cultural fit score 1.0-5.0 (optional)"},
                        "notes": {"type": "string", "description": "Interview notes (optional)"},
                        "recommendation": {"type": "string", "description": "Recommendation: strong_hire, hire, no_hire, strong_no_hire"},
                        "status": {"type": "string", "description": "Updated status (defaults to completed)"}
                    },
                    "required": ["interview_id", "overall_rating", "recommendation"]
                }
            }
        }
EOF

# Tool 13: onboard_employee.py
cat > hr_tools/onboard_employee.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class OnboardEmployee(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, user_id: str, position_id: str,
               hire_date: str, employment_type: str, hr_manager_approval: bool,
               compliance_verification: bool, manager_id: Optional[str] = None,
               date_of_birth: Optional[str] = None, address: Optional[str] = None,
               emergency_contact_name: Optional[str] = None,
               emergency_contact_phone: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        users = data.get("users", {})
        job_positions = data.get("job_positions", {})
        
        # Check approvals
        if not hr_manager_approval:
            return json.dumps({
                "error": "HR Manager approval required for employee onboarding",
                "halt": True
            })
        
        if not compliance_verification:
            return json.dumps({
                "error": "Compliance verification required for eligibility documents",
                "halt": True
            })
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        # Validate manager exists if provided
        if manager_id and str(manager_id) not in employees:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate employment type
        valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
        if employment_type not in valid_types:
            raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Check if employee already exists
        if str(employee_id) in employees:
            raise ValueError(f"Employee {employee_id} already exists")
        
        timestamp = "2025-10-01T00:00:00"
        
        new_employee = {
            "employee_id": employee_id,
            "user_id": user_id,
            "position_id": position_id,
            "hire_date": hire_date,
            "employment_status": "active",
            "employment_type": employment_type,
            "manager_id": manager_id,
            "date_of_birth": date_of_birth,
            "address": address,
            "emergency_contact_name": emergency_contact_name,
            "emergency_contact_phone": emergency_contact_phone,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        employees[employee_id] = new_employee
        return json.dumps({"success": True, "message": "Employee onboarded successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "onboard_employee",
                "description": "Onboard a new employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "user_id": {"type": "string", "description": "Associated user ID"},
                        "position_id": {"type": "string", "description": "Position ID"},
                        "hire_date": {"type": "string", "description": "Hire date"},
                        "employment_type": {"type": "string", "description": "Employment type: full_time, part_time, contract, intern, temporary"},
                        "manager_id": {"type": "string", "description": "Manager employee ID (optional)"},
                        "date_of_birth": {"type": "string", "description": "Date of birth (optional)"},
                        "address": {"type": "string", "description": "Address (optional)"},
                        "emergency_contact_name": {"type": "string", "description": "Emergency contact name (optional)"},
                        "emergency_contact_phone": {"type": "string", "description": "Emergency contact phone (optional)"},
                        "hr_manager_approval": {"type": "boolean", "description": "HR Manager approval (True/False)"},
                        "compliance_verification": {"type": "boolean", "description": "Compliance verification for eligibility documents (True/False)"}
                    },
                    "required": ["employee_id", "user_id", "position_id", "hire_date", "employment_type", "hr_manager_approval", "compliance_verification"]
                }
            }
        }
EOF

# Tool 14: update_employee_profile.py
cat > hr_tools/update_employee_profile.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateEmployeeProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, position_id: Optional[str] = None,
               employment_status: Optional[str] = None, employment_type: Optional[str] = None,
               manager_id: Optional[str] = None, address: Optional[str] = None,
               emergency_contact_name: Optional[str] = None,
               emergency_contact_phone: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        
        # Validate employee exists
        if str(employee_id) not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = employees[str(employee_id)]
        
        # Validate position if provided
        if position_id and str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        # Validate manager if provided
        if manager_id and str(manager_id) not in employees:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate employment status if provided
        if employment_status:
            valid_statuses = ['active', 'terminated', 'on_leave', 'suspended']
            if employment_status not in valid_statuses:
                raise ValueError(f"Invalid employment_status. Must be one of {valid_statuses}")
        
        # Validate employment type if provided
        if employment_type:
            valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
            if employment_type not in valid_types:
                raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Update fields
        if position_id:
            employee["position_id"] = position_id
        if employment_status:
            employee["employment_status"] = employment_status
        if employment_type:
            employee["employment_type"] = employment_type
        if manager_id:
            employee["manager_id"] = manager_id
        if address:
            employee["address"] = address
        if emergency_contact_name:
            employee["emergency_contact_name"] = emergency_contact_name
        if emergency_contact_phone:
            employee["emergency_contact_phone"] = emergency_contact_phone
        
        employee["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Employee profile updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_employee_profile",
                "description": "Update an employee's profile information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "position_id": {"type": "string", "description": "Updated position ID (optional)"},
                        "employment_status": {"type": "string", "description": "Employment status: active, terminated, on_leave, suspended (optional)"},
                        "employment_type": {"type": "string", "description": "Employment type (optional)"},
                        "manager_id": {"type": "string", "description": "Updated manager employee ID (optional)"},
                        "address": {"type": "string", "description": "Updated address (optional)"},
                        "emergency_contact_name": {"type": "string", "description": "Updated emergency contact name (optional)"},
                        "emergency_contact_phone": {"type": "string", "description": "Updated emergency contact phone (optional)"}
                    },
                    "required": ["employee_id"]
                }
            }
        }
EOF

# Tool 15: offboard_employee.py
cat > hr_tools/offboard_employee.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class OffboardEmployee(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, termination_date: str,
               termination_reason: str, hr_manager_approval: bool,
               compliance_officer_approval: bool) -> str:
        
        employees = data.get("employees", {})
        
        # Check approvals
        if not hr_manager_approval:
            return json.dumps({
                "error": "HR Manager approval required for employee offboarding",
                "halt": True
            })
        
        if not compliance_officer_approval:
            return json.dumps({
                "error": "Compliance Officer approval required for employee offboarding",
                "halt": True
            })
        
        # Validate employee exists
        if str(employee_id) not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = employees[str(employee_id)]
        
        # Update employee status
        employee["employment_status"] = "terminated"
        employee["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Employee offboarded successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "offboard_employee",
                "description": "Offboard an employee (terminate employment)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "termination_date": {"type": "string", "description": "Termination date"},
                        "termination_reason": {"type": "string", "description": "Reason for termination"},
                        "hr_manager_approval": {"type": "boolean", "description": "HR Manager approval (True/False)"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval (True/False)"}
                    },
                    "required": ["employee_id", "termination_date", "termination_reason", "hr_manager_approval", "compliance_officer_approval"]
                }
            }
        }
EOFd": ["first_name", "last_name", "email", "role"]
                }
            }
        }
EOF

# Tool 2: create_department.py
cat > hr_tools/create_department.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateDepartment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_name: str, manager_id: str, 
               budget: float, status: str = "active", hr_director_approval: bool = False) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        departments = data.get("departments", {})
        employees = data.get("employees", {})
        
        # Validate required fields
        if not department_name or not manager_id:
            raise ValueError("Department name and manager ID are required")
        
        # Check HR Director approval
        if not hr_director_approval:
            return json.dumps({
                "error": "HR Director approval required for department creation",
                "halt": True
            })
        
        # Validate manager exists
        if str(manager_id) not in employees:
            raise ValueError(f"Manager with ID {manager_id} not found")
        
        # Validate status
        valid_statuses = ['active', 'inactive']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        department_id = generate_id(departments)
        timestamp = "2025-10-01T00:00:00"
        
        new_department = {
            "department_id": department_id,
            "department_name": department_name,
            "manager_id": manager_id,
            "budget": budget,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        departments[department_id] = new_department
        return json.dumps({"department_id": department_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_department",
                "description": "Create a new department",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_name": {"type": "string", "description": "Name of the department"},
                        "manager_id": {"type": "string", "description": "Employee ID of the department manager"},
                        "budget": {"type": "number", "description": "Quarterly budget"},
                        "status": {"type": "string", "description": "Status: active, inactive (defaults to active)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval required (True/False)"}
                    },
                    "required": ["department_name", "manager_id", "budget", "hr_director_approval"]
                }
            }
        }
EOF

# Tool 3: update_department.py
cat > hr_tools/update_department.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateDepartment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_id: str, hr_director_approval: bool,
               department_name: Optional[str] = None, manager_id: Optional[str] = None,
               budget: Optional[float] = None, status: Optional[str] = None) -> str:
        
        departments = data.get("departments", {})
        employees = data.get("employees", {})
        
        # Check HR Director approval
        if not hr_director_approval:
            return json.dumps({
                "error": "HR Director approval required for department updates",
                "halt": True
            })
        
        # Validate department exists
        if str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        department = departments[str(department_id)]
        
        # Validate manager exists if provided
        if manager_id and str(manager_id) not in employees:
            raise ValueError(f"Manager with ID {manager_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ['active', 'inactive']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update fields
        if department_name:
            department["department_name"] = department_name
        if manager_id:
            department["manager_id"] = manager_id
        if budget is not None:
            department["budget"] = budget
        if status:
            department["status"] = status
        
        department["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Department updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_department",
                "description": "Update an existing department",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_id": {"type": "string", "description": "ID of the department to update"},
                        "department_name": {"type": "string", "description": "Updated department name (optional)"},
                        "manager_id": {"type": "string", "description": "Updated manager employee ID (optional)"},
                        "budget": {"type": "number", "description": "Updated budget (optional)"},
                        "status": {"type": "string", "description": "Updated status: active, inactive (optional)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval required (True/False)"}
                    },
                    "required": ["department_id", "hr_director_approval"]
                }
            }
        }
EOF

# Tool 4: create_job_position.py
cat > hr_tools/create_job_position.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateJobPosition(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, department_id: str, job_level: str,
               employment_type: str, hourly_rate_min: float, hourly_rate_max: float,
               status: str = "draft", hr_director_approval: Optional[bool] = None,
               hiring_manager_approval: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})
        
        # Validate required fields
        if not all([title, department_id, job_level, employment_type]):
            raise ValueError("Title, department_id, job_level, and employment_type are required")
        
        # Validate department exists
        if str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        # Validate job level
        valid_levels = ['entry', 'junior', 'mid', 'senior', 'lead', 'manager', 'director', 'executive']
        if job_level not in valid_levels:
            raise ValueError(f"Invalid job_level. Must be one of {valid_levels}")
        
        # Validate employment type
        valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
        if employment_type not in valid_types:
            raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Validate status
        valid_statuses = ['draft', 'open', 'closed']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check approvals for publishable positions
        if status == 'open':
            if hr_director_approval is None or hiring_manager_approval is None:
                return json.dumps({
                    "error": "HR Director and Hiring Manager approval required for open positions",
                    "halt": True
                })
            if not hr_director_approval or not hiring_manager_approval:
                return json.dumps({
                    "error": "Approval denied for position publication",
                    "halt": True
                })
        
        # Validate hourly rates
        if hourly_rate_min >= hourly_rate_max:
            raise ValueError("Minimum hourly rate must be less than maximum hourly rate")
        
        position_id = generate_id(job_positions)
        timestamp = "2025-10-01T00:00:00"
        
        new_position = {
            "position_id": position_id,
            "title": title,
            "department_id": department_id,
            "job_level": job_level,
            "employment_type": employment_type,
            "hourly_rate_min": hourly_rate_min,
            "hourly_rate_max": hourly_rate_max,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        job_positions[position_id] = new_position
        return json.dumps({"position_id": position_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_job_position",
                "description": "Create a new job position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Job title"},
                        "department_id": {"type": "string", "description": "Department ID"},
                        "job_level": {"type": "string", "description": "Job level: entry, junior, mid, senior, lead, manager, director, executive"},
                        "employment_type": {"type": "string", "description": "Employment type: full_time, part_time, contract, intern, temporary"},
                        "hourly_rate_min": {"type": "number", "description": "Minimum hourly rate"},
                        "hourly_rate_max": {"type": "number", "description": "Maximum hourly rate"},
                        "status": {"type": "string", "description": "Status: draft, open, closed (defaults to draft)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval for publishable positions (True/False)"},
                        "hiring_manager_approval": {"type": "boolean", "description": "Hiring Manager approval for publishable positions (True/False)"}
                    },
                    "required": ["title", "department_id", "job_level", "employment_type", "hourly_rate_min", "hourly_rate_max"]
                }
            }
        }
EOF

# Tool 5: update_job_position.py
cat > hr_tools/update_job_position.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateJobPosition(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str, title: Optional[str] = None,
               department_id: Optional[str] = None, job_level: Optional[str] = None,
               employment_type: Optional[str] = None, hourly_rate_min: Optional[float] = None,
               hourly_rate_max: Optional[float] = None, status: Optional[str] = None,
               hr_director_approval: Optional[bool] = None,
               hiring_manager_approval: Optional[bool] = None) -> str:
        
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        position = job_positions[str(position_id)]
        
        # Validate department if provided
        if department_id and str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        # Validate job level if provided
        if job_level:
            valid_levels = ['entry', 'junior', 'mid', 'senior', 'lead', 'manager', 'director', 'executive']
            if job_level not in valid_levels:
                raise ValueError(f"Invalid job_level. Must be one of {valid_levels}")
        
        # Validate employment type if provided
        if employment_type:
            valid_types = ['full_time', 'part_time', 'contract', 'intern', 'temporary']
            if employment_type not in valid_types:
                raise ValueError(f"Invalid employment_type. Must be one of {valid_types}")
        
        # Validate status if provided
        if status:
            valid_statuses = ['draft', 'open', 'closed']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            
            # Check approvals for open positions
            if status == 'open':
                if hr_director_approval is None or hiring_manager_approval is None:
                    return json.dumps({
                        "error": "HR Director and Hiring Manager approval required for open positions",
                        "halt": True
                    })
                if not hr_director_approval or not hiring_manager_approval:
                    return json.dumps({
                        "error": "Approval denied for position publication",
                        "halt": True
                    })
        
        # Validate hourly rates if provided
        min_rate = hourly_rate_min if hourly_rate_min is not None else position.get("hourly_rate_min")
        max_rate = hourly_rate_max if hourly_rate_max is not None else position.get("hourly_rate_max")
        if min_rate and max_rate and min_rate >= max_rate:
            raise ValueError("Minimum hourly rate must be less than maximum hourly rate")
        
        # Update fields
        if title:
            position["title"] = title
        if department_id:
            position["department_id"] = department_id
        if job_level:
            position["job_level"] = job_level
        if employment_type:
            position["employment_type"] = employment_type
        if hourly_rate_min is not None:
            position["hourly_rate_min"] = hourly_rate_min
        if hourly_rate_max is not None:
            position["hourly_rate_max"] = hourly_rate_max
        if status:
            position["status"] = status
        
        position["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Position updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_job_position",
                "description": "Update an existing job position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Position ID to update"},
                        "title": {"type": "string", "description": "Updated job title (optional)"},
                        "department_id": {"type": "string", "description": "Updated department ID (optional)"},
                        "job_level": {"type": "string", "description": "Updated job level (optional)"},
                        "employment_type": {"type": "string", "description": "Updated employment type (optional)"},
                        "hourly_rate_min": {"type": "number", "description": "Updated minimum hourly rate (optional)"},
                        "hourly_rate_max": {"type": "number", "description": "Updated maximum hourly rate (optional)"},
                        "status": {"type": "string", "description": "Updated status (optional)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval for publishable positions (True/False)"},
                        "hiring_manager_approval": {"type": "boolean", "description": "Hiring Manager approval for publishable positions (True/False)"}
                    },
                    "required": ["position_id"]
                }
            }
        }
EOF

# Tool 6: post_job_opening.py
cat > hr_tools/post_job_opening.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PostJobOpening(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str) -> str:
        
        job_positions = data.get("job_positions", {})
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        position = job_positions[str(position_id)]
        
        # Check if position is in draft status
        if position.get("status") != "draft":
            raise ValueError(f"Position must be in draft status to be posted. Current status: {position.get('status')}")
        
        # Update position status to open
        position["status"] = "open"
        position["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Job posted successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "post_job_opening",
                "description": "Post a job opening by changing status from draft to open",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Position ID to post"}
                    },
                    "required": ["position_id"]
                }
            }
        }
EOF

# Tool 7: close_job_opening.py
cat > hr_tools/close_job_opening.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CloseJobOpening(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str) -> str:
        
        job_positions = data.get("job_positions", {})
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        position = job_positions[str(position_id)]
        
        # Check if position is in open status
        if position.get("status") != "open":
            raise ValueError(f"Position must be in open status to be closed. Current status: {position.get('status')}")
        
        # Update position status to closed
        position["status"] = "closed"
        position["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Job closed successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "close_job_opening",
                "description": "Close a job opening by changing status from open to closed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Position ID to close"}
                    },
                    "required": ["position_id"]
                }
            }
        }
EOF

# Tool 8: create_candidate.py
cat > hr_tools/create_candidate.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateCandidate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], first_name: str, last_name: str, email: str,
               source: str, phone_number: Optional[str] = None, address: Optional[str] = None,
               status: str = "new") -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        candidates = data.get("candidates", {})
        
        # Validate required fields
        if not all([first_name, last_name, email, source]):
            raise ValueError("First name, last name, email, and source are required")
        
        # Validate source
        valid_sources = ['job_board', 'referral', 'company_website', 'recruiter', 'social_media', 'career_fair']
        if source not in valid_sources:
            raise ValueError(f"Invalid source. Must be one of {valid_sources}")
        
        # Validate status
        valid_statuses = ['new', 'screening', 'interviewing', 'offer', 'hired', 'rejected', 'withdrawn']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        candidate_id = generate_id(candidates)
        timestamp = "2025-10-01T00:00:00"
        
        new_candidate = {
            "candidate_id": candidate_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "source": source,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        candidates[candidate_id] = new_candidate
        return json.dumps({"candidate_id": candidate_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_candidate",
                "description": "Create a new candidate record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "First name"},
                        "last_name": {"type": "string", "description": "Last name"},
                        "email": {"type": "string", "description": "Email address"},
                        "phone_number": {"type": "string", "description": "Phone number (optional)"},
                        "address": {"type": "string", "description": "Address (optional)"},
                        "source": {"type": "string", "description": "Source: job_board, referral, company_website, recruiter, social_media, career_fair"},
                        "status": {"type": "string", "description": "Status: new, screening, interviewing, offer, hired, rejected, withdrawn (defaults to new)"}
                    },
                    "required": ["first_name", "last_name", "email", "source"]
                }
            }
        }
EOF