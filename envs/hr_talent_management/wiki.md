# HR Talent Management Domain Database Wiki

## Overview

The HR Talent Management Database supports comprehensive human resources operations across five specialized interfaces, providing end-to-end HR management capabilities from recruitment and hiring through employee lifecycle management, payroll processing, and compliance oversight. This system manages complex HR operations with strict regulatory compliance, comprehensive audit trails, and sophisticated workflow management.

### Regulatory Framework

The system operates under strict compliance with:

- **Labor Laws and Employment Regulations**
- **Equal Employment Opportunity (EEO) Requirements**
- **Data Protection Laws (GDPR, CCPA)**
- **Workplace Safety Standards (OSHA)**
- **Fair Labor Standards Act (FLSA)**
- **Family and Medical Leave Act (FMLA)**
- **Americans with Disabilities Act (ADA)**

### Interface Architecture

The HR Talent Management Domain is organized into five specialized interfaces:

1. **Interface 1: Recruitment & Hiring Operations**

   - Job requisition creation and management
   - Candidate sourcing and application processing
   - Interview scheduling and evaluation
   - Offer creation and management
   - Employee onboarding initiation

2. **Interface 2: Employee Lifecycle Management**

   - Employee record management and updates
   - Application processing and status tracking
   - Onboarding checklist management
   - Employee data change management
   - Performance and development tracking

3. **Interface 3: Recruitment & Candidate Management**

   - Job posting creation and management
   - Candidate profile management
   - Interview operations and panel management
   - Offer processing and acceptance tracking
   - Recruitment analytics and reporting

4. **Interface 4: Payroll & Benefits Operations**

   - Payroll cycle management and processing
   - Payroll input validation and approval
   - Benefit plan creation and management
   - Benefit enrollment processing
   - Payment processing and tracking

5. **Interface 5: Compliance & Analytics Operations**
   - Employee exit processing and clearance
   - Document management and verification
   - Notification and communication management
   - Compliance monitoring and reporting
   - Audit trail management and analytics

## Database Schema

### Users

Maintains user profiles for HR system access.

- **Fields:** user_id, first_name, last_name, email, phone_number, role, employment_status, timezone, created_at, updated_at
- **Roles:** hr_manager, hr_admin, hr_recruiter, hr_director, department_manager, compliance_officer, finance_manager, employee
- **Status:** active, inactive, suspended

### Job Requisitions

Stores information about job openings and requirements.

- **Fields:** requisition_id, job_title, department_id, location_id, employment_type, hiring_manager_id, budgeted_salary_min, budgeted_salary_max, job_description, grade, shift_type, remote_indicator, status, hr_manager_approver, dept_head_approver, hr_manager_approval_date, dept_head_approval_date, posted_date, created_by, created_at, updated_at
- **Employment Types:** full_time, part_time, contractor, intern
- **Status:** draft, pending_approval, approved, closed

### Job Postings

Tracks published job openings.

- **Fields:** posting_id, requisition_id, posted_date, portal_type, status, closed_date, created_at, updated_at
- **Portal Types:** internal, external, both
- **Status:** active, closed, cancelled

### Candidates

Details individual job applicants.

- **Fields:** candidate_id, first_name, last_name, email_address, contact_number, source_of_application, country_of_residence, linkedin_profile, current_ctc, status, created_at, updated_at
- **Status:** active, inactive, hired, rejected

### Applications

Records candidate applications to job postings.

- **Fields:** application_id, candidate_id, posting_id, resume_file_id, cover_letter_file_id, application_date, status, screened_by, screened_date, shortlist_approved_by, shortlist_approval_date, created_at, updated_at
- **Status:** applied, screened, shortlisted, rejected, hired

### Interviews

Tracks interview scheduling and evaluation.

- **Fields:** interview_id, application_id, interview_type, scheduled_date, interview_status, rating, recommendation, completed_by, completed_date, created_at, updated_at
- **Interview Types:** phone, video, in_person, technical, behavioral, panel
- **Status:** scheduled, completed, cancelled, rescheduled

### Interview Panel Members

Records interview panel assignments.

- **Fields:** interview_id, user_id, created_at

### Offers

Manages job offers and acceptance tracking.

- **Fields:** offer_id, candidate_id, requisition_id, position, start_date, base_salary, stock_options_amount, signing_bonus_amount, relocation_allowance_amount, reporting_manager_id, offer_status, compliance_approved_by, compliance_approval_date, hr_manager_approved_by, hr_manager_approval_date, issue_date, acceptance_date, offer_accepted_date, created_at, updated_at
- **Status:** draft, pending_compliance, pending_approval, approved_for_issue, issued, accepted, rejected, withdrawn

