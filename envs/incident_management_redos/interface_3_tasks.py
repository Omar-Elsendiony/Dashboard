from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="1",
        user_id="15",
        instruction=(
            "You are an operations manager handling a critical infrastructure incident. "
            "A P1 severity hardware failure has occurred (incident_id: 75). You need to query the incident tracking system "
            "to get incident details, then execute incident management operations to update the status to 'in_progress'. "
            "Process a change control request for emergency hardware replacement, and operate coordination activities "
            "with the datacenter team. Execute work order operations to create a task for hardware replacement with critical priority. "
            "Query audit information to see the incident history, then execute improvements by creating a post-incident review "
            "planning entry. Finally, relay to human escalation if the incident is not resolved within 1 hour."
        ),
        actions=[
            Action(name="query_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "75"
                }
            }),
            Action(name="execute_incident_operations", kwargs={
                "action": "update",
                "incident_id": "75",
                "incident_data": {
                    "status": "in_progress",
                    "severity": "P1",
                    "acknowledged_at": "2025-10-20T09:00:00"
                }
            }),
            Action(name="process_change_control", kwargs={
                "action": "create",
                "change_request_data": {
                    "incident_id": "75",
                    "requested_by": "15",
                    "change_type": "emergency",
                    "description": "Emergency server replacement for failed hardware",
                    "implementation_plan": "1. Prepare replacement server 2. Migrate data 3. Switch over 4. Verify operations",
                    "risk_level": "high",
                    "status": "pending"
                }
            }),
            Action(name="operate_coordinations", kwargs={
                "action": "create",
                "coordination_data": {
                    "incident_id": "75",
                    "coordinator_type": "internal_team",
                    "coordinator_name": "Datacenter Operations Team",
                    "coordination_purpose": "Emergency hardware replacement coordination",
                    "status": "active"
                }
            }),
            Action(name="execute_work_order_operations", kwargs={
                "action": "create",
                "work_order_data": {
                    "incident_id": "75",
                    "assigned_to": "25",
                    "description": "Replace failed server hardware in datacenter rack A23",
                    "priority": "critical",
                    "status": "assigned"
                }
            }),
            Action(name="query_audit_information", kwargs={
                "entity_type": "audit_trail",
                "filters": {
                    "entity_id": "75",
                    "entity_type": "incident"
                }
            }),
            Action(name="execute_improvements", kwargs={
                "action": "create",
                "improvement_data": {
                    "incident_id": "75",
                    "improvement_type": "post_incident_review",
                    "title": "Hardware failure - preventive measures review",
                    "description": "Review hardware monitoring and predictive maintenance procedures",
                    "status": "planned"
                }
            }),
            Action(name="relay_to_human", kwargs={
                "reason": "P1 critical incident requires management oversight",
                "incident_id": "75",
                "escalation_level": "executive"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="20",
        instruction=(
            "You are a security incident coordinator. A security breach incident (incident_id: 120) has been detected. "
            "Query the parties involved to find all security team members. Execute incident operations to mark it as critical P1 severity. "
            "Operate contracts with the security audit firm to initiate immediate investigation. "
            "Query assets that might be affected by checking all configuration items linked to the incident. "
            "Process incident reports to document the security breach details. Execute work notes to log all security actions taken. "
            "Operate improvements to create a root cause analysis task. Finally, capture audit records for compliance."
        ),
        actions=[
            Action(name="query_parties", kwargs={
                "entity_type": "users",
                "filters": {
                    "role": "security_analyst"
                }
            }),
            Action(name="query_incident_tracking", kwargs={
                "entity_type": "incidents",
                "filters": {
                    "incident_id": "120"
                }
            }),
            Action(name="execute_incident_operations", kwargs={
                "action": "update",
                "incident_id": "120",
                "incident_data": {
                    "severity": "P1",
                    "impact": "critical",
                    "urgency": "critical",
                    "status": "in_progress"
                }
            }),
            Action(name="operate_contracts", kwargs={
                "action": "create",
                "contract_data": {
                    "client_id": "5",
                    "contract_type": "security_audit",
                    "service_description": "Emergency security breach investigation",
                    "start_date": "2025-10-20",
                    "status": "active"
                }
            }),
            Action(name="query_assets", kwargs={
                "entity_type": "configuration_items",
                "filters": {
                    "ci_type": "server"
                }
            }),
            Action(name="process_incident_reports", kwargs={
                "action": "create",
                "report_data": {
                    "incident_id": "120",
                    "report_type": "security_breach",
                    "summary": "Unauthorized access detected on production servers",
                    "detailed_findings": "Multiple failed authentication attempts followed by successful breach. Data access logged.",
                    "created_by": "20"
                }
            }),
            Action(name="execute_work_notes", kwargs={
                "action": "create",
                "work_note_data": {
                    "incident_id": "120",
                    "created_by": "20",
                    "note_text": "Security team notified. External audit firm engaged. Access logs secured for forensic analysis.",
                    "note_type": "security"
                }
            }),
            Action(name="operate_improvements", kwargs={
                "action": "create",
                "improvement_data": {
                    "incident_id": "120",
                    "improvement_type": "root_cause_analysis",
                    "title": "Security breach root cause investigation",
                    "description": "Comprehensive analysis of security breach vectors and prevention measures",
                    "status": "in_progress"
                }
            }),
            Action(name="capture_audit_records", kwargs={
                "action": "create",
                "audit_data": {
                    "entity_type": "incident",
                    "entity_id": "120",
                    "action_type": "security_response",
                    "performed_by": "20",
                    "description": "Security incident response procedures initiated"
                }
            })
        ],
        outputs=[]
    )
]
