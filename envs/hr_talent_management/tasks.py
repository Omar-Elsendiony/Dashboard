from tau_bench.types import Action, Task

tasks = [
    Task(
        annotator="general",
        user_id="0",
        instruction=(
            "You are an HR Management System Administrator. You have access to all five interfaces "
            "and need to perform comprehensive HR operations across the system."
        ),
        actions=[
            Action(name="discover_reference_entities", kwargs={
                "entity_type": "users",
                "filters": {"email": "admin@company.com"}
            }),
            Action(name="discover_employee_entities", kwargs={
                "entity_type": "employees",
                "filters": {"employment_status": "active"}
            })
        ],
        outputs=[]
    )
]