### Offer Benefits

Tracks benefits associated with offers.

- **Fields:** offer_id, benefit_type, benefit_description, created_at

### Employees

Stores comprehensive employee information.

- **Fields:** employee_id, candidate_id, first_name, last_name, employee_type, department_id, location_id, job_title, start_date, tax_id, bank_account_number, routing_number, work_email, phone_number, manager_id, tax_filing_status, employment_status, created_at, updated_at
- **Employee Types:** full_time, part_time, contractor, intern
- **Employment Status:** active, inactive, terminated, on_leave

### Onboarding Checklists

Tracks employee onboarding progress.

- **Fields:** checklist_id, employee_id, candidate_name, start_date, position, hiring_manager_id, pre_onboarding_status, background_check_status, background_check_cleared_date, document_verification_status, it_provisioning_status, orientation_completed, orientation_date, benefits_enrollment_status, overall_status, created_at, updated_at
- **Status:** pending, in_progress, completed, delayed

### Documents

Manages document storage and verification.

- **Fields:** document_id, document_category, related_entity_type, related_entity_id, file_name, upload_date, uploaded_by, document_status, expiry_date, verification_status, verified_by, verified_date, created_at, updated_at
- **Document Categories:** resume, cover_letter, offer_letter, contract, verification_id_proof, verification_address_proof, verification_educational_certificate, verification_experience_letter, verification_work_visa, verification_pr_card, verification_bank_proof, budget_approval, headcount_justification, policy_acknowledgment, promotion_letter, transfer_memo, insurance_form, tax_form, other
- **Status:** active, archived, expired, deleted

### IT Provisioning Tasks

Tracks IT setup and equipment provisioning.

- **Fields:** task_id, employee_id, task_type, assigned_to, task_status, completion_date, created_at, updated_at
- **Task Types:** account_creation, equipment_setup, software_installation, access_provisioning, email_setup
- **Status:** pending, in_progress, completed, failed

### Payroll Cycles

Manages payroll processing periods.

- **Fields:** cycle_id, cycle_start_date, cycle_end_date, frequency, cutoff_date, status, created_at, updated_at
- **Frequency:** weekly, bi_weekly, semi_monthly, monthly
- **Status:** draft, open, processing, completed, closed

### Payroll Inputs

Records employee time and attendance data.

- **Fields:** input_id, employee_id, cycle_id, hours_worked, overtime_hours, manager_approval_status, manager_approved_by, manager_approval_date, input_status, created_at, updated_at
- **Status:** draft, pending_approval, approved, processed

### Payroll Earnings

Tracks additional earnings and bonuses.

- **Fields:** earning_id, payroll_input_id, employee_id, earning_type, amount, approval_status, approved_by, approval_date, created_at, updated_at
- **Earning Types:** bonus, incentive, reimbursement, overtime, commission
- **Status:** pending, approved, processed

### Payslips

Manages employee pay statements.

- **Fields:** payslip_id, employee_id, cycle_id, gross_pay, base_salary, bonus_earned, incentives_earned, reimbursements, total_deductions, net_pay, proration_status, payslip_status, released_date, created_at, updated_at
- **Status:** generated, verified, released, archived

### Payments

Tracks actual payment processing.

- **Fields:** payment_id, employee_id, cycle_id, payslip_id, amount, payment_date, payment_method, payment_status, transaction_id, bank_confirmation_date, created_at, updated_at
- **Payment Methods:** direct_deposit, check, wire_transfer
- **Status:** pending, completed, failed, refunded

### Benefit Plans

Defines available benefit options.

- **Fields:** plan_id, benefit_type, plan_name, provider_name, description, effective_from, effective_until, default_employee_contribution, default_employer_contribution, plan_status, created_at, updated_at
- **Benefit Types:** health_insurance, dental_insurance, vision_insurance, life_insurance, disability_insurance, retirement_401k, flexible_spending_account, health_savings_account
- **Status:** active, inactive, expired

### Benefit Enrollments

Tracks employee benefit selections.

- **Fields:** enrollment_id, employee_id, plan_id, effective_date, employee_contribution, employer_contribution, enrollment_window_start, enrollment_window_end, selection_date, enrollment_status, hr_manager_approval_status, approved_by, approval_date, created_at, updated_at
- **Status:** pending, active, cancelled, expired

### Employee Exits

Manages employee separation processes.

