RULES = [
    # Identity and Authorization
    "The assistant must acquire user information by following SOP 8.1 at the beginning of any operation to identify the user and populate fields that reference the current user of the system.",
    "The assistant must verify user authorization using check_authorization before performing any client management, user management, infrastructure, incident, communication, change management, reporting, or improvement operations.",
    "The assistant must validate that the authenticated user has the appropriate role permissions (Account Manager, System Administrator, Technical Support, Incident Manager, Executive, Client Contact) before executing operations specific to those roles.",
    
    # Client Management Operations (SOP 1.x)
    "The assistant must collect all required client information (client_name, company_type, primary_address, support_coverage, preferred_communication) before creating client records, and verify registration_number uniqueness using discover_parties if provided.",
    "The assistant must validate company_type, preferred_communication, and support_coverage values against allowed options when creating or updating client records.",
    "The assistant must verify no duplicate active SLA agreement exists for a client_id using discover_contracts before creating new SLA agreements.",
    "The assistant must set effective_date to current date if not provided, and set status to 'active' if not provided when creating SLA agreements, validating status is one of: active, inactive, expired.",
    "The assistant must halt and use transfer_to_human when encountering missing required inputs, duplicate registration numbers, invalid field values, or failed record creation/updates in client management operations.",
    
    # User Management Operations (SOP 2.x)
    "The assistant must collect all required user information (first_name, last_name, email, role, timezone) before creating user accounts, and check for existing records with the same email using discover_parties.",
    "The assistant must require client_id when creating users with client_contact role and verify the client exists.",
    "The assistant must retrieve current user records using discover_parties before applying modifications when updating user permissions.",
    "The assistant must validate role and status values against allowed options (incident_manager, technical_support, account_manager, executive, system_administrator, client_contact for roles; active, inactive for status).",
    "The assistant must halt and use transfer_to_human when encountering duplicate emails, invalid role/status values, missing client_id for client_contact role, or failed user record operations.",
    
    # Infrastructure Operations (SOP 3.x)
    "The assistant must collect required component information (ci_name, ci_type, environment) before creating infrastructure components, defaulting operational_status to 'operational' if not provided.",
    "The assistant must verify responsible_owner exists using discover_parties if provided when creating infrastructure components.",
    "The assistant must validate ci_type (server, application, database, network, storage, service), environment (production, staging, development, testing), and operational_status (operational, degraded, down) values.",
    "The assistant must verify both CI and client exist and are operational/active before creating CI client assignments, checking for duplicate assignments.",
    "The assistant must halt and use transfer_to_human when encountering invalid ci_type/environment/operational_status values, responsible owner not found, or failed component/assignment creation.",
    
    # Incident Creation and Management (SOP 4.1, 4.2)
    "The assistant must collect all required incident information (title, description, category, impact, urgency, reported_by) before creating incidents, acquiring reported_by using SOP 8.1.",
    "The assistant must perform severity assessment by gathering complete information about outages, scope of impact, regulatory implications, service degradation, and SLA risks, then calling assess_incident_severity to determine the incident severity.",
    "The assistant must validate category (inquiry/help, software, hardware, network, database), impact (critical, high, medium, low), urgency (critical, high, medium, low), and severity (P1, P2, P3, P4) values.",
    "The assistant must initiate a new incident bridge by following SOP 4.5 if the severity is P1 or P2 after creating an incident.",
    "The assistant must create incident-CI relationships by following SOP 4.13 for each affected configuration item if provided during incident creation.",
    "The assistant must confirm problem ticket exists and is not closed using discover_incident_tracking if problem_id is provided when updating incident status.",
    "The assistant must validate status transitions (open, in_progress, monitoring, resolved, closed) and verify assigned_to user exists and is active if provided.",
    "The assistant must halt and use transfer_to_human when encountering missing required inputs, invalid category/severity/impact/urgency/status values, assigned user not found, CI not found, problem ticket not found/closed, or failed incident operations.",
    
    # Incident Escalations (SOP 4.3)
    "The assistant must validate incident has valid status (open or in_progress) for escalation before creating escalation records.",
    "The assistant must confirm escalating user, target user, and approver (if provided) exist and are active using discover_parties before creating escalations.",
    "The assistant must create escalation records with status 'pending' and current timestamp, validating escalation_reason is valid.",
    "The assistant must halt and use transfer_to_human when encountering invalid incident status, users not found/inactive, invalid escalation_reason, or failed escalation creation.",
    
    # Incident Resolution and Closure (SOP 4.4)
    "The assistant must update incident status to 'resolved' using manage_incidents, then obtain postmortem details (incident_id, report_type, report_title, report_content) before creating postmortem draft report.",
    "The assistant must create postmortem incident draft report using manage_incident_reports after resolving the incident.",
    "The assistant must update incident to 'closed' status after postmortem review is complete.",
    "The assistant must halt and use transfer_to_human when encountering missing approval, incident not found/invalid status, missing postmortem information, invalid report_status, or failed resolution/report operations.",
    
    # Incident Bridge Management (SOP 4.5, 4.6)
    "The assistant must validate incident is in 'open' or 'in_progress' state and has an assigned Incident Manager before initiating incident bridges.",
    "The assistant must obtain Incident Manager approval using manage_approval_requests for P3/P4 incident bridge initiation if user is not authorized, then stop proceeding with the SOP.",
    "The assistant must set bridge type to 'major_incident' for P1 and P2 incidents, extracting the Incident Manager as bridge_host and creating bridge with status 'active'.",
    "The assistant must update incident status to 'in_progress' if its status is 'open' when initiating bridges.",
    "The assistant must validate bridge status is 'active' and bridge_host user is found and active before closing bridges.",
    "The assistant must update bridge status to 'closed' and set end_time to current timestamp when closing bridges.",
    "The assistant must halt and use transfer_to_human when encountering incident not found/invalid status, missing Incident Manager, missing P3/P4 approval, invalid bridge status, or failed bridge operations.",
    
    # Approval Management (SOP 4.7, 4.8)
    "The assistant must collect record identifying information, record_type (escalation, bridge, change, rollback, incident_closure, rca), requested_action, and approver information before creating approval requests.",
    "The assistant must acquire reference_id by following SOP 8.1 and validate record status allows approval request based on reference_type: escalation(pending), bridge(active), change(requested/scheduled), rollback(requested), incident(resolved), rca(in_progress/completed).",
    "The assistant must validate no pending approval exists for the same action type on the record by following SOP 8.1 before creating approval requests.",
    "The assistant must verify user is the designated approver and approval request status is 'pending' before processing approval decisions.",
    "The assistant must halt and use transfer_to_human when encountering user lacks authorization, referenced record not found, approver not found/inactive, invalid record status, duplicate pending approval, or failed approval operations.",
    
    # Problem Ticket Management (SOP 4.9, 4.10, 4.11)
    "The assistant must collect required problem information (title, description, category) and validate optional incident_ids exist using discover_incident_tracking before creating problem tickets.",
    "The assistant must update each linked incident with problem_id, create work notes stating 'Incident(s) linked to Problem Ticket [Problem ID]', and send notifications to Technical Support and Incident Manager.",
    "The assistant must validate problem ticket exists and is not closed before updating, applying status changes and optional fields with current timestamp.",
    "The assistant must send notifications to Incident Manager and Technical Support if problem status changed to resolved or closed.",
    "The assistant must verify incident and problem ticket exist, validate incident is not already linked, and confirm problem ticket is not closed before linking incidents to problems.",
    "The assistant must create work notes for both incident and problem ticket documenting the linkage, and send notification to Incident Manager.",
    "The assistant must halt and use transfer_to_human when encountering user not authorized, duplicate problem found, incident not found, problem closed, failed linkage/update, or notification/work note failures.",
    
    # Configuration Item Management (SOP 4.12, 4.13)
    "The assistant must validate problem ticket exists and is not closed, and CI exists before creating problem-CI relationships, checking for existing relationships to prevent duplicates.",
    "The assistant must check for existing incident-CI relationships to prevent duplicates before creating incident-CI relationships.",
    "The assistant must halt and use transfer_to_human when encountering missing required inputs, problem/incident not found/closed, CI not found, duplicate relationships, or failed relationship creation.",
    
    # Communication Management (SOP 5.1)
    "The assistant must acquire incident_id or problem_ticket_id by following SOP 8.1, validate communication_type (status_update, resolution_notice, escalation_notice, bridge_invitation) and recipient_type (client, internal, executive).",
    "The assistant must acquire recipient user ID by following SOP 8.1 if recipient information was provided, and set sender to current authenticated user's ID.",
    "The assistant must validate delivery_method (email, portal, sms, phone) if provided and ensure incident status is open or in_progress.",
    "The assistant must halt and use transfer_to_human when encountering user lacks authorization, incident not found/invalid status, recipient not found/inactive, invalid communication_type/recipient_type/delivery_method, or failed communication creation.",
    
    # Change Management Operations (SOP 6.1, 6.2)
    "The assistant must collect required change information (title, description, change_type, risk_level) and optional fields (incident_id, problem_ticket_id, implementation_date) before creating change requests.",
    "The assistant must determine approval requirements based on change_type and risk_level: standard+low (no approval), standard+medium/high (Incident Manager), normal (Incident Manager), emergency (Executive).",
    "The assistant must create approval request by following SOP 4.7 if approval is required based on change_type and risk_level determination.",
    "The assistant must validate change request exists and is implemented before creating rollback requests, collecting required information (change_id, title, rollback_reason) and optional incident_id.",
    "The assistant must halt and use transfer_to_human when encountering invalid change_type/risk_level values, incident/problem not found, failed change/rollback/approval request creation, or audit logging failures.",
    
    # Work Notes and Attachments (SOP 6.3, 6.4, 6.5)
    "The assistant must ensure exactly one of incident_id or problem_ticket_id is provided when creating work notes, collecting required information (note_text, note_type).",
    "The assistant must validate user is original author or system administrator before allowing work note updates.",
    "The assistant must validate reference_type (incident, change, rca, report, pir, communication, work_order, problem) and acquire reference_id by following SOP 8.1 before creating attachments.",
    "The assistant must collect required attachment information (file_name, file_url) and optional fields (file_type, file_size_bytes).",
    "The assistant must halt and use transfer_to_human when encountering user not authorized to update work notes, work note not found, invalid reference_type, failed work note/attachment operations, or audit logging failures.",
    
    # Escalation and Communication Status Updates (SOP 6.6, 6.7)
    "The assistant must validate new escalation status is one of (pending, approved, denied, cancelled) and status transition is valid based on current status before updating escalations.",
    "The assistant must add work note to related incident documenting escalation status change using manage_work_notes after updating escalation status.",
    "The assistant must validate new communication delivery_status is one of (pending, sent, delivered, failed) before updating communications.",
    "The assistant must add work note stating 'Delivery failed for communication [communication_id]' to related incident if delivery_status is 'failed'.",
    "The assistant must halt and use transfer_to_human when encountering invalid status values, invalid status transitions, target user not found/inactive, failed updates, or work note creation failures.",
    
    # Root Cause Analysis (SOP 6.8, 6.9)
    "The assistant must validate incident exists with status resolved/closed and meets RCA eligibility criteria (severity P1 or P2) or problem ticket exists with status resolved/closed before conducting RCA.",
    "The assistant must collect RCA information (incident_id or problem_ticket_id, rca_title, assigned_to, due_date) and optional fields (analysis_method, root_cause_summary, status).",
    "The assistant must set reported_by to current authenticated user's ID and validate analysis_method (5_whys, fishbone, timeline, fault_tree, kepner_tregoe) if provided.",
    "The assistant must verify user is authorized to update RCA analysis and validate assigned user and approved_by user exist and are active when updating RCA records.",
    "The assistant must halt and use transfer_to_human when encountering incident/problem not found/invalid status, does not meet RCA criteria, assigned user invalid, invalid analysis_method/status, or failed RCA operations.",
    
    # Post-Incident Review Management (SOP 6.10)
    "The assistant must validate facilitator user exists and is active before updating post-incident review records.",
    "The assistant must validate status is one of (scheduled, completed, cancelled) if provided when updating PIR records.",
    "The assistant must apply all changes to PIR records with current timestamp and user identification.",
    "The assistant must halt and use transfer_to_human when encountering user lacks authorization, PIR not found, facilitator not found/inactive, invalid status, or failed PIR update/audit logging.",
    
    # Reporting Operations (SOP 7.1, 7.2)
    "The assistant must validate incident exists with status resolved/closed before generating incident reports, collecting required information (incident_id, report_title, report_type, report_content, report_status).",
    "The assistant must validate report_type (post_incident_review, client_impact, compliance) and report_status (draft, completed, approved, archived) values.",
    "The assistant must validate incident exists with status closed before creating post-incident reviews, collecting required information (incident_id, scheduled_date, facilitator, review_notes, lessons_learned, action_items, status).",
    "The assistant must validate facilitator user exists and is active before creating PIR records.",
    "The assistant must halt and use transfer_to_human when encountering incident not found/invalid status, required incident data incomplete, invalid report_type/report_status/status values, facilitator not found/inactive, or failed report/PIR creation.",
    
    # Entity Identification Operations (SOP 8.1)
    "The assistant must identify appropriate discovery tool based on entity type: discover_parties (clients, vendors, users), discover_assets (products, configuration_items), discover_contracts (subscriptions, sla_agreements), discover_incident_tracking (incidents, problem_tickets, work_notes, attachments, incident_reports, work_orders), discover_coordination (escalations, bridges, bridge_participants), discover_change_control (change_requests, rollback_requests), discover_workflows (communications, approval_requests), discover_improvement (root_cause_analyses, post_incident_reviews), discover_audit (audit_trails).",
    "The assistant must obtain search criteria from user based on entity type and provide as many criteria as possible to the discovery tool to locate specific records and IDs.",
    "The assistant must retrieve records that match the criteria along with the ID field for each record using the appropriate discovery tool.",
    "The assistant must use SOP 8.1 to acquire entity IDs whenever entity information (name, email, number) is provided but the specific ID is needed for operations, to verify entity existence/status/attributes, or to retrieve full entity records for validation/display/processing.",
    
    # Audit and Logging Requirements
    "The assistant must log all operations using log_audit_records after completing each SOP step that modifies system state, including client creation/updates, user operations, infrastructure changes, incident operations, escalations, problem tickets, communications, change requests, work notes, attachments, RCA operations, PIR operations, and report generation.",
    "The assistant must maintain comprehensive audit trails documenting user actions, timestamps, and operation details for all system modifications.",
    
    # Error Handling and Escalation
    "The assistant must halt operations and use transfer_to_human when encountering any specified error conditions in each SOP, including but not limited to: missing required inputs, invalid field values, unauthorized users, duplicate records, entity not found, invalid status transitions, failed record operations, or audit logging failures.",
    "The assistant must provide clear error messages explaining why operations cannot proceed and what corrective actions are needed.",
    "The assistant must not proceed with operations if authorization checks fail, required entities are not found, or validation criteria are not met.",
    
    # System Integration and Data Validation
    "The assistant must only use information provided by authenticated system tools (manage_*, discover_*, check_authorization, assess_incident_severity, log_audit_records) and never fabricate entity IDs, statuses, or other system data.",
    "The assistant must validate all referenced entities exist and have appropriate status before executing operations that depend on them.",
    "The assistant must perform one tool call at a time and wait for results before making additional calls or responding to the user.",
    "The assistant must maintain data integrity by checking for duplicate records, validating status transitions, and ensuring referential integrity between related entities (incidents-problems, incidents-CIs, escalations-incidents, bridges-incidents, changes-incidents, etc.).",
    
    # Workflow and Process Enforcement
    "The assistant must follow sequential SOP steps in order without skipping required validations or authorizations.",
    "The assistant must create required approval requests when operations require authorization based on change_type, risk_level, severity, or user role.",
    "The assistant must update related entities when creating linkages (updating incidents with problem_id when linking to problems, creating work notes for both entities when linking incidents to problems, etc.).",
    "The assistant must send required notifications using manage_communications when creating problem tickets, updating problem status to resolved/closed, linking incidents to problems, and after updating escalation status.",
    "The assistant must enforce timing requirements by setting current timestamps for creation, setting effective_date to current date if not provided for SLAs, and validating scheduled dates for PIRs.",
    
    # Status and State Management
    "The assistant must validate status values match allowed options for each entity type: incidents (open, in_progress, monitoring, resolved, closed), problem_tickets (open, in_progress, resolved, closed), escalations (pending, approved, denied, cancelled), bridges (active, closed), change_requests (requested, approved, denied, scheduled, implemented, cancelled), rollback_requests (requested, approved, executed, failed), communications (pending, sent, delivered, failed), approval_requests (pending, approved, denied), rca (assigned, in_progress, completed, approved), pir (scheduled, completed, cancelled), reports (draft, completed, approved, archived).",
    "The assistant must enforce valid status transitions and prevent invalid state changes (e.g., cannot escalate closed incidents, cannot link to closed problem tickets, cannot update closed problems, cannot close bridges that aren't active).",
    "The assistant must update status automatically when required by workflow (setting escalation status to 'pending', setting incident to 'in_progress' when opening bridge if currently 'open', setting incident to 'resolved' then 'closed' during resolution process)."
]