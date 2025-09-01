from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are Paula Holmes (pholmes@corp.org), an incident manager in Technical Operations. "
            "A critical security incident has been reported involving unauthorized access to the client database. "
            "The incident affects client Garcia Ltd and was detected on their authentication component. "
            "You need to record this high-priority incident with the title 'Unauthorized Database Access Attempt' "
            "and categorize it as a 'security_breach'. The impact should be set to 'high' since it involves "
            "client data security. The incident was detected at 2025-09-01T08:00:00. "
            "You need to assign this incident to yourself as the incident manager and get the user details "
            "for the reporter who identified this issue."
        ),
        actions=[
            Action(name="get_users", kwargs={
                "email": "pholmes@corp.org"
            }),
            Action(name="get_clients", kwargs={
                "client_name_contains": "Garcia"
            }),
            Action(name="get_components", kwargs={
                "client_id": "1"
            }),
            Action(name="record_incident", kwargs={
                "title": "Unauthorized Database Access Attempt",
                "category": "security_breach",
                "impact": "high",
                "client_id": "1",
                "reporter_id": "67",
                "detected_at": "2025-09-01T08:00:00",
                "component_id": "1",
                "assigned_manager_id": "1",
                "p2_risk_high_priority_sla_breach": True
            }),
            Action(name="get_users", kwargs={
                "user_id": "67"
            }),
            Action(name="get_incidents", kwargs={
                "title": "Unauthorized Database Access Attempt"
            })
        ],
        outputs=[]
    )
]