- **Fields:** exit_id, employee_id, exit_date, exit_reason, manager_clearance, it_equipment_return, finance_settlement_status, clearance_status, approved_by, approval_date, final_pay_amount, leave_encashment_amount, paid_date, created_at, updated_at
- **Exit Reasons:** resignation, termination, retirement, layoff, contract_end
- **Status:** initiated, in_progress, completed

### Notifications

System notifications and alerts.

- **Fields:** notification_id, recipient_user_id, recipient_email, notification_type, reference_type, reference_id, message, notification_status, sent_at, created_at
- **Notification Types:** alert, reminder, report, policy_update, benefit_enrollment, payroll_notification, onboarding_reminder
- **Status:** pending, sent, failed, read

### Audit Trails

Comprehensive activity logging.

- **Fields:** audit_id, reference_id, reference_type, action, user_id, field_name, old_value, new_value, timestamp, ip_address, user_agent
- **Reference Types:** employee, candidate, job_requisition, job_posting, application, interview, offer, document, payroll_cycle, payroll_input, payroll_earning, payslip, payment, benefit_plan, benefit_enrollment, employee_exit, notification, user, department, location
- **Actions:** create, update, delete, approve, reject, verify, process, send, upload, download

### Departments

Organizational structure management.

- **Fields:** department_id, department_name, department_code, manager_id, budget, status, created_at, updated_at
- **Status:** active, inactive, merged, dissolved

### Locations

Office and facility management.

- **Fields:** location_id, location_name, address, city_name, country, status, created_at, updated_at
- **Status:** active, inactive, closed

## API Interactions

The HR Talent Management Domain provides 160+ specialized tools across five interfaces, representing the exclusive means for agents to interact with the database. All operations maintain strict audit trails, role-based access controls, and regulatory compliance.

### Interface 1: Recruitment & Hiring Operations (~32 Tools)

**Core Functions:**

- **Entity Discovery:** discover_reference_entities, discover_job_entities, discover_candidate_entities, discover_interview_offer_entities, discover_employee_entities, discover_document_task_entities, discover_payroll_entities, discover_benefit_entities, discover_payment_entities, discover_system_entities
- **Job Operations:** manage_job_operations (create_requisition, update_requisition, approve_requisition, create_posting, update_posting)
- **Candidate Operations:** manage_candidate_operations (create_candidate, update_candidate)
- **Application Operations:** manage_application_operations (create_application, update_application_status)
- **Interview Operations:** manage_interview_operations (schedule_interview, add_panel_member, conduct_evaluation)
- **Offer Operations:** manage_offer_operations (create_offer, add_benefit, verify_compliance, approve_offer, issue_offer, record_acceptance)
- **Employee Operations:** manage_employee_operations (create_employee, update_employee_data)
- **Onboarding Operations:** manage_onboarding_operations (create_checklist, update_checklist)
- **Document Operations:** manage_document_operations (upload_document, verify_document, update_document_status)
- **IT Operations:** manage_it_provisioning_operations (create_task, update_task)
- **Notification Operations:** manage_notification_operations (create_notification)
- **Audit Operations:** create_audit_entry
- **Human Transfer:** transfer_to_human

### Interface 2: Employee Lifecycle Management (~32 Tools)

**Core Functions:**

- **Entity Discovery:** discover_reference_entities, discover_job_entities, discover_candidate_entities, discover_interview_offer_entities, discover_employee_entities, discover_document_task_entities, discover_payroll_entities, discover_benefit_entities, discover_payment_entities, discover_system_entities
- **Job Operations:** administer_job_operations (create_requisition, update_requisition, approve_requisition, create_posting, update_posting)
- **Candidate Operations:** administer_candidate_operations (create_candidate, update_candidate)
- **Application Operations:** administer_application_operations (create_application, update_application_status)
- **Interview Operations:** administer_interview_operations (schedule_interview, add_panel_member, conduct_evaluation)
- **Offer Operations:** administer_offer_operations (create_offer, add_benefit, verify_compliance, approve_offer, issue_offer, record_acceptance)
- **Employee Operations:** administer_employee_operations (create_employee, update_employee_data)
- **Onboarding Operations:** administer_onboarding_operations (create_checklist, update_checklist)
- **Document Operations:** administer_document_operations (upload_document, verify_document, update_document_status)
- **IT Operations:** administer_it_provisioning_operations (create_task, update_task)
- **Notification Operations:** administer_notification_operations (create_notification)
- **Audit Operations:** add_audit_entry
- **Human Transfer:** transfer_to_human

### Interface 3: Recruitment & Candidate Management (~32 Tools)

**Core Functions:**

