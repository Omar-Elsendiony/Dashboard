from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="94",
        instruction=(
            "You are an incident manager who has been working on resolving a critical database performance "
            "incident (incident_id: 1) that has been affecting multiple clients. All the necessary fixes "
            "have been implemented and tested. You need to complete the incident resolution process by "
            "recording a post-incident review, creating a change request for the database optimization "
            "that was implemented, and documenting the root cause analysis. The incident involved webhook "
            "delivery failures due to database locks. You should also record final communications to "
            "stakeholders informing them that the incident has been resolved and normal operations have resumed."
        ),
        actions=[
            Action(name="query_incidents", kwargs={
                "incident_id": "1"
            }),
            Action(name="query_users", kwargs={
                "user_id": "94"
            }),
            Action(name="record_root_cause_analysis", kwargs={
                "incident_id": "1",
                "root_cause": "Database locks caused by inefficient queries blocking webhook delivery process",
                "analysis_details": "Long-running queries were holding locks on key tables, preventing webhook processing",
                "prevention_measures": "Query optimization and connection pooling implemented",
                "analyst_id": "94"
            }),
            Action(name="record_change_request", kwargs={
                "incident_id": "1",
                "change_type": "database_optimization",
                "description": "Optimize database queries and implement connection pooling for webhook delivery",
                "impact_assessment": "Improved performance and reduced lock contention",
                "requested_by": "94"
            }),
            Action(name="record_communication", kwargs={
                "incident_id": "1",
                "communication_type": "resolution_notification",
                "message": "Webhook delivery incident has been resolved. Database optimization completed and normal operations resumed.",
                "recipient_type": "all_stakeholders",
                "sent_by": "94"
            }),
            Action(name="record_post_incident_review", kwargs={
                "incident_id": "1",
                "review_summary": "Database performance incident successfully resolved through query optimization",
                "lessons_learned": "Need for better query performance monitoring and connection pool management",
                "action_items": "Implement database performance alerts and regular query optimization reviews",
                "conducted_by": "94"
            }),
            Action(name="query_knowledge_base_articles", kwargs={
                "category": "performance_issue"
            })
        ],
        outputs=[]
    )
]
