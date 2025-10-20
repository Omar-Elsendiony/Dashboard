from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="1",
        user_id="30",
        instruction=(
            "You are a service desk manager. A software incident (incident_id: 200) has been reported by multiple clients. "
            "You need to retrieve incident tracking data to understand the scope, then administer the incident by updating "
            "its priority to high. Coordinate with stakeholders by creating a bridge call for all affected parties. "
            "Retrieve assets information to identify all affected software configuration items. "
            "Oversee change control by creating an emergency patch deployment request. "
            "Administer work orders for the development team to create and deploy the fix. "
            "Retrieve contracts to check SLA commitments with affected clients. "
            "Finally, monitor audit trail and hand over to human support if escalation is needed."
        ),
        actions=[
            Action(name="retrieve_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "200"
                }
            }),
            Action(name="administer_incidents", kwargs={
                "action": "update",
                "incident_id": "200",
                "incident_data": {
                    "urgency": "high",
                    "impact": "high",
                    "status": "in_progress"
                }
            }),
            Action(name="coordinate_stakeholders", kwargs={
                "action": "create",
                "coordination_data": {
                    "incident_id": "200",
                    "coordinator_type": "bridge_call",
                    "coordinator_name": "Emergency Response Bridge",
                    "coordination_purpose": "Multi-client software issue resolution coordination",
                    "status": "scheduled"
                }
            }),
            Action(name="retrieve_assets", kwargs={
                "entity_type": "configuration_items",
                "filters": {
                    "ci_type": "software",
                    "status": "active"
                }
            }),
            Action(name="oversee_change_control", kwargs={
                "action": "create",
                "change_request_data": {
                    "incident_id": "200",
                    "requested_by": "30",
                    "change_type": "emergency",
                    "description": "Emergency software patch deployment for critical bug fix",
                    "implementation_plan": "1. Code review 2. QA testing 3. Staged rollout 4. Production deployment 5. Monitoring",
                    "risk_level": "medium",
                    "status": "pending"
                }
            }),
            Action(name="administer_work_orders", kwargs={
                "action": "create",
                "work_order_data": {
                    "incident_id": "200",
                    "assigned_to": "45",
                    "description": "Develop and deploy software patch for incident INC0000200",
                    "priority": "critical",
                    "status": "assigned"
                }
            }),
            Action(name="retrieve_contracts", kwargs={
                "entity_type": "sla_agreements",
                "filters": {
                    "status": "active"
                }
            }),
            Action(name="monitor_audit_trail", kwargs={
                "entity_type": "audit_trail",
                "filters": {
                    "entity_id": "200",
                    "entity_type": "incident"
                }
            }),
            Action(name="hand_over_to_human", kwargs={
                "reason": "Multiple client impact requires senior management notification",
                "incident_id": "200",
                "escalation_level": "senior_management"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="35",
        instruction=(
            "You are an IT operations lead managing infrastructure. A network incident (incident_id: 250) has caused "
            "connectivity issues affecting multiple departments. Retrieve parties information to identify all network administrators. "
            "Administer the incident by assigning it to the network team lead (user_id: 55). "
            "Retrieve workflow information to understand the standard network incident resolution process. "
            "Coordinate stakeholders to notify all affected departments about the outage. "
            "Oversee improvements by creating a preventive maintenance plan. "
            "Administer communications to send status updates to all impacted users. "
            "Retrieve audit information to document all actions taken. "
            "Finally, verify authorization for implementing network changes and monitor audit trail."
        ),
        actions=[
            Action(name="retrieve_parties", kwargs={
                "entity_type": "users",
                "filters": {
                    "role": "network_admin"
                }
            }),
            Action(name="retrieve_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "250"
                }
            }),
            Action(name="administer_incidents", kwargs={
                "action": "update",
                "incident_id": "250",
                "incident_data": {
                    "assigned_to": "55",
                    "status": "in_progress",
                    "acknowledged_at": "2025-10-20T13:00:00"
                }
            }),
            Action(name="retrieve_workflows", kwargs={
                "entity_type": "work_orders",
                "filters": {
                    "incident_id": "250"
                }
            }),
            Action(name="coordinate_stakeholders", kwargs={
                "action": "create",
                "coordination_data": {
                    "incident_id": "250",
                    "coordinator_type": "internal_notification",
                    "coordinator_name": "Department Coordination",
                    "coordination_purpose": "Network outage notification and status updates",
                    "status": "active"
                }
            }),
            Action(name="oversee_improvements", kwargs={
                "action": "create",
                "improvement_data": {
                    "incident_id": "250",
                    "improvement_type": "preventive_maintenance",
                    "title": "Network infrastructure maintenance schedule",
                    "description": "Implement regular network equipment checks and redundancy testing",
                    "status": "proposed"
                }
            }),
            Action(name="administer_communications", kwargs={
                "action": "create",
                "communication_data": {
                    "incident_id": "250",
                    "communication_type": "broadcast",
                    "subject": "Network Incident Status Update",
                    "message": "Network connectivity issue identified. Team working on resolution. Expected restoration: 2 hours.",
                    "sent_by": "35",
                    "status": "sent"
                }
            }),
            Action(name="retrieve_audit_information", kwargs={
                "entity_type": "audit_trail",
                "filters": {
                    "entity_id": "250",
                    "entity_type": "incident"
                }
            }),
            Action(name="verify_authorization", kwargs={
                "user_id": "35",
                "action_type": "network_change",
                "resource": "network_infrastructure"
            }),
            Action(name="monitor_audit_trail", kwargs={
                "entity_type": "audit_trail",
                "filters": {
                    "performed_by": "35",
                    "action_type": "update"
                }
            })
        ],
        outputs=[]
    )
]
