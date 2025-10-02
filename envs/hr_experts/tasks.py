tasks = [
    {
        "annotator": 0,
        "user_id": "hr_director_001",
        "instruction": (
            "You are Sarah Thompson, an HR Director with the email 'sarah.thompson@company.com'. You need to "
            "manage a comprehensive employee lifecycle process. First, create a new user account for a new employee "
            "Jennifer Martinez as a Marketing Coordinator, then create a department for Digital Marketing. "
            "After that, create an employee record with full onboarding, enroll her in benefits, assign training, "
            "and add an audit trail for all operations."
        ),
        "actions": [
            {"name": "manage_user", "arguments": {
                "action": "create",
                "first_name": "Jennifer",
                "last_name": "Martinez",
                "email": "jennifer.martinez@company.com",
                "role": "employee",
                "department": "Digital Marketing",
                "hr_director_approval": True
            }},
            {"name": "manage_department", "arguments": {
                "action": "create",
                "name": "Digital Marketing",
                "manager_id": "mgr_003",
                "budget": 750000,
                "location": "Main Office",
                "hr_director_approval": True
            }},
            {"name": "manage_employee", "arguments": {
                "action": "create",
                "user_id": "usr_004",
                "position": "Marketing Coordinator",
                "salary": 55000,
                "start_date": "2025-10-01",
                "hr_manager_approval": True,
                "compliance_verification": True
            }},
            {"name": "manage_employee_benefits", "arguments": {
                "action": "enroll",
                "employee_id": "emp_004",
                "benefits_plan_id": "plan_health_001",
                "enrollment_date": "2025-10-01",
                "contribution_amount": 125.00
            }},
            {"name": "manage_employee_training", "arguments": {
                "action": "assign",
                "employee_id": "emp_004",
                "training_program_id": "train_orientation_001",
                "enrollment_date": "2025-10-01",
                "deadline": "2025-10-15"
            }},
            {"name": "check_approval", "arguments": {
                "action": "audit_trail",
                "reference_id": "emp_004",
                "reference_type": "employee",
                "operation": "onboarding_complete"
            }}
        ],
    },
    {
        "annotator": 1,
        "user_id": "payroll_admin_001",
        "instruction": (
            "You are Michael Chen, a Payroll Administrator with the email 'michael.chen@company.com'. You need to "
            "process payroll operations for multiple employees. First, retrieve employee payroll information, "
            "process regular payroll with overtime calculations, handle payroll deductions for taxes and benefits, "
            "then calculate final net pay and generate payroll reports."
        ),
        "actions": [
            {"name": "discover_employee", "arguments": {
                "search_criteria": "active_employees",
                "department": "Engineering"
            }},
            {"name": "manage_payroll_record", "arguments": {
                "action": "create",
                "employee_id": "emp_001",
                "pay_period": "2025-09-16_to_2025-09-30",
                "regular_hours": 80,
                "overtime_hours": 5,
                "hourly_rate": 45.00,
                "finance_officer_approval": True
            }},
            {"name": "manage_payroll_deduction", "arguments": {
                "action": "apply",
                "payroll_id": "pay_001",
                "deduction_type": "federal_tax",
                "amount": 650.00,
                "deduction_type_2": "health_insurance",
                "amount_2": 125.00
            }},
            {"name": "discover_payroll_record", "arguments": {
                "employee_id": "emp_001",
                "pay_period": "2025-09-16_to_2025-09-30"
            }},
            {"name": "check_approval", "arguments": {
                "action": "payroll_validation",
                "payroll_id": "pay_001",
                "finance_officer_approval": True
            }}
        ],
    },
    {
        "annotator": 2,
        "user_id": "benefits_admin_001", 
        "instruction": (
            "You are Lisa Rodriguez, a Benefits Administrator with the email 'lisa.rodriguez@company.com'. "
            "You need to manage comprehensive benefits administration. First, create a new benefits plan for "
            "dental coverage, then enroll multiple employees in various benefit programs, handle a life event "
            "change for an employee, and process benefits premium calculations."
        ),
        "actions": [
            {"name": "manage_benefits_plan", "arguments": {
                "action": "create",
                "plan_name": "Premium Dental Coverage",
                "plan_type": "dental",
                "premium_amount": 75.00,
                "coverage_details": "Comprehensive dental with orthodontics",
                "start_date": "2025-10-01",
                "hr_director_approval": True
            }},
            {"name": "discover_benefits_plan", "arguments": {
                "plan_type": "all_active"
            }},
            {"name": "manage_employee_benefits", "arguments": {
                "action": "enroll",
                "employee_id": "emp_002",
                "benefits_plan_id": "plan_dental_001",
                "enrollment_date": "2025-10-01",
                "coverage_level": "family"
            }},
            {"name": "manage_employee_benefits", "arguments": {
                "action": "life_event_change",
                "employee_id": "emp_003",
                "event_type": "marriage",
                "effective_date": "2025-09-15",
                "coverage_change": "add_spouse"
            }},
            {"name": "check_approval", "arguments": {
                "action": "benefits_audit",
                "employee_id": "emp_002",
                "audit_type": "enrollment_verification"
            }}
        ],
    },
    {
        "annotator": 3,
        "user_id": "hr_manager_001",
        "instruction": (
            "You are David Park, an HR Manager with the email 'david.park@company.com'. You need to "
            "handle performance management and employee development activities. First, conduct performance "
            "reviews for team members, create training programs, manage leave requests, and handle "
            "employee relations issues with proper documentation and approvals."
        ),
        "actions": [
            {"name": "manage_performance_review", "arguments": {
                "action": "create",
                "employee_id": "emp_001",
                "reviewer_id": "hr_manager_001",
                "review_period": "2025-H1",
                "overall_rating": 4,
                "goals_achievement": 85,
                "development_areas": "Leadership skills, Project management",
                "hr_manager_approval": True
            }},
            {"name": "manage_training_programs", "arguments": {
                "action": "create",
                "program_name": "Leadership Development Workshop",
                "duration_hours": 16,
                "description": "Advanced leadership skills for senior staff",
                "mandatory": False,
                "max_participants": 20
            }},
            {"name": "manage_leave_requests", "arguments": {
                "action": "process",
                "employee_id": "emp_002",
                "leave_type": "FMLA",
                "start_date": "2025-10-15",
                "duration_weeks": 12,
                "medical_certification": True,
                "hr_manager_approval": True
            }},
            {"name": "discover_employee", "arguments": {
                "search_criteria": "pending_reviews",
                "department": "all"
            }},
            {"name": "check_approval", "arguments": {
                "action": "compliance_check",
                "operation_type": "performance_management",
                "compliance_officer_review": True
            }}
        ],
    },
    {
        "annotator": 4,
        "user_id": "compliance_officer_001",
        "instruction": (
            "You are Rachel Kim, a Compliance Officer with the email 'rachel.kim@company.com'. You need to "
            "ensure regulatory compliance across all HR operations. First, conduct compliance audits for "
            "employee records, validate FMLA eligibility, review payroll compliance, handle document "
            "management for sensitive records, and generate compliance reports."
        ),
        "actions": [
            {"name": "discover_employee", "arguments": {
                "search_criteria": "compliance_audit",
                "audit_type": "annual_review"
            }},
            {"name": "manage_document_storage", "arguments": {
                "action": "upload",
                "employee_id": "emp_001",
                "document_type": "I9_form",
                "confidentiality_level": "highly_confidential",
                "retention_years": 3,
                "compliance_officer_approval": True
            }},
            {"name": "discover_leave_balance", "arguments": {
                "employee_id": "emp_002",
                "leave_type": "FMLA",
                "eligibility_check": True
            }},
            {"name": "manage_expense_reimbursements", "arguments": {
                "action": "audit",
                "employee_id": "emp_003",
                "expense_period": "2025-Q3",
                "audit_type": "policy_compliance"
            }},
            {"name": "check_approval", "arguments": {
                "action": "regulatory_compliance",
                "audit_scope": "department_wide",
                "compliance_status": "verified"
            }}
        ],
    }
]