- **Entity Discovery:** discover_reference_entities, discover_job_entities, discover_candidate_entities, discover_interview_offer_entities, discover_employee_entities, discover_document_task_entities, discover_payroll_entities, discover_benefit_entities, discover_payment_entities, discover_system_entities
- **Job Operations:** administer_job_operations (create_requisition, update_requisition, approve_requisition, create_posting, update_posting)
- **Candidate Operations:** administer_candidate_operations (create_candidate, update_candidate)
- **Application Operations:** administer_application_operations (create_application, update_application_status)
- **Interview Operations:** administer_interview_operations (schedule_interview, add_panel_member, conduct_evaluation)
- **Offer Operations:** administer_offer_operations (create_offer, add_benefit, verify_compliance, approve_offer, issue_offer, record_acceptance)
- **Employee Operations:** administer_employee_operations (create_employee, update_employee_data)
- **Onboarding Operations:** administer_onboarding_operations (create_checklist, update_checklist)
- **Document Operations:** administer_document_operations (upload_document, verify_document, update_document_status)
- **IT Operations:** administer_it_provisioning_operations (create_task, update_task)
- **Notification Operations:** administer_notification_operations (create_notification)
- **Audit Operations:** add_audit_entry
- **Human Transfer:** transfer_to_human

### Interface 4: Payroll & Benefits Operations (~32 Tools)

**Core Functions:**

- **Entity Discovery:** get_reference_entities, get_job_entities, get_candidate_entities, get_interview_offer_entities, get_employee_entities, get_document_task_entities, get_payroll_entities, get_benefit_entities, get_payment_entities, get_system_entities
- **Job Operations:** process_job_operations (create_requisition, update_requisition, approve_requisition, create_posting, update_posting)
- **Candidate Operations:** process_candidate_operations (create_candidate, update_candidate)
- **Application Operations:** process_application_operations (create_application, update_application_status)
- **Interview Operations:** process_interview_operations (schedule_interview, add_panel_member, conduct_evaluation)
- **Offer Operations:** process_offer_operations (create_offer, add_benefit, verify_compliance, approve_offer, issue_offer, record_acceptance)
- **Employee Operations:** process_employee_operations (create_employee, update_employee_data)
- **Onboarding Operations:** process_onboarding_operations (create_checklist, update_checklist)
- **Document Operations:** process_document_operations (upload_document, verify_document, update_document_status)
- **IT Operations:** process_it_provisioning_operations (create_task, update_task)
- **Payroll Operations:** process_payroll_cycle_operations, process_payroll_input_operations, process_payroll_earning_operations, process_payslip_operations, process_payment_operations
- **Benefit Operations:** process_benefit_plan_operations, process_benefit_enrollment_operations
- **Notification Operations:** process_notification_operations (create_notification)
- **Audit Operations:** build_audit_entry
- **Human Transfer:** transfer_to_human

### Interface 5: Compliance & Analytics Operations (~32 Tools)

**Core Functions:**

- **Entity Discovery:** get_reference_entities, get_job_entities, get_candidate_entities, get_interview_offer_entities, get_employee_entities, get_document_task_entities, get_payroll_entities, get_benefit_entities, get_payment_entities, get_system_entities
- **Job Operations:** process_job_operations (create_requisition, update_requisition, approve_requisition, create_posting, update_posting)
- **Candidate Operations:** process_candidate_operations (create_candidate, update_candidate)
- **Application Operations:** process_application_operations (create_application, update_application_status)
- **Interview Operations:** process_interview_operations (schedule_interview, add_panel_member, conduct_evaluation)
- **Offer Operations:** process_offer_operations (create_offer, add_benefit, verify_compliance, approve_offer, issue_offer, record_acceptance)
- **Employee Operations:** process_employee_operations (create_employee, update_employee_data)
- **Onboarding Operations:** process_onboarding_operations (create_checklist, update_checklist)
- **Document Operations:** process_document_operations (upload_document, verify_document, update_document_status)
- **IT Operations:** process_it_provisioning_operations (create_task, update_task)
- **Payroll Operations:** process_payroll_cycle_operations, process_payroll_input_operations, process_payroll_earning_operations, process_payslip_operations, process_payment_operations
- **Benefit Operations:** process_benefit_plan_operations, process_benefit_enrollment_operations
- **Exit Operations:** process_employee_exit_operations (create_exit, update_clearance, process_settlement)
- **Location Operations:** process_location_operations (create_location, update_location)
- **Department Operations:** process_department_operations (create_department, update_department)
- **Notification Operations:** process_notification_operations (create_notification)
- **Audit Operations:** build_audit_entry
- **Human Transfer:** transfer_to_human

