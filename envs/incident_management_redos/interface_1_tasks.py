from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="1",
        user_id="1",
        instruction=(
            "You are Melissa Jones (melissa.jones@outlook.com), an incident manager. "
            "A critical software incident (INC0000001) has been reported with intermittent application errors. "
            "You need to handle this incident by first discovering the incident details, then assessing its severity. "
            "After assessment, update the incident status to 'in_progress' and assign it to user ID 50 (a technical specialist). "
            "Create a work order with the description 'Investigate and fix application errors' with high priority. "
            "Add a work note documenting 'Initial assessment completed, assigned to technical team for resolution'. "
            "Finally, log an audit record for tracking purposes."
        ),
        actions=[
            Action(name="discover_parties", kwargs={
                "entity_type": "users",
                "filters": {
                    "email": "melissa.jones@outlook.com"
                }
            }),
            Action(name="discover_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_number": "INC0000001"
                }
            }),
            Action(name="assess_incident_severity", kwargs={
                "incident_id": "1",
                "category": "software",
                "impact": "medium",
                "urgency": "medium"
            }),
            Action(name="manage_incidents", kwargs={
                "action": "update",
                "incident_id": "1",
                "incident_data": {
                    "status": "in_progress",
                    "assigned_to": "50",
                    "severity": "P3",
                    "acknowledged_at": "2025-10-20T10:00:00"
                }
            }),
            Action(name="manage_work_orders", kwargs={
                "action": "create",
                "work_order_data": {
                    "incident_id": "1",
                    "assigned_to": "50",
                    "description": "Investigate and fix application errors",
                    "priority": "high",
                    "status": "pending"
                }
            }),
            Action(name="manage_work_notes", kwargs={
                "action": "create",
                "work_note_data": {
                    "incident_id": "1",
                    "created_by": "1",
                    "note_text": "Initial assessment completed, assigned to technical team for resolution",
                    "note_type": "internal"
                }
            }),
            Action(name="log_audit_records", kwargs={
                "action": "create",
                "audit_data": {
                    "entity_type": "incident",
                    "entity_id": "1",
                    "action_type": "update",
                    "performed_by": "1",
                    "description": "Incident status updated to in_progress and assigned to technical team"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="5",
        instruction=(
            "You are a senior incident manager. There is a P1 severity hardware incident (INC0000050) "
            "that has breached its SLA. You need to check if there are any SLA breach incidents, "
            "then escalate this incident to management. Create an escalation with reason 'SLA breach - critical hardware failure', "
            "and coordinate with external vendor 'TechSupport Inc' for immediate assistance. "
            "Update the incident to add problem ticket ID 10 to track the root cause analysis."
        ),
        actions=[
            Action(name="get_sla_breach_incidents", kwargs={
                "severity": "P1"
            }),
            Action(name="discover_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_number": "INC0000050"
                }
            }),
            Action(name="manage_escalations", kwargs={
                "action": "create",
                "escalation_data": {
                    "incident_id": "50",
                    "escalated_to": "10",
                    "escalation_reason": "SLA breach - critical hardware failure",
                    "escalation_level": "management",
                    "status": "pending"
                }
            }),
            Action(name="manage_coordinations", kwargs={
                "action": "create",
                "coordination_data": {
                    "incident_id": "50",
                    "coordinator_type": "external_vendor",
                    "coordinator_name": "TechSupport Inc",
                    "coordination_purpose": "Emergency hardware replacement and repair",
                    "status": "initiated"
                }
            }),
            Action(name="manage_incidents", kwargs={
                "action": "update",
                "incident_id": "50",
                "incident_data": {
                    "problem_id": "10",
                    "status": "monitoring"
                }
            }),
            Action(name="log_audit_records", kwargs={
                "action": "create",
                "audit_data": {
                    "entity_type": "incident",
                    "entity_id": "50",
                    "action_type": "escalate",
                    "performed_by": "5",
                    "description": "Incident escalated due to SLA breach"
                }
            })
        ],
        outputs=[]
    )
]
