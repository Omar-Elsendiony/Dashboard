from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="user_0001",
        instruction=(
            "Your user ID is user_0001. You are an HR administrator onboarding a new employee. "
            "Please create the user's profile, then register them as a worker, assign them to an organization, "
            "and designate them as the manager for the HR department."
        ),
        actions=[
            Action(name="create_user", kwargs={
                "first_name": "Diana",
                "last_name": "Stone",
                "email": "diana.stone@example.com",
                "role": "employee",
                "timezone": "UTC",
                "locale": "en-US"
            }),
            Action(name="create_worker", kwargs={
                "user_id": "user_0001",
                "organization_id": "org_1001",
                "type": "employee",
                "start_date": "2025-07-01"
            }),
            Action(name="assign_worker_to_org", kwargs={
                "worker_id": "worker_0001",
                "organization_id": "org_1001"
            }),
            Action(name="assign_department_manager", kwargs={
                "department_id": "dept_hr_01",
                "manager_worker_id": "worker_0001"
            })
        ],
        outputs=[]
    )
]
