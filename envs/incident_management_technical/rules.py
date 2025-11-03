RULES = [
    # Identity and Authorization
    "The assistant must acquire user information by using discover_parties at the beginning of any operation to identify the user and populate fields that reference the current user of the system.",
    "The assistant must log any create/update/delete operation using log_audit_records.",
    "The assistant must halt and use transfer_to_human if receiving any error from the tools or if a verification/validation step fails.",
    
    # User Account Management (SOP 1)
    "The assistant must obtain the user information (refer to manage_users tool documentation for field requirements) before creating a new user.",
    "The assistant must create a user record with all required and optional fields using manage_users when creating a new user.",
    "The assistant must retrieve current user record using discover_parties before updating an existent user information.",
    "The assistant must obtain the new values for the fields needed to be updated before applying modifications to user information.",
    "The assistant must apply the modifications using manage_users when updating user information.",
    
    # Incident Creation (SOP 2.1)
    "The assistant must gather severity assessment information including: whether there is a complete outage of business-critical services with no workaround, the scope of impact (enterprise-wide, multiple customers, number of affected parties), any regulatory/safety/financial implications, whether high-priority customers or recurrent incidents are involved, the level of service degradation (major or moderate) and availability of workarounds, whether multiple departments/sites/critical business functions are affected, any risk of breaching high-priority SLAs, and whether the impact is localized to a single department or function.",
    "The assistant must call assess_incident_severity tool with all the severity assessment information gathered.",
    "The assistant must use the returned severity from assess_incident_severity as the incident severity.",
    "The assistant must obtain the incident required and optional information, gathering as many optional fields as available (refer to manage_incidents tool documentation for field requirements) before creating an incident.",
    "The assistant must create a new incident using manage_incidents.",
    "The assistant must initiate a new incident bridge by following SOP 4.1 if the severity is P1 or P2 after creating an incident.",
    "The assistant must attribute the incident for each configuration item by following SOP 10 if affected configuration item(s) information were provided.",
    
    # Incident Update (SOP 2.2)
    "The assistant must obtain the information for the incident to be updated by using discover_incident_tracking before updating an incident.",
    "The assistant must confirm that the problem ticket exists and is not closed using discover_incident_tracking if problem_id is being updated.",
    "The assistant must validate that the user is active using discover_parties if assigned to user is being updated.",
    "The assistant must apply the change(s) using manage_incidents when updating an incident.",
    "The assistant must create a postmortem incident draft report using manage_incident_reports stating 'Incident [Incident ID] has been closed.' if the update sets status to 'closed'.",
    
    # Creating Incident Escalations (SOP 3)
    "The assistant must obtain the ID of the incident needed to be escalated by using discover_incident_tracking before creating an escalation.",
    "The assistant must validate incident has valid status (open or in_progress) for escalation.",
    "The assistant must confirm the target user exists and is active using discover_parties before creating an escalation.",
    "The assistant must create the escalation record with status pending using manage_escalations.",
    
    # Initiating an Incident Bridge (SOP 4.1)
    "The assistant must obtain the information for incident requiring bridge collaboration by using discover_incident_tracking before initiating an incident bridge.",
    "The assistant must validate that incident is in an open or in_progress state and has an assigned Incident Manager before initiating a bridge.",
    "The assistant must extract the Incident Manager assigned to the incident when initiating a bridge.",
    "The assistant must set the bridge type to 'major_incident' for P1 and P2 incidents, otherwise obtain the bridge type whether coordination, or technical.",
    "The assistant must obtain the required and optional bridge information (refer to manage_coordinations tool documentation for field requirements) before creating a bridge.",
    "The assistant must create the bridge record using manage_coordinations.",
    "The assistant must update the incident status to in_progress if its status is open using manage_incidents after creating the bridge.",
    "The assistant must add each participant by following SOP 4.2 if additional participants need to be added to the bridge.",
    
    # Adding Bridge Participants (SOP 4.2)
    "The assistant must obtain the bridge ID for adding participants by using discover_coordination before adding participants to a bridge.",
    "The assistant must validate that the bridge status is active before adding participants.",
    "The assistant must obtain the participant user information by using discover_parties for each participant to be added.",
    "The assistant must validate that the user status is active for each participant before adding them to the bridge.",
    "The assistant must obtain the participant's role in the bridge (host, technical_support, account_manager, or executive) for each participant.",
    "The assistant must check for existing participant to prevent duplicates using discover_coordination before adding each participant.",
    "The assistant must add the participant to the bridge using manage_coordinations after all validations are complete.",
    "The assistant must add a Work Note to the parent incident documenting the participant addition: 'Bridge participant(s) added to bridge [Bridge Number] for incident [Incident ID]' after adding participants.",
    
    # Closing an Incident Bridge (SOP 5)
    "The assistant must obtain the information for the bridge to close by using discover_coordination.",
    "The assistant must validate the bridge status is active and if the bridge is already Closed or Cancelled, stop and record a work note: 'Bridge already closed.' using manage_work_notes.",
    "The assistant must obtain the information for the incident associated with the bridge to close using incident ID retrieved and providing it to discover_incident_tracking tool.",
    "The assistant must confirm that the related incident associated with the bridge is in a Resolved or Monitoring state before closing the bridge.",
    "The assistant must validate the bridge host user is found and active using discover_parties before closing the bridge.",
    "The assistant must update the bridge status to closed using manage_coordinations.",
    "The assistant must add a Work Note for the parent incident: 'Bridge closed for the incident [Incident ID] by [User first name + User last name] after all activities completed.' after closing the bridge.",
    
    # Creating Problem Tickets (SOP 6)
    "The assistant must obtain the required information to create the problem ticket (refer to manage_problem_tickets tool documentation for field requirements) before creating a problem ticket.",
    "The assistant must create the Problem Ticket record using manage_problem_tickets.",
    "The assistant must retrieve details and confirm each incident record exists using discover_incident_tracking if any incidents are associated with this problem ticket.",
    "The assistant must establish a linkage between each incident and the newly created problem ticket by updating the incident records via manage_incidents for all incidents identified.",
    "The assistant must record 'Incident(s) linked to Problem Ticket [Problem ID]' in Work Notes by following SOP 14 after linking incidents to the problem ticket.",
    
    # Updating Problem Tickets (SOP 7)
    "The assistant must obtain the information to identify the problem ticket to update by using discover_incident_tracking before updating a problem ticket.",
    "The assistant must obtain the information to update (refer to manage_problem_tickets tool documentation for field requirements).",
    "The assistant must apply the status change and any optional fields using manage_problem_tickets.",
    "The assistant must record 'Problem ticket updated with new investigation details' in Work Notes using manage_work_notes after updating the problem ticket.",
    "The assistant must send notifications to the reporter of the incident by following SOP 11 if status changed to resolved or closed and the reporter is not the user conducting the action.",
    
    # Linking Incidents to Problem Tickets (SOP 8)
    "The assistant must obtain the incident to link to the problem ticket by using discover_incident_tracking.",
    "The assistant must obtain the problem ticket to link the incident to by using discover_incident_tracking.",
    "The assistant must update the incident record using manage_incidents and set problem_id to the problem ticket ID when linking an incident to a problem ticket.",
    "The assistant must record 'Incident linked to Problem Ticket [Problem Number]' in Work Notes for the incident using manage_work_notes.",
    "The assistant must record 'Incident [Incident Number] linked to this problem ticket' in Work Notes for the problem ticket using manage_work_notes.",
    "The assistant must send notification to the Incident Manager using manage_communications after linking an incident to a problem ticket.",
    
    # Linking Configuration Items to Problem Tickets (SOP 9)
    "The assistant must obtain the problem_id of the problem ticket to link the configuration item to by using discover_incident_tracking.",
    "The assistant must validate problem ticket exists and is not closed before linking a configuration item to it.",
    "The assistant must obtain the ID of the configuration item to link by using discover_assets.",
    "The assistant must check for existing relationship to prevent duplicates using discover_incident_tracking before creating the relationship.",
    "The assistant must create problem-Configuration item relationship using manage_incidents_problems_configuration_items.",
    
    # Linking Configuration Items to Incidents (SOP 10)
    "The assistant must obtain the ID for the incident to link the configuration item to by using discover_incident_tracking.",
    "The assistant must obtain the information for the configuration item to link by using discover_assets.",
    "The assistant must check for existing relationship to prevent duplicates using discover_incident_tracking before creating the incident-CI relationship.",
    "The assistant must create incident-Configuration item relationship using manage_incidents_problems_configuration_items.",
    
    # Conducting Communications (SOP 11)
    "The assistant must obtain the required and optional information to conduct a communication, gathering as many optional fields as available (refer to manage_communications tool documentation for field requirements).",
    "The assistant must acquire the recipient user ID by using discover_parties and validate that the recipient status is active if recipient information was provided.",
    "The assistant must create a communication record using manage_communications.",
    
    # Creating Change Requests (SOP 12)
    "The assistant must acquire the incident information using discover_incident_tracking if this change is incident-related.",
    "The assistant must acquire the problem information using discover_incident_tracking if this change is problem-related.",
    "The assistant must obtain the required and optional change request information (refer to manage_change_control tool documentation for field requirements) before creating a change request.",
    "The assistant must create a new change request record using manage_change_control.",
    "The assistant must determine approval requirements based on change_type and risk_level: if change_type is emergency, approval required from Executive.",
    "The assistant must create an approval request by following SOP 20 if approval is required.",
    
    # Managing Rollback Requests (SOP 13)
    "The assistant must obtain the ID of the implemented change request to be rolled back by using discover_change_control.",
    "The assistant must obtain whether the change caused a new incident and if so, create that incident by following SOP 2 if it is not created or acquire that incident if it exists by using discover_incident_tracking.",
    "The assistant must create the rollback request using manage_change_control.",
    
    # Managing Work Notes - Creating (SOP 14)
    "The assistant must acquire the incident information by using discover_incident_tracking if the note is to document an incident.",
    "The assistant must acquire the problem information by using discover_incident_tracking if the note is to document a problem ticket.",
    "The assistant must obtain the required and optional information related to work note before creating it.",
    "The assistant must create the work note record using manage_work_notes.",
    
    # Managing Work Notes - Updating (SOP 14)
    "The assistant must obtain the required and optional information (refer to manage_work_notes tool documentation for fields that can be updated) before updating a work note.",
    "The assistant must update the work note record using manage_work_notes.",
    
    # Creating Attachment Records (SOP 15)
    "The assistant must obtain the required and optional information to create attachments before creating attachment records.",
    "The assistant must create the attachment record using manage_attachments.",
    
    # Updating Escalation Status (SOP 16)
    "The assistant must obtain the ID of the escalation to update by using discover_coordination.",
    "The assistant must obtain the fields needed to be updated (refer to the manage_escalations tool documentation to understand the fields that can be updated).",
    "The assistant must apply the status change and any optional fields using manage_escalations.",
    "The assistant must add a work note to the related incident documenting the status change by following SOP 14 after updating escalation status.",
    
    # Conducting Root Cause Analysis (SOP 17.A)
    "The assistant must obtain the root cause analysis information needed (refer to manage_improvements tool documentation for field requirements) before conducting root cause analysis.",
    "The assistant must validate that the incident has a status of resolved or closed using discover_incident_tracking if the incident related to the root cause analysis is provided.",
    "The assistant must validate that incident meets RCA eligibility criteria: Incident severity is P1 or P2 if the incident is provided for RCA.",
    "The assistant must validate that the problem ticket has a status of resolved or closed by using discover_incident_tracking if the problem ticket related to the root cause analysis is provided.",
    "The assistant must create the root cause analysis record with all gathered information using manage_improvements.",
    
    # Updating Root Cause Analysis (SOP 17.B)
    "The assistant must retrieve the root cause analysis record to be updated using discover_improvement.",
    "The assistant must obtain the new values for the fields that need to be updated (refer to manage_improvements tool to understand the fields that can be updated).",
    "The assistant must apply all changes to the root cause analysis record using manage_improvements.",
    
    # Creating Post-Incident Review (SOP 17.C)
    "The assistant must obtain the information for the incident to review by using discover_incident_tracking before creating a post-incident review.",
    "The assistant must verify that incident status is 'Closed' before creating a post-incident review.",
    "The assistant must create post-incident review record using manage_improvements.",
    
    # Updating Post-Incident Review (SOP 17.D)
    "The assistant must obtain the post incident review record needed to be updated by using discover_improvement.",
    "The assistant must obtain the information needed to be updated (refer to the manage_improvements tool documentation).",
    "The assistant must apply all changes to the post-incident review record using manage_improvements.",
    
    # Generating Incident Reports (SOP 18)
    "The assistant must validate that incident that a report is created for exists and has status of resolved or closed using discover_incident_tracking.",
    "The assistant must obtain the required and optional information to generate a report (refer to manage_incident_reports tool documentation for field requirements).",
    "The assistant must generate the report using manage_incident_reports.",
    
    # Approving or Denying Requests (SOP 19)
    "The assistant must obtain the request identifying information by using discover_workflows along with the decision.",
    "The assistant must update the approval request using manage_approval_requests.",
    
    # Requesting Approvals (SOP 20)
    "The assistant must obtain the reference_id of the record requiring approval (e.g., incident number, change number, escalation details, bridge number, RCA number) by calling the discover_* tool that retrieves that entity information.",
    "The assistant must obtain the approver information: Name, email, or other identifying information for the person who must approve this request using discover_parties.",
    "The assistant must retrieve the record ID and full record details.",
    "The assistant must validate that the record status allows an approval request based on reference_type: Escalation (status must be pending), Bridge (status must be active), Change (status must be requested or scheduled), Rollback (status must be requested), Incident for closure (status must be resolved), RCA (status must be in_progress or completed).",
    "The assistant must validate that no pending approval exists for the same action type on this record with the same approver by using discover_workflows.",
    "The assistant must create the new approval request by using manage_approval_requests.",
    
    # Retrieving SLA Breach Incidents (SOP 21)
    "The assistant must determine filter criteria: identify if filtering by specific client is needed, determine if time range filtering is required (start_date and/or end_date), identify if filtering by incident status is needed.",
    "The assistant must validate the client exists using discover_parties if client_id is provided.",
    "The assistant must ensure dates are in YYYY-MM-DD format if date range is provided.",
    "The assistant must ensure status is one of: open, in_progress, monitoring, resolved, closed if status is provided.",
    "The assistant must call get_sla_breach_incidents with the determined filter criteria to retrieve incidents that have breached either Response SLA (detection_time to acknowledged_at) or Resolution SLA (detection_time to resolved_at/closed_at).",
]