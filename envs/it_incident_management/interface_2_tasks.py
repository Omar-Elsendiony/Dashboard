from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="2",
        instruction=(
            "You are Danny Wright (dwright@corp.org), an incident manager in Technical Operations. "
            "A network connectivity incident has been affecting multiple clients. You need to investigate "
            "which infrastructure components are experiencing issues and create a knowledge base article "
            "documenting the resolution steps for similar network-related incidents. The incident involves "
            "intermittent network timeouts on the API gateway component. You should also check for any "
            "existing SLA agreements that might be impacted and add a workaround for immediate relief "
            "while the permanent fix is being implemented."
        ),
        actions=[
            Action(name="fetch_users", kwargs={
                "email": "dwright@corp.org"
            }),
            Action(name="fetch_incidents", kwargs={
                "category": "integration_failure"
            }),
            Action(name="fetch_components", kwargs={
                "component_type": "api_endpoint"
            }),
            Action(name="fetch_sla_agreements", kwargs={
                "status": "active"
            }),
            Action(name="add_knowledge_base_article", kwargs={
                "title": "Network Timeout Resolution on API Gateway",
                "category": "integration_failure",
                "content": "For intermittent network timeouts on API gateway: 1) Check load balancer configuration 2) Verify DNS resolution 3) Test connection pools 4) Monitor for packet loss",
                "severity_level": "medium",
                "author_id": "2"
            }),
            Action(name="add_workaround", kwargs={
                "incident_id": "10",
                "description": "Temporary routing through backup API endpoint",
                "workaround_type": "temporary_fix",
                "created_by": "2"
            }),
            Action(name="log_incident", kwargs={
                "title": "API Gateway Network Timeouts",
                "category": "integration_failure",
                "severity": "P2",
                "impact": "high",
                "client_id": "91",
                "reporter_id": "28",
                "component_id": "4",
                "detected_at": "2025-09-01T10:00:00"
            })
        ],
        outputs=[]
    )
]
