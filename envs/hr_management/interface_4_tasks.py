from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="user_0004",
        instruction=(
            "Your user ID is user_0004. You’re managing employee experience for your organization. "
            "Please launch a new quarterly engagement survey, assign a laptop to one of your workers, "
            "track its status, and finally record their feedback submission."
        ),
        actions=[
            Action(name="launch_survey", kwargs={
                "organization_id": "org_4001",
                "name": "Quarterly Feedback",
                "launch_date": "2025-07-01",
                "close_date": "2025-07-15"
            }),
            Action(name="assign_device", kwargs={
                "worker_id": "worker_0004",
                "organization_id": "org_4001",
                "type": "laptop",
                "model": "MacBook Pro"
            }),
            Action(name="track_device_status", kwargs={
                "worker_id": "worker_0004"
            }),
            Action(name="submit_engagement_response", kwargs={
                "worker_id": "worker_0004",
                "survey_id": "survey_001",
                "responses": {"q1": "yes", "q2": "no"}
            })
        ],
        outputs=[]
    )
]
