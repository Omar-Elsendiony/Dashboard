tasks = [
    {
        "annotator": 0,
        "user_id": "hr_director_001",
        "instruction": (
            "You are Sarah Thompson, an HR Director with the email 'sarah.thompson@company.com'. You need to "
            "oversee a complete talent acquisition process. First, create a new job position for a Software Engineer "
            "in the Engineering department, then post the job opening. After that, create a candidate record for "
            "John Smith who applied through LinkedIn, create their job application, and schedule an interview. "
            "Finally, record the interview outcome and add an audit trail for all operations."
        ),
        "actions": [
            {"name": "get_departments", "arguments": {}},
            {"name": "create_job_position", "arguments": {
                "title": "Senior Software Engineer",
                "department_id": "dept_eng_01",
                "description": "Develop and maintain scalable web applications",
                "salary_min": 80000,
                "salary_max": 120000,
                "status": "draft",
                "required_skills": ["Python", "JavaScript", "React"],
                "hr_director_approval": True
            }},
            {"name": "post_job_opening", "arguments": {
                "position_id": "pos_001",
                "hr_director_approval": True
            }},
            {"name": "create_candidate", "arguments": {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@email.com",
                "phone": "+1-555-0123",
                "source": "LinkedIn"
            }},
            {"name": "create_job_application", "arguments": {
                "candidate_id": "cand_001",
                "position_id": "pos_001",
                "recruiter_id": "rec_001",
                "cover_letter": "I am excited to apply for this position..."
            }},
            {"name": "schedule_interview", "arguments": {
                "application_id": "app_001",
                "interviewer_id": "usr_002",
                "interview_date": "2025-09-01",
                "interview_time": "10:00:00",
                "duration_minutes": 60
            }},
            {"name": "record_interview_outcome", "arguments": {
                "interview_id": "int_001",
                "outcome": "passed",
                "technical_rating": 4,
                "communication_rating": 5,
                "cultural_fit_rating": 4,
                "notes": "Strong technical skills and good cultural fit"
            }},
            {"name": "create_audit_log", "arguments": {
                "user_id": "hr_director_001",
                "table_name": "job_positions",
                "action_type": "create",
                "record_id": "pos_001"
            }}
        ],
    },
    {
        "annotator": 1,
        "user_id": "hr_manager_001",
        "instruction": (
            "You are Michael Chen, an HR Manager with the email 'michael.chen@company.com'. You need to "
            "onboard a new employee and manage their initial setup. First, create a user account for the new "
            "employee Diana Stone, then process her onboarding with all required documentation. After that, "
            "create a department record for the new HR Analytics team, submit her first timesheet entry, "
            "and create a training program for new employee orientation."
        ),
        "actions": [
            {"name": "get_users", "arguments": {"role": "employee"}},
            {"name": "create_user", "arguments": {
                "first_name": "Diana",
                "last_name": "Stone",
                "email": "diana.stone@company.com",
                "role": "employee",
                "timezone": "America/New_York",
                "locale": "en-US",
                "hr_director_approval": True
            }},
            {"name": "create_worker", "arguments": {
                "user_id": "usr_003",
                "organization_id": "org_001",
                "type": "employee",
                "start_date": "2025-09-01",
                "position": "HR Analyst",
                "salary": 65000,
                "hr_manager_approval": True,
                "compliance_verification": True
            }},
            {"name": "create_department", "arguments": {
                "name": "HR Analytics",
                "manager_id": "usr_002",
                "budget": 500000,
                "location": "New York Office",
                "hr_director_approval": True
            }},
            {"name": "submit_timesheet", "arguments": {
                "employee_id": "emp_003",
                "work_date": "2025-09-02",
                "clock_in": "09:00:00",
                "clock_out": "17:30:00",
                "break_minutes": 60
            }},
            {"name": "create_training_program", "arguments": {
                "name": "New Employee Orientation",
                "description": "Comprehensive orientation program for new hires",
                "duration_hours": 8,
                "mandatory": True,
                "expiry_months": 12,
                "status": "active"
            }},
            {"name": "create_audit_log", "arguments": {
                "user_id": "hr_manager_001",
                "table_name": "workers",
                "action_type": "create",
                "record_id": "emp_003"
            }}
        ],
    },
    {
        "annotator": 2,
        "user_id": "payroll_admin_001",
        "instruction": (
            "You are Jessica Rodriguez, a Payroll Administrator with the email 'jessica.rodriguez@company.com'. "
            "You need to process payroll for the current period. First, get time entries for an employee, "
            "validate their timesheet, then process their payroll run including gross pay calculation and deductions. "
            "After that, create an expense reimbursement for their business travel and update the reimbursement status."
        ),
        "actions": [
            {"name": "get_time_entries", "arguments": {
                "employee_id": "emp_003",
                "start_date": "2025-09-01",
                "end_date": "2025-09-15"
            }},
            {"name": "approve_timesheet", "arguments": {
                "timesheet_id": "ts_001",
                "approver_id": "payroll_admin_001",
                "status": "approved"
            }},
            {"name": "process_payroll_run", "arguments": {
                "employee_id": "emp_003",
                "pay_period_start": "2025-09-01",
                "pay_period_end": "2025-09-15",
                "total_hours": 80,
                "hourly_rate": 31.25,
                "finance_officer_approval": True
            }},
            {"name": "insert_payroll_deduction", "arguments": {
                "payroll_id": "pay_001",
                "deduction_type": "federal_tax",
                "amount": 400.00,
                "description": "Federal income tax"
            }},
            {"name": "create_expense_reimbursement", "arguments": {
                "employee_id": "emp_003",
                "amount": 250.00,
                "currency": "USD",
                "description": "Business travel expenses",
                "receipt_file_path": "/documents/receipts/travel_001.pdf",
                "submit_date": "2025-09-16"
            }},
            {"name": "update_expense_reimbursement", "arguments": {
                "reimbursement_id": "reimb_001",
                "amount": 275.00,
                "description": "Updated business travel expenses with parking"
            }},
            {"name": "create_audit_log", "arguments": {
                "user_id": "payroll_admin_001",
                "table_name": "payroll_records",
                "action_type": "create",
                "record_id": "pay_001"
            }}
        ],
    },
    {
        "annotator": 3,
        "user_id": "employee_001", 
        "instruction": (
            "You are Alex Johnson, an Employee with the email 'alex.johnson@company.com'. You need to "
            "manage your HR-related activities. First, enroll in a training program and track your completion. "
            "Then create a performance review, submit a leave request for vacation time, and enroll in "
            "the company benefits plan. Finally, upload a personal document to your employee profile."
        ),
        "actions": [
            {"name": "enroll_employee_training", "arguments": {
                "employee_id": "emp_001",
                "training_program_id": "train_001",
                "enrollment_date": "2025-09-01"
            }},
            {"name": "complete_employee_training", "arguments": {
                "employee_id": "emp_001", 
                "training_program_id": "train_001",
                "completion_date": "2025-09-05",
                "score": 95
            }},
            {"name": "create_performance_review", "arguments": {
                "employee_id": "emp_001",
                "reviewer_id": "mgr_001",
                "review_period_start": "2025-01-01",
                "review_period_end": "2025-06-30",
                "overall_rating": 4,
                "goals": "Improve project management skills",
                "hr_manager_approval": True
            }},
            {"name": "create_leave_request", "arguments": {
                "employee_id": "emp_001",
                "leave_type": "annual",
                "start_date": "2025-10-15",
                "end_date": "2025-10-19",
                "days_requested": 5,
                "reason": "Family vacation"
            }},
            {"name": "enroll_employee_benefits", "arguments": {
                "employee_id": "emp_001",
                "benefits_plan_id": "plan_001",
                "enrollment_date": "2025-09-01",
                "contribution_amount": 150.00,
                "beneficiary": "spouse"
            }},
            {"name": "upload_document", "arguments": {
                "employee_id": "emp_001",
                "document_type": "personal_id",
                "file_path": "/documents/personal/drivers_license.pdf",
                "confidentiality_level": "confidential",
                "retention_years": 7
            }},
            {"name": "create_audit_log", "arguments": {
                "user_id": "employee_001",
                "table_name": "leave_requests", 
                "action_type": "create",
                "record_id": "leave_001"
            }}
        ],
    },
    {
        "annotator": 4,
        "user_id": "finance_officer_001",
        "instruction": (
            "You are Robert Kim, a Finance Officer with the email 'robert.kim@company.com'. You need to "
            "handle financial aspects of HR operations. First, validate and approve a payroll run, "
            "then process an expense reimbursement. After that, create a new benefits plan for dental coverage, "
            "review payroll corrections, and generate financial reports for the HR department."
        ),
        "actions": [
            {"name": "get_payroll_summary", "arguments": {
                "department_id": "dept_eng_01",
                "pay_period": "2025-09-01_to_2025-09-15"
            }},
            {"name": "approve_payroll_run", "arguments": {
                "payroll_run_id": "payrun_001",
                "approver_id": "finance_officer_001",
                "approval_status": "approved",
                "total_amount": 125000.00
            }},
            {"name": "process_expense_reimbursement", "arguments": {
                "reimbursement_id": "reimb_001",
                "approver_id": "finance_officer_001",
                "status": "approved",
                "approval_notes": "Valid business expenses"
            }},
            {"name": "create_benefits_plan", "arguments": {
                "plan_name": "Dental Coverage Plus",
                "plan_type": "dental",
                "premium_amount": 85.00,
                "coverage_details": "Full dental coverage including orthodontics",
                "start_date": "2025-10-01",
                "end_date": "2025-12-31",
                "finance_officer_approval": True
            }},
            {"name": "process_payroll_correction", "arguments": {
                "payroll_id": "pay_001",
                "correction_type": "overtime_adjustment",
                "adjustment_amount": 150.00,
                "reason": "Missing overtime hours",
                "finance_officer_approval": True
            }},
            {"name": "get_department_summary_report", "arguments": {
                "department_id": "dept_hr_01",
                "report_period": "2025-Q3"
            }},
            {"name": "create_audit_log", "arguments": {
                "user_id": "finance_officer_001",
                "table_name": "benefits_plans",
                "action_type": "create", 
                "record_id": "plan_002"
            }}
        ],
    }
]
