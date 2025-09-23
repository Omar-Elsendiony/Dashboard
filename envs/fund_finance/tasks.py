from tau_bench.types import Action, Task

tasks = [
    Task(
        annotator="general",
        user_id="0",
        instruction=(
            "You are a Finance Expert System Administrator. You have access to all five interfaces "
            "and need to perform comprehensive fund management operations across the system."
        ),
        actions=[
            Action(name="approval_lookup", kwargs={
                "action": "system_monitoring",
                "requester_email": "admin@company.com"
            }),
            Action(name="generate_report", kwargs={
                "report_type": "system_overview"
            })
        ],
        outputs=[]
    )
]