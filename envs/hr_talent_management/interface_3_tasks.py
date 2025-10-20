from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="3",
        user_id="2",
        instruction=(
            "You are Maria Garcia, an HR Recruiter. You need to manage recruitment processes and candidate lifecycle. "
            "Discover candidate entities, create job postings, manage interview operations, and process offers."
        ),
        actions=[
            Action(name="lookup_candidate_entities", kwargs={
                "entity_type": "candidates",
                "filters": {"status": "active"}
            }),
            Action(name="execute_job_operations", kwargs={
                "operation_type": "create_posting",
                "requisition_id": "3",
                "posted_date": "01-12-2025",
                "portal_type": "external",
                "user_id": "2"
            }),
            Action(name="execute_interview_operations", kwargs={
                "operation_type": "schedule_interview",
                "application_id": "4",
                "interview_type": "technical",
                "scheduled_date": "01-20-2025",
                "panel_member_ids": ["5", "6"],
                "user_id": "2"
            }),
            Action(name="execute_offer_operations", kwargs={
                "operation_type": "create_offer",
                "candidate_id": "7",
                "requisition_id": "3",
                "position": "Product Manager",
                "start_date": "02-15-2025",
                "base_salary": 95000.0,
                "reporting_manager_id": "12",
                "user_id": "2",
                "offer_letter_file_name": "offer_letter_pm.pdf",
                "status": "draft"
            }),
            Action(name="make_audit_entry", kwargs={
                "reference_id": "7",
                "reference_type": "offer",
                "action": "create",
                "user_id": "2",
                "field_name": "offer_creation"
            })
        ],
        outputs=[]
    )
]
