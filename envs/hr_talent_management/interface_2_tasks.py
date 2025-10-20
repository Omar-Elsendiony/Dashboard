from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="2",
        user_id="3",
        instruction=(
            "You are David Rodriguez, an HR Admin. You need to manage employee lifecycle and administrative functions. "
            "Check system entities, handle employee operations, process applications, and manage onboarding."
        ),
        actions=[
            Action(name="fetch_reference_entities", kwargs={
                "entity_type": "users",
                "filters": {"email": "david.rodriguez@company.com"}
            }),
            Action(name="administer_application_operations", kwargs={
                "operation_type": "create_application",
                "created_by": "3",
                "candidate_id": "5",
                "posting_id": "2",
                "resume_file_id": "10",
                "application_date": "01-10-2025"
            }),
            Action(name="administer_employee_operations", kwargs={
                "operation_type": "update_employee_data",
                "employee_id": "2",
                "user_id": "3",
                "job_title": "Senior Marketing Manager",
                "employment_status": "active"
            }),
            Action(name="administer_onboarding_operations", kwargs={
                "operation_type": "create_checklist",
                "employee_id": "3",
                "start_date": "02-01-2025",
                "position": "Data Analyst",
                "hiring_manager_id": "8",
                "user_id": "3"
            }),
            Action(name="add_audit_entry", kwargs={
                "reference_id": "3",
                "reference_type": "onboarding",
                "action": "create",
                "user_id": "3",
                "field_name": "onboarding_checklist"
            })
        ],
        outputs=[]
    )
]
