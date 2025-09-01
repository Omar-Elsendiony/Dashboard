RULES = [
    # Interface 1: Talent Acquisition & Recruiting Rules
    {
        "rule_id": "TAR_001",
        "interface": "interface_1",
        "category": "Job Position Management",
        "rule": "All job position creation requires validation of department ID and salary range consistency. Invalid details halt the process.",
        "halt_condition": "Halt: Invalid position details: [list]",
        "required_approvals": ["HR Director", "Hiring Manager"],
        "applies_to": ["create_job_position", "update_job_position"]
    },
    {
        "rule_id": "TAR_002", 
        "interface": "interface_1",
        "category": "Job Posting",
        "rule": "Job posting requires position to be in draft status with all required information. Missing requirements halt posting.",
        "halt_condition": "Halt: Missing job posting details: [list]",
        "required_approvals": ["HR Director"],
        "applies_to": ["post_job_opening"]
    },
    {
        "rule_id": "TAR_003",
        "interface": "interface_1", 
        "category": "Candidate Management",
        "rule": "Candidate creation requires valid email and source. Invalid details halt the process.",
        "halt_condition": "Halt: Invalid candidate details: [list]",
        "required_approvals": [],
        "applies_to": ["create_candidate"]
    },
    {
        "rule_id": "TAR_004",
        "interface": "interface_1",
        "category": "Application Management",
        "rule": "Application stage changes require valid transitions and proper approvals. Adverse AI screening actions require Compliance review.",
        "halt_condition": "Halt: Invalid application status change",
        "required_approvals": ["Recruiter", "Hiring Manager", "Compliance Officer (for adverse actions)"],
        "applies_to": ["update_application_stage", "create_job_application"]
    },
    {
        "rule_id": "TAR_005",
        "interface": "interface_1",
        "category": "Interview Management", 
        "rule": "Interview scheduling requires valid application and interviewer. Interview outcome recording requires scheduled/completed state.",
        "halt_condition": "Halt: Invalid interview scheduling details / Interview not found or invalid state",
        "required_approvals": [],
        "applies_to": ["schedule_interview", "record_interview_outcome"]
    },

    # Interface 2: Core HR, On/Off-boarding Rules
    {
        "rule_id": "CHR_001",
        "interface": "interface_2",
        "category": "User Provisioning",
        "rule": "User creation requires valid email, supported role, and no duplicate users. Elevated roles require additional approvals.",
        "halt_condition": "Halt: Invalid user details: [list] / Approval missing: [role]",
        "required_approvals": ["HR Director", "IT Administrator (for elevated roles)"],
        "applies_to": ["create_user"]
    },
    {
        "rule_id": "CHR_002",
        "interface": "interface_2",
        "category": "Department Management",
        "rule": "Department creation/updates require valid manager ID and budget format with HR Director approval.",
        "halt_condition": "Halt: Invalid department details: [list] / Approval missing for department operation",
        "required_approvals": ["HR Director"],
        "applies_to": ["create_department", "update_department"]
    },
    {
        "rule_id": "CHR_003",
        "interface": "interface_2",
        "category": "Employee Onboarding",
        "rule": "Onboarding requires all required fields, HR Manager approval, and Compliance verification for eligibility.",
        "halt_condition": "Halt: Missing onboarding fields: [list] / Approval or compliance verification missing",
        "required_approvals": ["HR Manager", "Compliance Officer"],
        "applies_to": ["create_worker", "employee_onboarding"]
    },
    {
        "rule_id": "CHR_004",
        "interface": "interface_2",
        "category": "Employee Offboarding",
        "rule": "Offboarding requires no pending obligations and proper approvals. Pending items halt the process.",
        "halt_condition": "Halt: Pending items: [list] / Required approvals missing",
        "required_approvals": ["HR Manager", "Compliance Officer"],
        "applies_to": ["employee_offboarding", "terminate_employee"]
    },
    {
        "rule_id": "CHR_005",
        "interface": "interface_2",
        "category": "Document Management",
        "rule": "Document uploads require supported type and complete metadata with proper confidentiality levels.",
        "halt_condition": "Halt: Invalid document metadata: [list]",
        "required_approvals": [],
        "applies_to": ["upload_document"]
    },

    # Interface 3: Time, Attendance, Payroll & Expenses Rules  
    {
        "rule_id": "TAP_001",
        "interface": "interface_3",
        "category": "Timesheet Management",
        "rule": "Timesheet submission requires valid work date with no overlap of existing approved entries.",
        "halt_condition": "Halt: Invalid timesheet entry",
        "required_approvals": ["Payroll Administrator", "Hiring Manager (for approval)"],
        "applies_to": ["submit_timesheet", "approve_timesheet"]
    },
    {
        "rule_id": "TAP_002",
        "interface": "interface_3",
        "category": "Payroll Processing",
        "rule": "Payroll runs require all inputs (hours, deductions) and Finance Officer approval.",
        "halt_condition": "Halt: Invalid payroll input: [list] / Finance Officer approval required",
        "required_approvals": ["Finance Officer"],
        "applies_to": ["process_payroll_run", "approve_payroll_run"]
    },
    {
        "rule_id": "TAP_003",
        "interface": "interface_3",
        "category": "Payroll Corrections",
        "rule": "Payroll corrections require valid payroll record and Finance Officer approval.",
        "halt_condition": "Halt: Payroll record not found / Finance Officer approval required",
        "required_approvals": ["Finance Officer"],
        "applies_to": ["process_payroll_correction"]
    },
    {
        "rule_id": "TAP_004",
        "interface": "interface_3",
        "category": "Expense Reimbursements",
        "rule": "Expense reimbursement updates require existing 'submitted' status. Processing requires valid approver.",
        "halt_condition": "Halt: Invalid reimbursement details: [reimbursement not found] / [cannot update non-submitted reimbursement]",
        "required_approvals": ["Finance Officer"],
        "applies_to": ["update_expense_reimbursement", "process_expense_reimbursement"]
    },

    # Interface 4: Performance, Learning & Development Rules
    {
        "rule_id": "PLD_001",
        "interface": "interface_4", 
        "category": "Performance Reviews",
        "rule": "Performance reviews require valid reviewer/employee and no overlapping approved reviews with HR Manager approval.",
        "halt_condition": "Halt: Invalid performance review details / HR Manager approval required",
        "required_approvals": ["HR Manager"],
        "applies_to": ["create_performance_review", "update_performance_review"]
    },
    {
        "rule_id": "PLD_002",
        "interface": "interface_4",
        "category": "Training Programs",
        "rule": "Training program creation requires all valid program fields and proper status setting.",
        "halt_condition": "Halt: Invalid training program details",
        "required_approvals": [],
        "applies_to": ["create_training_program", "update_training_program"]
    },
    {
        "rule_id": "PLD_003",
        "interface": "interface_4",
        "category": "Training Enrollment",
        "rule": "Training enrollment requires valid employee and program with proper status progression tracking.",
        "halt_condition": "Halt: Invalid training enrollment",
        "required_approvals": [],
        "applies_to": ["enroll_employee_training", "complete_employee_training"]
    },

    # Interface 5: Benefits and Leave Rules
    {
        "rule_id": "BAL_001",
        "interface": "interface_5",
        "category": "Benefits Plans",
        "rule": "Benefits plan creation requires valid plan type and consistent dates with proper approvals.",
        "halt_condition": "Halt: Invalid benefits plan details / HR Director or Finance Officer approval required",
        "required_approvals": ["HR Director", "Finance Officer"],
        "applies_to": ["create_benefits_plan", "update_benefits_plan"]
    },
    {
        "rule_id": "BAL_002",
        "interface": "interface_5",
        "category": "Benefits Enrollment",
        "rule": "Benefits enrollment requires valid plan/employee and contribution within allowed limits.",
        "halt_condition": "Halt: Invalid enrollment details: [list]",
        "required_approvals": [],
        "applies_to": ["enroll_employee_benefits", "update_employee_benefits"]
    },
    {
        "rule_id": "BAL_003",
        "interface": "interface_5",
        "category": "Leave Requests",
        "rule": "Leave requests require valid employee, leave type, logical dates, and sufficient balance. Default allocation is 15 days.",
        "halt_condition": "Halt: Invalid leave request details: [list] / Insufficient leave balance: [X days available]",
        "required_approvals": ["HR Manager (for processing)"],
        "applies_to": ["create_leave_request", "process_leave_request"]
    },

    # Global Rules for All Interfaces
    {
        "rule_id": "GLB_001",
        "interface": "all",
        "category": "Audit Trail",
        "rule": "All actions must generate audit log entries. Failed audit writes halt operations.",
        "halt_condition": "Halt: Audit trail failure",
        "required_approvals": [],
        "applies_to": ["all_operations"]
    },
    {
        "rule_id": "GLB_002",
        "interface": "all",
        "category": "Authorization",
        "rule": "All actions requiring authorization must provide verification codes. Only users with appropriate permissions can grant authorization.",
        "halt_condition": "Halt: Unauthorized access / Invalid authorization",
        "required_approvals": ["Varies by action"],
        "applies_to": ["all_operations_requiring_approval"]
    },
    {
        "rule_id": "GLB_003",
        "interface": "all",
        "category": "Role-Based Access",
        "rule": "Users can only perform actions within their role permissions. Elevated roles have additional privileges.",
        "halt_condition": "Halt: Insufficient permissions",
        "required_approvals": [],
        "applies_to": ["all_operations"]
    },
    {
        "rule_id": "GLB_004",
        "interface": "all",
        "category": "Data Validation",
        "rule": "All inputs must be validated before processing. Invalid or missing required elements halt operations.",
        "halt_condition": "Halt: Invalid input data: [details]",
        "required_approvals": [],
        "applies_to": ["all_operations"]
    },
    {
        "rule_id": "GLB_005",
        "interface": "all",
        "category": "Single-Turn Execution",
        "rule": "Each procedure must be self-contained and completed in one interaction with proper validation and logging.",
        "halt_condition": "Halt: Procedure cannot be completed in single turn",
        "required_approvals": [],
        "applies_to": ["all_operations"]
    }
]