### Key Requirements

- All HR operations require appropriate role-based authorization
- Employee data changes must maintain proper audit trails
- Payroll processing requires manager approval workflows
- Benefit enrollments must validate eligibility periods
- All document operations require proper categorization
- Compliance operations must follow regulatory requirements
- All communications require appropriate authorization
- Exit processes must complete clearance requirements

## Core Business Rules

### Authorization Matrix

- **HR Manager:** Full access to HR operations, policy enforcement, and employee management
- **HR Admin:** Administrative functions, data management, and routine processing
- **HR Recruiter:** Recruitment operations, candidate management, and hiring processes
- **HR Director:** Strategic oversight, policy decisions, and high-level reporting
- **Department Manager:** Team management, approval workflows, and department operations
- **Compliance Officer:** Regulatory oversight, policy compliance, and audit management
- **Finance Manager:** Payroll operations, financial approvals, and budget management

### HR Controls

- **Dual Authorization:** Sensitive operations require dual approval
- **Reconciliation:** Regular reconciliation of payroll and benefit data
- **Audit Trails:** Comprehensive logging of all HR activities
- **Policy Enforcement:** Automated enforcement of HR policies and procedures

### Regulatory Compliance

- **Data Privacy:** Strict protection of employee personal information
- **Equal Opportunity:** Compliance with EEO and anti-discrimination laws
- **Labor Standards:** Adherence to wage and hour regulations
- **Benefits Compliance:** Proper administration of benefit programs

## HR Talent Management Agent Policy Framework

The HR Talent Management Domain operates under a comprehensive policy framework ensuring regulatory compliance, operational excellence, and employee privacy protection across all human resources activities.

### General Principles

1. **Employee Privacy and Data Protection**
   - Protect employee personal information and maintain confidentiality
   - Ensure compliance with data protection regulations (GDPR, CCPA)
   - Implement appropriate access controls and security measures

2. **Regulatory Compliance**
   - Strict adherence to labor laws and employment regulations
   - Compliance with Equal Employment Opportunity requirements
   - Maintenance of comprehensive audit trails for all HR activities

3. **Operational Excellence**
   - Accurate and timely processing of all HR operations
   - Comprehensive documentation and record-keeping
   - Continuous improvement of HR processes and controls

4. **Fair Employment Practices**
   - Ensure equal opportunity in all hiring and employment decisions
   - Maintain diversity and inclusion in recruitment processes
   - Provide fair and consistent treatment of all employees

### Role-Based Authorization

**HR Manager Responsibilities:**
- Employee lifecycle management and policy enforcement
- Recruitment oversight and hiring decisions
- Performance management and development programs
- Compliance monitoring and policy implementation

**HR Admin Functions:**
- Administrative data management and system maintenance
- Routine HR processing and documentation
- Employee record management and updates
- Support for HR operations and reporting

**HR Recruiter Duties:**
- Candidate sourcing and recruitment activities
- Interview coordination and evaluation
- Offer management and hiring processes
- Recruitment analytics and reporting

**HR Director Authority:**
- Strategic HR planning and policy development
- High-level oversight and decision making
- Compliance and regulatory management
- Organizational development and change management

**Department Manager Functions:**
- Team management and performance oversight
- Approval workflows for team-related operations
- Budget management and resource allocation
- Employee development and career guidance

**Compliance Officer Authority:**
- Regulatory compliance monitoring and reporting
- Policy enforcement and audit management
- Risk assessment and mitigation
- Legal and regulatory guidance

**Finance Manager Duties:**
- Payroll operations and financial processing
- Budget management and cost control
- Financial approvals and expense management
- Compensation and benefits administration

### Security and Compliance Framework

#### Data Protection and Security
- **Encryption:** All sensitive employee data encrypted at rest and in transit
- **Access Controls:** Role-based access with multi-factor authentication
- **Audit Logging:** Comprehensive logging of all system activities and user actions
- **Data Backup:** Regular automated backups with disaster recovery procedures

#### Regulatory Compliance Controls
- **Labor Law Compliance:** Automated compliance monitoring and reporting
- **EEO Compliance:** Adherence to equal employment opportunity requirements
- **Data Privacy:** Protection of employee personal information
- **Benefits Administration:** Proper administration of benefit programs

#### Risk Management Framework
- **Operational Risk:** Process controls and exception monitoring
- **Compliance Risk:** Regulatory compliance monitoring and reporting
- **Data Security Risk:** Protection of sensitive employee information
- **Legal Risk:** Adherence to employment laws and regulations
