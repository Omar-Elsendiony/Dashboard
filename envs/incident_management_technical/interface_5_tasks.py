from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="1",
        user_id="40",
        instruction=(
            "Handle a critical multi-system incident affecting production services. "
            "First, examine the incident tracking system to retrieve full details about the critical network outage. "
            "Update the incident to reflect its critical severity and business impact. "
            "Escalate the incident to executive management providing detailed business impact justification. "
            "Examine all affected configuration items and infrastructure assets to understand the scope. "
            "Create an emergency change request to activate disaster recovery procedures with detailed implementation steps. "
            "Set up a coordination bridge as a war room to bring together all technical leads for synchronized response. "
            "Review active customer service level agreements to understand contractual obligations and response time requirements. "
            "Initiate a comprehensive post-incident improvement initiative focused on disaster recovery procedure enhancements. "
            "Generate an executive summary incident report documenting the timeline, impact, and recovery actions. "
            "Finally, examine audit trail records to ensure all critical actions are properly logged for compliance."
        ),
        actions=[
            # Step 1: Examine incident details
            Action(name="discover_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "35"
                }
            }),
            
            # Step 2: Update incident to critical severity
            Action(name="manage_incidents", kwargs={
                "action": "update",
                "incident_id": "35",
                "incident_data": {
                    "severity": "P1",
                    "impact": "critical",
                    "urgency": "critical",
                    "status": "in_progress"
                }
            }),
            
            # Step 3: Escalate to executive management
            Action(name="manage_escalations", kwargs={
                "action": "create",
                "escalation_data": {
                    "incident_id": "35",
                    "escalated_from": "40",
                    "escalated_to": "351",
                    "escalation_reason": "Business-critical multi-system network outage requiring executive coordination and customer communication"
                }
            }),
            
            # Step 4: Examine affected configuration items
            Action(name="discover_assets", kwargs={
                "entity_type": "configuration_items",
                "filters": {
                    "status": "active"
                }
            }),
            
            # Step 5: Create emergency change request
            Action(name="manage_change_control", kwargs={
                "action": "create",
                "change_request_data": {
                    "title": "Emergency Disaster Recovery Activation",
                    "description": "Activate disaster recovery procedures for critical network outage affecting all production services",
                    "change_type": "emergency",
                    "risk_level": "critical",
                    "requested_by": "40",
                    "incident_id": "35"
                }
            }),
            
            # Step 6: Set up war room coordination bridge
            Action(name="manage_coordinations", kwargs={
                "entity_type": "bridge",
                "action": "create",
                "bridge_data": {
                    "incident_id": "35",
                    "bridge_type": "coordination",
                    "bridge_host": "40"
                }
            }),
            
            # Step 7: Review customer SLA agreements
            Action(name="discover_contracts", kwargs={
                "entity_type": "sla_agreements",
                "filters": {
                    "status": "active"
                }
            }),
            
            # Step 8: Initiate improvement initiative (Note: Requires root_cause_analyses or post_incident_reviews table)
            Action(name="manage_work_notes", kwargs={
                "action": "create",
                "note_data": {
                    "incident_id": "35",
                    "note_text": "Comprehensive disaster recovery review initiated. Focus areas: 1) Failover mechanisms 2) Network redundancy 3) Business continuity procedures 4) Customer communication protocols",
                    "note_type": "progress_update",
                    "created_by": "40"
                }
            }),
            
            # Step 9: Generate executive incident report
            Action(name="manage_incident_reports", kwargs={
                "action": "create",
                "incident_id": "35",
                "report_title": "Executive Summary: Critical Multi-System Network Outage",
                "report_type": "post_incident_review",
                "report_content": "EXECUTIVE SUMMARY: Critical network outage affecting all production services. Multiple systems impacted. Disaster recovery procedures activated. Estimated business impact: Service disruption across all customer-facing applications. Recovery actions: 1) Disaster recovery site activation 2) System failover procedures 3) Service restoration and validation 4) Customer communication coordination. Root cause investigation ongoing.",
                "generated_by": "40"
            }),
            
            # Step 10: Examine audit records for compliance
            Action(name="discover_audit", kwargs={
                "entity_type": "audit_trails",
                "filters": {
                    "reference_id": "35",
                    "reference_type": "incident"
                }
            })
        ],
        outputs=["35", "351"]
    ),
]