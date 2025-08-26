#!/bin/bash

# Create directory for the tools
mkdir -p hr_tools_3
cd hr_tools_3

# Tool 37: get_candidates.py
cat > get_candidates.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCandidates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], candidate_id: Optional[str] = None,
               email: Optional[str] = None, source: Optional[str] = None,
               status: Optional[str] = None) -> str:
        candidates = data.get("candidates", {})
        results = []
        
        for candidate in candidates.values():
            if candidate_id and candidate.get("candidate_id") != candidate_id:
                continue
            if email and candidate.get("email", "").lower() != email.lower():
                continue
            if source and candidate.get("source") != source:
                continue
            if status and candidate.get("status") != status:
                continue
            results.append(candidate)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_candidates",
                "description": "Get candidates with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_id": {"type": "string", "description": "Filter by candidate ID"},
                        "email": {"type": "string", "description": "Filter by email address"},
                        "source": {"type": "string", "description": "Filter by source (job_board, referral, company_website, recruiter, social_media, career_fair)"},
                        "status": {"type": "string", "description": "Filter by status (new, screening, interviewing, offer, hired, rejected, withdrawn)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 38: get_job_applications.py
cat > get_job_applications.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetJobApplications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], application_id: Optional[str] = None,
               candidate_id: Optional[str] = None, position_id: Optional[str] = None,
               status: Optional[str] = None, recruiter_id: Optional[str] = None) -> str:
        job_applications = data.get("job_applications", {})
        results = []
        
        for application in job_applications.values():
            if application_id and application.get("application_id") != application_id:
                continue
            if candidate_id and application.get("candidate_id") != candidate_id:
                continue
            if position_id and application.get("position_id") != position_id:
                continue
            if status and application.get("status") != status:
                continue
            if recruiter_id and application.get("recruiter_id") != recruiter_id:
                continue
            results.append(application)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_job_applications",
                "description": "Get job applications with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string", "description": "Filter by application ID"},
                        "candidate_id": {"type": "string", "description": "Filter by candidate ID"},
                        "position_id": {"type": "string", "description": "Filter by position ID"},
                        "status": {"type": "string", "description": "Filter by status (submitted, under_review, screening, interviewing, offer_made, accepted, rejected, withdrawn)"},
                        "recruiter_id": {"type": "string", "description": "Filter by recruiter ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 39: get_interviews.py
cat > get_interviews.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInterviews(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], interview_id: Optional[str] = None,
               application_id: Optional[str] = None, interviewer_id: Optional[str] = None,
               interview_type: Optional[str] = None, status: Optional[str] = None) -> str:
        interviews = data.get("interviews", {})
        results = []
        
        for interview in interviews.values():
            if interview_id and interview.get("interview_id") != interview_id:
                continue
            if application_id and interview.get("application_id") != application_id:
                continue
            if interviewer_id and interview.get("interviewer_id") != interviewer_id:
                continue
            if interview_type and interview.get("interview_type") != interview_type:
                continue
            if status and interview.get("status") != status:
                continue
            results.append(interview)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_interviews",
                "description": "Get interviews with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "interview_id": {"type": "string", "description": "Filter by interview ID"},
                        "application_id": {"type": "string", "description": "Filter by application ID"},
                        "interviewer_id": {"type": "string", "description": "Filter by interviewer ID"},
                        "interview_type": {"type": "string", "description": "Filter by interview type (phone_screening, technical, behavioral, panel, final)"},
                        "status": {"type": "string", "description": "Filter by status (scheduled, completed, cancelled, no_show)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 40: get_payroll_records.py
cat > get_payroll_records.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPayrollRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_id: Optional[str] = None,
               employee_id: Optional[str] = None, pay_period_start: Optional[str] = None,
               pay_period_end: Optional[str] = None, status: Optional[str] = None) -> str:
        payroll_records = data.get("payroll_records", {})
        results = []
        
        for payroll in payroll_records.values():
            if payroll_id and payroll.get("payroll_id") != payroll_id:
                continue
            if employee_id and payroll.get("employee_id") != employee_id:
                continue
            if pay_period_start and payroll.get("pay_period_start") != pay_period_start:
                continue
            if pay_period_end and payroll.get("pay_period_end") != pay_period_end:
                continue
            if status and payroll.get("status") != status:
                continue
            results.append(payroll)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_records",
                "description": "Get payroll records with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "Filter by payroll ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "pay_period_start": {"type": "string", "description": "Filter by pay period start date"},
                        "pay_period_end": {"type": "string", "description": "Filter by pay period end date"},
                        "status": {"type": "string", "description": "Filter by status (draft, approved, paid, cancelled)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 41: get_employee_timesheets.py
cat > get_employee_timesheets.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmployeeTimesheets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], timesheet_id: Optional[str] = None,
               employee_id: Optional[str] = None, work_date: Optional[str] = None,
               status: Optional[str] = None) -> str:
        employee_timesheets = data.get("employee_timesheets", {})
        results = []
        
        for timesheet in employee_timesheets.values():
            if timesheet_id and timesheet.get("timesheet_id") != timesheet_id:
                continue
            if employee_id and timesheet.get("employee_id") != employee_id:
                continue
            if work_date and timesheet.get("work_date") != work_date:
                continue
            if status and timesheet.get("status") != status:
                continue
            results.append(timesheet)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_timesheets",
                "description": "Get employee timesheets with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timesheet_id": {"type": "string", "description": "Filter by timesheet ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "work_date": {"type": "string", "description": "Filter by work date"},
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved, rejected)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 42: get_benefits_plans.py
cat > get_benefits_plans.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetBenefitsPlans(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], plan_id: Optional[str] = None,
               plan_type: Optional[str] = None, status: Optional[str] = None) -> str:
        benefits_plans = data.get("benefits_plans", {})
        results = []
        
        for plan in benefits_plans.values():
            if plan_id and plan.get("plan_id") != plan_id:
                continue
            if plan_type and plan.get("plan_type") != plan_type:
                continue
            if status and plan.get("status") != status:
                continue
            results.append(plan)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_benefits_plans",
                "description": "Get benefits plans with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan_id": {"type": "string", "description": "Filter by plan ID"},
                        "plan_type": {"type": "string", "description": "Filter by plan type (health_insurance, dental, vision, life_insurance, disability, retirement_401k, pto, flexible_spending)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 43: get_employee_benefits.py
cat > get_employee_benefits.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmployeeBenefits(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], enrollment_id: Optional[str] = None,
               employee_id: Optional[str] = None, plan_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        employee_benefits = data.get("employee_benefits", {})
        results = []
        
        for benefit in employee_benefits.values():
            if enrollment_id and benefit.get("enrollment_id") != enrollment_id:
                continue
            if employee_id and benefit.get("employee_id") != employee_id:
                continue
            if plan_id and benefit.get("plan_id") != plan_id:
                continue
            if status and benefit.get("status") != status:
                continue
            results.append(benefit)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_benefits",
                "description": "Get employee benefits with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "enrollment_id": {"type": "string", "description": "Filter by enrollment ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "plan_id": {"type": "string", "description": "Filter by plan ID"},
                        "status": {"type": "string", "description": "Filter by status (active, terminated, pending)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 44: get_performance_reviews.py
cat > get_performance_reviews.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPerformanceReviews(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], review_id: Optional[str] = None,
               employee_id: Optional[str] = None, reviewer_id: Optional[str] = None,
               review_type: Optional[str] = None, status: Optional[str] = None) -> str:
        performance_reviews = data.get("performance_reviews", {})
        results = []
        
        for review in performance_reviews.values():
            if review_id and review.get("review_id") != review_id:
                continue
            if employee_id and review.get("employee_id") != employee_id:
                continue
            if reviewer_id and review.get("reviewer_id") != reviewer_id:
                continue
            if review_type and review.get("review_type") != review_type:
                continue
            if status and review.get("status") != status:
                continue
            results.append(review)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_performance_reviews",
                "description": "Get performance reviews with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "review_id": {"type": "string", "description": "Filter by review ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "reviewer_id": {"type": "string", "description": "Filter by reviewer ID"},
                        "review_type": {"type": "string", "description": "Filter by review type (annual, quarterly, probationary, project_based)"},
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 45: get_training_programs.py
cat > get_training_programs.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTrainingPrograms(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_id: Optional[str] = None,
               program_type: Optional[str] = None, mandatory: Optional[bool] = None,
               status: Optional[str] = None) -> str:
        training_programs = data.get("training_programs", {})
        results = []
        
        for program in training_programs.values():
            if program_id and program.get("program_id") != program_id:
                continue
            if program_type and program.get("program_type") != program_type:
                continue
            if mandatory is not None and program.get("mandatory") != mandatory:
                continue
            if status and program.get("status") != status:
                continue
            results.append(program)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_training_programs",
                "description": "Get training programs with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_id": {"type": "string", "description": "Filter by program ID"},
                        "program_type": {"type": "string", "description": "Filter by program type (onboarding, compliance, technical, leadership, safety, diversity, ai_ethics)"},
                        "mandatory": {"type": "boolean", "description": "Filter by mandatory flag (True/False)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, draft)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 46: get_employee_training.py
cat > get_employee_training.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmployeeTraining(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], training_record_id: Optional[str] = None,
               employee_id: Optional[str] = None, program_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        employee_training = data.get("employee_training", {})
        results = []
        
        for training in employee_training.values():
            if training_record_id and training.get("training_record_id") != training_record_id:
                continue
            if employee_id and training.get("employee_id") != employee_id:
                continue
            if program_id and training.get("program_id") != program_id:
                continue
            if status and training.get("status") != status:
                continue
            results.append(training)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_training",
                "description": "Get employee training records with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "training_record_id": {"type": "string", "description": "Filter by training record ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "program_id": {"type": "string", "description": "Filter by program ID"},
                        "status": {"type": "string", "description": "Filter by status (enrolled, in_progress, completed, failed, cancelled)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 47: get_documents.py
cat > get_documents.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetDocuments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], document_id: Optional[str] = None,
               document_type: Optional[str] = None, employee_id: Optional[str] = None,
               confidentiality_level: Optional[str] = None, status: Optional[str] = None) -> str:
        document_storage = data.get("document_storage", {})
        results = []
        
        for document in document_storage.values():
            if document_id and document.get("document_id") != document_id:
                continue
            if document_type and document.get("document_type") != document_type:
                continue
            if employee_id and document.get("employee_id") != employee_id:
                continue
            if confidentiality_level and document.get("confidentiality_level") != confidentiality_level:
                continue
            if status and document.get("status") != status:
                continue
            results.append(document)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_documents",
                "description": "Get documents with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string", "description": "Filter by document ID"},
                        "document_type": {"type": "string", "description": "Filter by document type (contract, policy, handbook, form, certificate, report, resume, offer_letter)"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "confidentiality_level": {"type": "string", "description": "Filter by confidentiality level (public, internal, confidential, restricted)"},
                        "status": {"type": "string", "description": "Filter by status (active, archived, deleted)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 48: get_audit_logs.py
cat > get_audit_logs.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAuditLogs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               action: Optional[str] = None, reference_type: Optional[str] = None,
               reference_id: Optional[str] = None, start_date: Optional[str] = None,
               end_date: Optional[str] = None) -> str:
        audit_logs = data.get("audit_logs", {})
        results = []
        
        for log in audit_logs.values():
            if user_id and log.get("user_id") != user_id:
                continue
            if action and log.get("action") != action:
                continue
            if reference_type and log.get("reference_type") != reference_type:
                continue
            if reference_id and log.get("reference_id") != reference_id:
                continue
            if start_date and log.get("timestamp", "") < start_date:
                continue
            if end_date and log.get("timestamp", "") > end_date:
                continue
            results.append(log)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_audit_logs",
                "description": "Get audit logs with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "action": {"type": "string", "description": "Filter by action type (create, read, update, delete, approve, reject)"},
                        "reference_type": {"type": "string", "description": "Filter by reference type"},
                        "reference_id": {"type": "string", "description": "Filter by reference ID"},
                        "start_date": {"type": "string", "description": "Filter by start date (ISO format)"},
                        "end_date": {"type": "string", "description": "Filter by end date (ISO format)"}
                    },
                    "required": []
                }
            }
        }
EOF

echo "All HR database tools have been created successfully!"
echo "Files created in hr_tools_3/ directory:"
ls -la hr_tools_3/

echo ""
echo "To use these tools, import them in your Python project:"
echo "from hr_tools_3.get_candidates import GetCandidates"
echo "from hr_tools_3.get_job_applications import GetJobApplications"
echo "# ... and so on"