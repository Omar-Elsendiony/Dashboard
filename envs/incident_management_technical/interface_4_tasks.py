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
        ),
        actions=[
            Action(name="retrieve_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "200"
                }
            }),
            Action(name="address_incidents", kwargs={
                "action": "update",
                "incident_id": "200",
                "incident_data": {
                    "urgency": "high",
                    "impact": "high",
                    "status": "in_progress"
                }
            }),
            Action(name="address_coordinations", kwargs={
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
            })
        ],
        outputs=[]
    )
]
