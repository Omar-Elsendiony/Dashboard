from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="5",
        user_id="5",
        instruction=(
            "You are Lisa Thompson, an HR Director. You need to manage strategic HR operations and compliance. "
            "Get system entities, process employee exits, manage notifications, and handle compliance operations."
        ),
        actions=[
            Action(name="retrieve_system_entities", kwargs={
                "entity_type": "audit_trails",
                "filters": {"reference_type": "employee"}
            }),
            Action(name="handle_employee_exit_operations", kwargs={
                "operation_type": "create_exit",
                "employee_id": "6",
                "exit_date": "02-28-2025",
                "exit_reason": "resignation",
                "user_id": "5"
            }),
            Action(name="handle_notification_operations", kwargs={
                "operation_type": "create_notification",
                "recipient_user_id": "7",
                "recipient_email": "employee@company.com",
                "notification_type": "policy_update",
                "reference_type": "employee",
                "reference_id": "7",
                "message": "Your benefits enrollment period is now open"
            }),
            Action(name="handle_document_operations", kwargs={
                "operation_type": "upload_document",
                "document_category": "policy_acknowledgment",
                "related_entity_type": "employee",
                "related_entity_id": "8",
                "file_name": "employee_handbook_acknowledgment.pdf",
                "upload_date": "01-15-2025",
                "uploaded_by": "5"
            }),
            Action(name="open_audit_entry", kwargs={
                "reference_id": "6",
                "reference_type": "employee_exit",
                "action": "create",
                "user_id": "5",
                "field_name": "exit_process"
            })
        ],
        outputs=[]
    )
]
