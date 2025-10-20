from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="1",
        user_id="40",
        instruction=(
            "You are a senior operations manager handling a complex multi-system incident (incident_id: 300). "
            "You need to examine incident tracking to get full incident details, then regulate the incident by "
            "escalating it to executive management due to business impact. "
            "Examine assets to identify all affected configuration items across systems. "
            "Facilitate change control for emergency system recovery procedures. "
            "Regulate coordinations by setting up a war room with all technical leads. "
            "Examine contracts to verify customer SLA obligations. "
            "Facilitate improvements by initiating a comprehensive disaster recovery review. "
            "Regulate incident reports to document the full incident timeline and impact. "
            "Examine audit records for compliance and governance requirements. "
            "Finally, delegate to human executive team for final decision making."
        ),
        actions=[
            Action(name="examine_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "300"
                }
            }),
            Action(name="regulate_incidents", kwargs={
                "action": "update",
                "incident_id": "300",
                "incident_data": {
                    "severity": "P1",
                    "impact": "critical",
                    "urgency": "critical",
                    "status": "monitoring"
                }
            }),
            Action(name="regulate_escalations", kwargs={
                "action": "create",
                "escalation_data": {
                    "incident_id": "300",
                    "escalated_to": "5",
                    "escalation_reason": "Business-critical multi-system failure",
                    "escalation_level": "executive",
                    "status": "escalated"
                }
            }),
            Action(name="examine_assets", kwargs={
                "entity_type": "configuration_items",
                "filters": {
                    "status": "impacted"
                }
            }),
            Action(name="facilitate_change_control", kwargs={
                "action": "create",
                "change_request_data": {
                    "incident_id": "300",
                    "requested_by": "40",
                    "change_type": "emergency",
                    "description": "Emergency disaster recovery procedures activation",
                    "implementation_plan": "1. Activate DR site 2. Failover systems 3. Data synchronization 4. Service restoration 5. Validation",
                    "risk_level": "critical",
                    "status": "approved"
                }
            }),
            Action(name="regulate_coordinations", kwargs={
                "action": "create",
                "coordination_data": {
                    "incident_id": "300",
                    "coordinator_type": "war_room",
                    "coordinator_name": "Emergency Operations War Room",
                    "coordination_purpose": "Coordinate multi-team disaster recovery efforts",
                    "status": "active"
                }
            }),
            Action(name="examine_contracts", kwargs={
                "entity_type": "sla_agreements",
                "filters": {
                    "status": "active",
                    "sla_type": "platinum"
                }
            }),
            Action(name="facilitate_improvements", kwargs={
                "action": "create",
                "improvement_data": {
                    "incident_id": "300",
                    "improvement_type": "disaster_recovery_review",
                    "title": "Comprehensive DR procedures enhancement",
                    "description": "Full review of disaster recovery procedures, failover mechanisms, and business continuity plans",
                    "status": "critical"
                }
            }),
            Action(name="regulate_incident_reports", kwargs={
                "action": "create",
                "report_data": {
                    "incident_id": "300",
                    "report_type": "executive_summary",
                    "summary": "Critical multi-system failure - disaster recovery procedures activated",
                    "detailed_findings": "Cascading failure across multiple systems. DR site activated. Business impact: 2 hours downtime affecting all services.",
                    "created_by": "40"
                }
            }),
            Action(name="examine_audit_records", kwargs={
                "entity_type": "audit_trail",
                "filters": {
                    "entity_id": "300",
                    "entity_type": "incident",
                    "action_type": "critical"
                }
            }),
            Action(name="delegate_to_human", kwargs={
                "reason": "Business-critical incident requires executive decision on customer communications and PR strategy",
                "incident_id": "300",
                "escalation_level": "c_level"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="42",
        instruction=(
            "You are a compliance and audit manager reviewing a resolved security incident (incident_id: 350). "
            "You need to examine incident tracking and audit records to verify all procedures were followed correctly. "
            "Examine parties involved in the incident resolution to identify all responders. "
            "Regulate incident reports by creating a comprehensive compliance report. "
            "Examine workflows to ensure proper change management procedures were followed. "
            "Facilitate improvements by creating lessons learned documentation. "
            "Examine contracts to verify all client notification requirements were met. "
            "Regulate communications to send final incident closure notification. "
            "Examine audit records for the complete audit trail. "
            "Finally, confirm authorization was properly obtained for all actions taken."
        ),
        actions=[
            Action(name="examine_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "350",
                    "status": "resolved"
                }
            }),
            Action(name="examine_audit_records", kwargs={
                "entity_type": "audit_trail",
                "filters": {
                    "entity_id": "350",
                    "entity_type": "incident"
                }
            }),
            Action(name="examine_parties", kwargs={
                "entity_type": "users",
                "filters": {
                    "status": "active"
                }
            }),
            Action(name="regulate_incident_reports", kwargs={
                "action": "create",
                "report_data": {
                    "incident_id": "350",
                    "report_type": "compliance_report",
                    "summary": "Security incident resolution - compliance verification",
                    "detailed_findings": "All security procedures followed. Incident response timeline within SLA. Client notification completed. No compliance violations identified.",
                    "created_by": "42"
                }
            }),
            Action(name="examine_workflows", kwargs={
                "entity_type": "change_requests",
                "filters": {
                    "incident_id": "350",
                    "status": "completed"
                }
            }),
            Action(name="facilitate_improvements", kwargs={
                "action": "create",
                "improvement_data": {
                    "incident_id": "350",
                    "improvement_type": "lessons_learned",
                    "title": "Security incident response lessons learned",
                    "description": "Documentation of successful response procedures and identified areas for improvement",
                    "status": "documented"
                }
            }),
            Action(name="examine_contracts", kwargs={
                "entity_type": "sla_agreements",
                "filters": {
                    "status": "active"
                }
            }),
            Action(name="regulate_communications", kwargs={
                "action": "create",
                "communication_data": {
                    "incident_id": "350",
                    "communication_type": "closure_notification",
                    "subject": "Incident Closure - INC0000350",
                    "message": "The security incident has been fully resolved. All systems verified operational. Compliance report available upon request.",
                    "sent_by": "42",
                    "status": "sent"
                }
            }),
            Action(name="examine_audit_records", kwargs={
                "entity_type": "audit_trail",
                "filters": {
                    "entity_type": "incident",
                    "action_type": "compliance_check"
                }
            }),
            Action(name="confirm_authorization", kwargs={
                "user_id": "42",
                "action_type": "compliance_review",
                "resource": "incident_records"
            })
        ],
        outputs=[]
    )
]
