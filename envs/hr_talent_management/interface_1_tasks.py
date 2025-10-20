from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="1",
        user_id="1",
        instruction=(
            "You are Sarah Johnson, an HR Manager. You need to manage recruitment and employee operations. "
            "First, discover system entities, then create a new job requisition, manage candidate operations, "
            "and create an employee record."
        ),
        actions=[
            Action(name="discover_reference_entities", kwargs={
                "entity_type": "users",
                "filters": {"email": "sarah.johnson@company.com"}
            }),
            Action(name="manage_job_operations", kwargs={
                "operation_type": "create_requisition",
                "job_title": "Senior Software Engineer",
                "department_id": "2",
                "location_id": "1",
                "employment_type": "full_time",
                "hiring_manager_id": "15",
                "budgeted_salary_min": 80000.0,
                "budgeted_salary_max": 120000.0,
                "created_by": "1"
            }),
            Action(name="manage_candidate_operations", kwargs={
                "operation_type": "create_candidate",
                "first_name": "Michael",
                "last_name": "Chen",
                "email_address": "michael.chen@email.com",
                "contact_number": "+1-555-0123",
                "country_of_residence": "USA",
                "created_by": "1",
                "resume_file_name": "michael_chen_resume.pdf"
            }),
            Action(name="manage_employee_operations", kwargs={
                "operation_type": "create_employee",
                "first_name": "Jennifer",
                "last_name": "Williams",
                "employee_type": "full_time",
                "department_id": "3",
                "location_id": "2",
                "job_title": "Marketing Specialist",
                "start_date": "01-15-2025",
                "tax_id": "123-45-6789",
                "bank_account_number": "1234567890",
                "routing_number": "021000021",
                "work_email": "jennifer.williams@company.com",
                "role": "employee",
                "user_id": "1"
            }),
            Action(name="create_audit_entry", kwargs={
                "reference_id": "1",
                "reference_type": "employee",
                "action": "create",
                "user_id": "1",
                "field_name": "employee_record"
            })
        ],
        outputs=[]
    )
]
