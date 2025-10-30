from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Robert Soto (robert.soto@techcorp.com), an incident manager. "
            "A network incident has been reported by client 'Baldwin Ltd' (client_id: 2). "
            "You need to search for the client information, then handle the incident by creating a new incident record "
            "with category 'network', severity P2, high impact and high urgency. The incident title should be "
            "'VPN connectivity issues affecting multiple users' with appropriate description. "
            "After creating the incident, compute its severity based on the impact and urgency, "
            "then handle an approval request for emergency change to fix the network configuration. "
            "Create a communication record to notify the client about the incident and expected resolution time."
        ),
        actions=[
            Action(name="search_parties", kwargs={
                "entity_type": "clients",
                "filters": {
                    "client_name": "Baldwin Ltd"
                }
            }),
            Action(name="search_parties", kwargs={
                "entity_type": "users",
                "filters": {
                    "email": "robert.soto@techcorp.com"
                }
            }),
            Action(name="handle_incidents", kwargs={
                "action": "create",
                "incident_data": {
                    "title": "VPN connectivity issues affecting multiple users",
                    "description": "Multiple users from Baldwin Ltd reporting VPN connection failures. Intermittent disconnections and authentication errors observed. Affecting business operations.",
                    "category": "network",
                    "severity": "P2",
                    "impact": "high",
                    "urgency": "high",
                    "status": "open",
                    "reported_by": "2"
                }
            }),
            Action(name="compute_incident_severity", kwargs={
                "incident_id": "1001",
                "category": "network",
                "impact": "high",
                "urgency": "high"
            }),
            Action(name="handle_approval_requests", kwargs={
                "action": "create",
                "approval_request_data": {
                    "incident_id": "1001",
                    "requested_by": "2",
                    "approval_type": "change_request",
                    "description": "Emergency network configuration change to resolve VPN issues",
                    "priority": "high",
                    "status": "pending"
                }
            }),
            Action(name="handle_communications", kwargs={
                "action": "create",
                "communication_data": {
                    "incident_id": "1001",
                    "client_id": "2",
                    "communication_type": "email",
                    "subject": "VPN Incident Notification",
                    "message": "We are aware of the VPN connectivity issues affecting your organization. Our team is working on resolution. Expected resolution time: 2 hours.",
                    "sent_by": "2",
                    "status": "sent"
                }
            }),
            Action(name="record_audit_records", kwargs={
                "action": "create",
                "audit_data": {
                    "entity_type": "incident",
                    "entity_id": "1001",
                    "action_type": "create",
                    "performed_by": "2",
                    "description": "New network incident created for Baldwin Ltd VPN issues"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="8",
        instruction=(
            "You are a technical specialist managing incidents. An incident (INC0000025) related to database performance "
            "has been assigned to you. You need to search for this incident, then handle it by updating the status to "
            "'in_progress'. Create a problem ticket to track the root cause of recurring database slowness issues. "
            "Handle a change control request for database optimization with description 'Index optimization and query tuning'. "
            "After implementing the change, handle the incident by updating it to 'resolved' status and "
            "acquire any SLA breach incidents that might have occurred during this time."
        ),
        actions=[
            Action(name="search_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_number": "INC0000025"
                }
            }),
            Action(name="handle_incidents", kwargs={
                "action": "update",
                "incident_id": "25",
                "incident_data": {
                    "status": "in_progress",
                    "acknowledged_at": "2025-10-20T11:00:00"
                }
            }),
            Action(name="handle_problem_tickets", kwargs={
                "action": "create",
                "problem_data": {
                    "title": "Recurring database performance degradation",
                    "description": "Multiple incidents reported regarding database slowness. Root cause analysis needed for long-term resolution.",
                    "category": "database",
                    "priority": "high",
                    "status": "open",
                    "created_by": "8"
                }
            }),
            Action(name="handle_change_control", kwargs={
                "action": "create",
                "change_request_data": {
                    "incident_id": "25",
                    "requested_by": "8",
                    "change_type": "standard",
                    "description": "Index optimization and query tuning",
                    "implementation_plan": "1. Analyze slow queries 2. Create missing indexes 3. Optimize existing queries 4. Test performance improvements",
                    "risk_level": "medium",
                    "status": "approved"
                }
            }),
            Action(name="handle_incidents", kwargs={
                "action": "update",
                "incident_id": "25",
                "incident_data": {
                    "status": "resolved",
                    "resolved_at": "2025-10-20T15:00:00"
                }
            }),
            Action(name="acquire_sla_breach_incidents", kwargs={
                "severity": "P2"
            }),
            Action(name="record_audit_records", kwargs={
                "action": "create",
                "audit_data": {
                    "entity_type": "incident",
                    "entity_id": "25",
                    "action_type": "resolve",
                    "performed_by": "8",
                    "description": "Database incident resolved after optimization changes"
                }
            })
        ],
        outputs=[]
    )
]
