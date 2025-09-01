from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="37",
        instruction=(
            "You are an incident manager analyzing recent incident patterns and working on improving "
            "the overall incident management process. You've noticed that there have been recurring "
            "performance issues with database-related incidents. You need to review the metrics for "
            "recent incidents, particularly those involving database components, and create comprehensive "
            "documentation to help prevent similar issues in the future. You should log a knowledge base "
            "article with best practices for database performance monitoring, document lessons learned "
            "from recent incidents in a post-incident review, and analyze the root cause patterns. "
            "Additionally, you want to add an incident report summarizing the recent database performance trends "
            "and recommend improvements to the monitoring and alerting systems."
        ),
        actions=[
            Action(name="list_incidents", kwargs={
                "category": "performance_issue"
            }),
            Action(name="list_users", kwargs={
                "role": "incident_manager"
            }),
            Action(name="list_metrics", kwargs={
                "metric_type": "incident_resolution_time"
            }),
            Action(name="log_knowledge_base_article", kwargs={
                "title": "Database Performance Monitoring Best Practices",
                "category": "performance_issue",
                "content": "Comprehensive guide for monitoring database performance including query optimization, index management, and connection pooling strategies",
                "severity_level": "medium",
                "author_id": "37"
            }),
            Action(name="log_post_incident_review", kwargs={
                "incident_id": "7",
                "review_summary": "Analysis of recent database deadlock incidents and resolution patterns",
                "lessons_learned": "Proactive monitoring of lock contention and query performance critical for prevention",
                "action_items": "Implement automated alerts for long-running queries and lock timeouts",
                "conducted_by": "37"
            }),
            Action(name="log_root_cause_analysis", kwargs={
                "incident_id": "52",
                "root_cause": "High transaction volume causing deadlocks in customer database",
                "analysis_details": "Concurrent transactions on same resources without proper isolation",
                "prevention_measures": "Query optimization and transaction timeout configuration",
                "analyst_id": "37"
            }),
            Action(name="log_incident_report", kwargs={
                "title": "Database Performance Trends Analysis - Q3 2025",
                "incident_category": "performance_issue",
                "summary": "Comprehensive analysis of database-related incidents showing increasing trend in deadlock occurrences",
                "recommendations": "Enhanced monitoring, query optimization training, and improved database configuration",
                "report_period_start": "2025-07-01",
                "report_period_end": "2025-09-01",
                "created_by": "37"
            }),
            Action(name="list_root_cause_analyses", kwargs={
                "category": "performance_issue"
            })
        ],
        outputs=[]
    )
]
