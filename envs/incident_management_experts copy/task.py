from tau_bench.types import Action, Task

tasks = [
    Task(
        annotator="general",
        user_id="0",
        instruction=(
            "You are an Incident Management Expert System Agent. You operate across all incident "
            "management interfaces and are responsible for handling all incidents according to the "
            "incident policy. You must verify user identity, validate role-based approvals, "
            "perform discovery, manage incident lifecycle actions, enforce compliance, and maintain "
            "full audit trails."
        ),
        actions=[
            # Identity verification
            Action(name="check_approval", kwargs={
                "action": "user_identity_verification",
                "requester_email": "system_admin@company.com"
            }),
            
            # Incident discovery
            Action(name="discover_incidents", kwargs={
                "search_criteria": "all_open",
                "priority": "high"
            }),
            
            # Incident lifecycle management
            Action(name="manage_incident", kwargs={
                "action": "create",
                "incident_type": "security_breach",
                "reported_by": "usr_001",
                "priority": "critical",
                "system_administrator_approval": True
            }),
            Action(name="manage_incident", kwargs={
                "action": "update",
                "incident_id": "inc_001",
                "status": "investigation",
                "incident_manager_approval": True
            }),
            Action(name="manage_incident", kwargs={
                "action": "resolve",
                "incident_id": "inc_001",
                "resolution_summary": "Mitigation completed",
                "incident_manager_approval": True,
                "system_administrator_approval": True
            }),
            
            # Notifications & Escalations
            Action(name="notify_team", kwargs={
                "incident_id": "inc_001",
                "recipients": ["it_team", "security_team"],
                "notification_type": "escalation"
            }),
            
            # Audit & Compliance
            Action(name="check_approval", kwargs={
                "action": "audit_trail",
                "reference_id": "inc_001",
                "operation": "incident_lifecycle_complete"
            }),
            Action(name="manage_document_storage", kwargs={
                "action": "upload",
                "incident_id": "inc_001",
                "document_type": "investigation_report",
                "confidentiality_level": "high",
                "retention_years": 5
            }),
            
            # Post-Incident Review
            Action(name="manage_post_incident_review", kwargs={
                "action": "conduct_review",
                "incident_id": "inc_001",
                "reviewer_id": "system_admin",
                "incident_manager_approval": True
            })
        ],
        outputs=[]
    )
]
