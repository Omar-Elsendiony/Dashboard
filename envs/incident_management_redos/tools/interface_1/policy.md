# Incident Management Standard Operating Procedures

---

# **The current time is 2025-10-07 12:00:00 UTC**

# **Introduction**

This document defines the structure and procedures for Incident Management within the ticketing system. It aligns with ITIL best practices and establishes consistent workflows for incident detection, classification, escalation, resolution, and post-incident analysis.

**At the beginning, acquire the user information by following SOP 8.1. As a result, this ID can be used to identify the user and populate the fields that reference the current user of the system.**

# **Standard Operating Procedures (SOPs)**

## **1. Client Management Operations**

### 1.1 Creating Client Records

**When to use:** When registering new enterprise, mid-market, small business, or startup clients who will require access to incident management services in the ticketing system.

**Who can perform:**

* Account Managers  
* System Administrators  
* Technical Support

Steps:

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following client information:  
   * client_name: Legal or business name of the client  
   * company_type  
   * primary_address:  primary_address (headquarters or billing address)  
   * support_coverage  
   * preferred_communication  
   * registration_number (optional)  
   * status (optional)  
3. If registration_number is provided, verify it is unique across all client records using discover_parties.  
4. Create the client record with all required and optional fields using manage_clients.  
5. Log the client creation action using log_audit_records.

Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:

* Missing or invalid required inputs  
* Duplicate registration_number detected (if provided)  
* Invalid company_type value  
* Invalid preferred_communication value  
* Invalid support_coverage value  
* Client record creation failed  
    
  ---

### 1.2 Updating Client Information

**When to use:** When client details change or status modifications are required.

**Who can perform:**

* Account Managers assigned to the client  
* System Administrators

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following information:  
   * client_id: The unique identifier of the client to update. Acquire by following SOP 8.1  
   * client_name  (optional): Legal or business name of the client  
   * company_type (optional)  
   * primary_address (optional):  primary_address (headquarters or billing address)  
   * support_coverage (optional)  
   * preferred_communication (optional)  
   * registration_number (optional)  
   * status (optional)  
       
3. Retrieve the current client record using client_id using discover_parties.  
4. Apply all changes to the client record using manage_clients.  
5. Log the client update action using log_audit_records.

**Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* Missing required client_id input  
* Client record not found  
* User lacks authorization to modify client  
* Invalid company_type value  
* Invalid preferred_communication value  
* Invalid support_coverage value  
* Invalid status value  
* Duplicate registration_number detected  
* Client record update failed

  ---

### 1.3 SLA Agreement Creation

**When to use:** When defining specific SLA metrics for client subscriptions.

**Who can perform:**

* Account Managers  
* Executives

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from user:  
   * client_id: The unique identifier of the client. Acquire by following SOP 8.1  
   * tier: Service tier level  
   * support_coverage: Support coverage level  
   * Effective_date (optional): SLA effective start date  
   * expiration_date (optional): SLA expiration date  
   * status: SLA status (optional)  
3. Verify that no duplicate active SLA agreement for this client_id exists using discover_contracts.  
4. If effective_date is not provided, set to current date.  
5. If status is not provided, set status to 'active'. Otherwise, validate it is one of: active, inactive, expired.  
6. Create SLA agreement using manage_contracts.  
7. Log the SLA agreement creation action using log_audit_records.

**Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* Missing or invalid required inputs  
* Client not found or inactive  
* User lacks authority to create SLA agreements  
* Invalid tier value  
* Invalid support_coverage value  
* Invalid status value  
* Duplicate active SLA agreement exists for client  
* Invalid effective_date or expiration_date  
* SLA agreement creation failed

## **2. User Management Operations**

### 2.1 Creating User Accounts

**When to use:** When adding personnel to the incident management system.

**Who can perform:**

* System Administrators  
* Incident Managers

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following user information:  
   * first_name: User's first name  
   * last_name: User's last name  
   * email: User's email address  
   * role: Role of the user to be created  
   * timezone: User's timezone  
   * Client_id  (optional): Associated client for client_contact role  
   * Status  (optional) : User status  
3. Check for existing records with same email address using discover_parties.  
4. Create user record with all required and optional fields using manage_users.  
5. Log the user creation action using log_audit_records.

**Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* Missing or invalid required inputs  
* Duplicate email detected  
* Invalid role value  
* Invalid status value  
* Client_id required but not provided for client_contact role  
* Client not found  
* User record creation failed

### 2.2 Update User Permissions

**When to use:** When modifying user access levels or role assignments.

**Who can perform:**

* System Administrators  
* Incident Managers

**Steps:**

1. Verify that the approval to conduct the action is present - System administrators, Incident managers only using check_authorization.  
2. Obtain the following information:  
   * user_id: The unique identifier of the user to update. Acquire by following SOP 8.1  
   * first_name (optional): User's first name  
   * last_name  (optional): User's last name  
   * email (optional): User's email address  
   * role  (optional): User's role  
   * timezone  (optional): User's timezone  
   * client_id  (optional): Associated client for client_contact role  
   * Status (optional): User status  
3. Retrieve current user record using discover_parties.  
4. Apply the modifications using manage_users.  
5. Create an audit entry for user permission update using log_audit_records.

**Halt, and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**

* Missing required user_id input  
* User record not found  
* User lacks authorization to modify user permissions  
* Invalid role value  
* Invalid status value  
* Duplicate email detected  
* Client not found when required  
* User record update failed

## **3. Product and Infrastructure Operations**

### 3.1 Creating Infrastructure Components

**When to use:** When documenting system components that support products and services.

**Who can perform:**

* Technical Support Specialists  
* System Administrators

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following component information:  
   * ci_name  
   * ci_type (server, application, database, network, storage, service)  
   * environment (production, staging, development, testing)  
   * operational_status (default: 'operational') (optional)  
   * responsible_owner (optional)  
3. If responsible_owner provided, verify user exists using discover_parties.  
4. Create component record using manage_assets.  
5. Record this action in the audit log for traceability using log_audit_records.

**Halt, and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**

* Missing or invalid inputs  
* Invalid ci_type value  
* Invalid environment value  
* Invalid operational_status value  
* Responsible owner user not found or inactive  
* Component record creation failed

### 3.2 Managing CI Client Assignments

**When to use:** When assigning configuration items to clients for access control and incident tracking.

**Who can perform:**

* System Administrators  
* Technical Support Specialists

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following information:  
   * Ci_id: Configuration item ID. Acquire by following SOP 8.1  
   * Client_id: Acquire by following SOP 8.1  
3. Create CI client assignment using manage_assets.  
4. Log the assignment action using log_audit_records.

**Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* Missing or invalid required inputs  
* CI not found or not operational  
* Client not found or inactive  
* Duplicate assignment exists  
* Assignment creation failed

## **4. Incident Operations**

### 4.1 Creating Incidents

**When to use:** When service impacts are detected that require a formal incident management response. This includes client-reported outages, automated alerts from monitoring systems, or executive escalations that disrupt normal operations.

**Who can perform:**

* Incident Managers  
* Technical Support (if delegated by Incident Manager)  
* Executives  
* Systems Administrators

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following incident information:  
   * title  
   * description  
   * category (inquiry/help\\, software, hardware, Network, Database)  
   * impact (critical, high, medium, low)  
   * urgency (critical, high, medium, low)  
   * reported_by: User of the system that reported the incident. Acquire by following SOP 8.1  
   * assigned_to (optional)  
   * detection_time (optional)  
   * problem_id (optional)  
   * affected configuration item(s) (optional)

3. Perform a Severity Assessment by following those steps:  
   * Gather severity assessment information:  
     1. Whether there is a complete outage of business-critical services with no workaround  
     2. The scope of impact (enterprise-wide, multiple customers, number of affected parties)  
     3. Any regulatory, safety, or financial implications  
     4. Whether high-priority customers or recurrent incidents are involved  
     5. The level of service degradation (major or moderate) and availability of workarounds  
     6. Whether multiple departments, sites, or critical business functions are affected  
     7. Any risk of breaching high-priority SLAs  
     8. Whether the impact is localized to a single department or function  
   * Call `assess_incident_severity` with all the information gathered in (1).  
   * Use the returned severity as the incident severity.  
4. Create a new incident using manage_incidents.  
5. If the severity is P1 or P2, then a new incident bridge is initiated by following SOP 4.5  
6. If affected configuration item(s) information were provided, then for each configuration item:  
   * Create incident-CI relationship by following SOP 4.13  
7. Log the incident creation action using log_audit_records.  
   

**Halt, and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**

* Missing or invalid inputs  
* Assigned user not found or inactive, if provided  
* Configuration item not found or inactive  
* Problem ticket not found or closed, if provided  
* Invalid category value  
* Invalid severity, impact or urgency value  
* Invalid status value  
* Incident record creation failed

  ---

### 4.2 Updating Incident Status

**When to use:** When incident status changes are required during the incident lifecycle.

**Who can perform:**

* Incident Managers  
* Technical Support assigned to the incident  
* System Administrators  
* Executive

**Steps:**

1. Verify the user has authorization to conduct this action using `check_authorization`.  
2. Obtain the following information:

   * incident_id  
   * status (open, in_progress, monitoring, resolved, closed)  
   * assigned_to (optional)  
   * problem_id (optional)  
3. If `problem_id` was provided in Step 2, confirm that the problem ticket exists and is not closed using `discover_incident_tracking`.  
4. Apply the status change and any optional fields using `manage_incidents`.  
5. Log the incident status update action using `log_audit_records`.

**Halt, and use `transfer_to_human` if you receive the following problems; otherwise complete the SOP:**

* Missing required incident_id or status input  
* Incident record not found  
* Assigned user not found or inactive, if provided  
* Problem ticket not found or closed, if provided  
* Invalid status value  
* Invalid status transition  
* Missing timestamp for relevant status change  
* User not authorized to update this incident  
* Incident record update failed  
  ---

### 4.3 Creating Incident Escalations

**When to use:** When escalating incidents due to severity, SLA breach risk, or resource requirements.

**Who can perform:**

* Incident Managers  
* Technical Support  
* Account Managers  
* Systems Administrator  
* Executive

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following escalation information:  
   * incident_id  
   * escalated_to  
   * escalation_reason  
   * approver (optional)  
3. Validate incident has valid status (open or in_progress) for escalation.  
4. Confirm the escalating user (current user) exists and is active using discover_parties.  
5. Confirm the target user exists and is active using discover_parties.  
6. If approver was provided, confirm the approver user exists and is active.  
7. Create the escalation record with status pending and current timestamp using manage_escalations.  
8. Log the escalation creation action using log_audit_records.

**Halt, and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**

* Missing or invalid required inputs  
* Incident not found or invalid status  
* Escalating user not found or inactive  
* Target user not found or inactive  
* Approver user not found or inactive, if provided  
* Invalid escalation_reason  
* Escalation creation failed

  ---

### 4.4 Resolving an Incident

**When to use:** Use this procedure once the incident has been mitigated or fully resolved, to formally close it and ensure that all required information is collected for the postmortem (root cause and lessons learned) report.

**Who can perform:**

* Incident Managers  
* Technical Support

**Steps:**

1. Verify that the approval to conduct the resolving an Incident action is present (incident_manager or technical_support or executive approval required) using `check_authorization`.  
2. Obtain the incident_id  
3. Update the incident status to `resolved` using `manage_incidents`.  
4. Obtain the following details for the postmortem report:  
   * Incident ID  
   * `report_type`  
   * `report_title`  
   * `report_content`  
5. Create a postmortem incident draft report using `manage_incident_reports`.  
6. Update the incident to `closed` status after postmortem review is complete using `manage_incidents`.  
7. Log the incident resolution action using `log_audit_records`.

**Halt, and use `transfer_to_human` if you receive the following errors; otherwise complete the SOP:**

* Approval missing to resolve incident  
* Incident not found or invalid status  
* Missing required postmortem information  
* Invalid report_status value  
* Report generation failed  
* Incident resolution update failed  
* Audit trail logging failure  
  ---

### 4.5 Initiating an Incident Bridge

**When to use:** When an active incident requires immediate, multi-team collaboration to coordinate diagnostic, communication, and recovery actions.

A bridge must be initiated for all P1 (Critical) and P2 (High) incidents.

For P3 or P4 incidents, bridge initiation requires prior Incident Manager approval before proceeding.

**Who can perform:**

* Incident Managers  
* Technical Support Specialists  
* Executives

**Steps:**

1. Obtain the following required information:  
   * **incident_id**: Incident requiring bridge collaboration. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
2. Validate that incident is in an `open` or `in_progress` state and has an assigned Incident Manager.  
3. Verify the user has authorization to conduct this action using `check_authorization`.  
4. If the user is not authorized, then check If severity is P3 or P4. If that is the case, then obtain approval from the Incident Manager using `manage_approval_requests` and stop proceeding with the SOP.  
5. Extract the Incident Manager assigned to the incident from Step 1.  
6. Create the bridge record with the following values using `manage_coordinations`

   * **Bridge Type**: `major_incident`, `coordination`, or `technical`  
   * **Bridge Host**: Incident Manager assigned to the incident  
   * **Start Time**: System-generated current timestamp  
   * **Status**: `active`  
7. For P1 and P2 incidents, the bridge type is going to be ‘major_incident’  
8. Update the incident status to `in_progress` if its status is `open` using `manage_incidents`.  
9. Log the bridge initiation action using `log_audit_records`.

**Halt, and use `transfer_to_human` if you receive the following problems; otherwise complete the SOP:**

* Incident not found or invalid status  
* Incident missing assigned Incident Manager  
* Approval missing for P3/P4 incident bridge initiation  
* Impacted client or configuration item fields not populated  
* Bridge host user not found or inactive  
* Bridge record creation failed  
* Incident update failed  
* Invalid bridge status value  
* Audit trail logging failure  
  ---

### 4.6 Closing an Incident Bridge

**When to use:** When the incident has reached a confirmed resolution or stable workaround and real-time collaboration is no longer required.

**Who can perform:**

* Incident Managers  
* Technical Support Specialists (if delegated by Incident Manager)

**Steps:**

1. Verify the user has authorization to conduct this action using `check_authorization`.

2. Obtain the following required information:

   * **incident_id**: Incident associated with the bridge to close. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **bridge_id**: Bridge to close. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
3. Validate the bridge status is `active`.  
4. Validate the bridge host user is found and active using `discover_parties`.  
5. Update the bridge status to `closed` using `manage_coordinations`.

6. Update the bridge end time to current timestamp using `manage_coordinations`.

7. Log the bridge closure action using `log_audit_records`.

**Halt, and use `transfer_to_human` if you receive the following problems; otherwise complete the SOP:**

* User not authorized to close bridges  
* Incident not found  
* Bridge record not found or not linked to incident  
* Bridge status is not `active`  
* Bridge host user not found or inactive  
* Incident status is not `resolved` or `monitoring`  
* Incident missing required resolution documentation or impact summary  
* Bridge status update failed  
* Bridge end time update failed  
* Audit trail logging failure  
  ---

### 4.7 Requesting Approvals

**When to use:** When an action requires documented authorization before execution. This may include bridge initiation, escalation, change implementation, or any process step defined by policy as requiring approval.

**Who can perform:**

* Technical Support Specialist  
* System Administrator  
* Incident Managers

**Steps:**

1. Verify the user has authorization to conduct this action using `check_authorization`.  
2. Obtain the following **required** information from the user:  
   1. **Record identifying information**: Details to locate the record requiring approval (e.g., incident number, change number, escalation details, bridge number, RCA number)  
   2. **Record type**: Type of record (one of: `escalation`, `bridge`, `change`, `rollback`, `incident_closure`, `rca`)  
   3. **Requested action**: Description of the action requiring approval (one of: create_escalation,initiate_bridge,create_change_request,create_rollback_request,conduct_rca,close_incident)  
   4. **Approver information**: Name, email, or other identifying information for the person who must approve this request  
3. Acquire the `reference_id` by following SOP 8.1 (Acquiring Entity Records and IDs) and provide the record identifying information from Step 2 as search criteria  
4. Retrieve the record ID and full record details  
5. Validate that the record status allows an approval request based on `reference_type` from the record retrieved in Step 3:  
   1. **Escalation**: status must be `pending`  
   2. **Bridge**: status must be `active`  
   3. **Change**: status must be `requested` or `scheduled`  
   4. **Rollback**: status must be `requested`  
   5. **Incident (for closure)**: status must be `resolved`  
   6. **RCA**: status must be `in_progress` or `completed`  
6. Validate that no pending approval exists for the same action type on this record by following SOP 8.1  
7. Create a new approval request record using `manage_approval_requests`  
8. Log the approval request creation using `log_audit_records`

**Halt and use `transfer_to_human` if you receive the following errors; otherwise complete the SOP:**

* User lacks authorization  
* Referenced record not found  
* Approver user not found or inactive  
* Record status does not allow approval request  
* Duplicate pending approval exists for same action  
* Cannot determine incident association for communication  
* Approval request creation failed  
* Communication notification failed  
* Audit trail logging failure

### 4.8 Approving or Denying Requests

**When to use:** When an approval request has been submitted and a response is required to authorize or deny the requested action.

**Who can perform:**

* Incident Managers  
* Executives

**Steps:**

1. Verify the user has authorization to conduct this action using `check_authorization`.  
2. Obtain the following **required** information from the user:  
   * **Approval request identifying information**: Approval request number, reference type, reference ID, or other details to locate the approval request  
   * **Decision**: Approve or deny  
3. Acquire the `approval_id` and full approval request details by following SOP 8.1.  
4. Update the approval request using `manage_approval_requests`  
5. Log the approval decision action using `log_audit_records`.

**Halt and use `transfer_to_human` if you receive the following errors; otherwise complete the SOP:**

* User lacks authorization  
* Approval request not found  
* Approval request status is not pending  
* Current user is not the designated approver  
* Linked record not found  
* Approval request update failed  
* Audit trail logging failure

### 4.9 Creating Problem Tickets

**When to use:** When a recurring, underlying, or systemic issue is identified that may be the root cause of one or more related incidents.

**Who can perform:**

* Technical Support Specialist  
* System Administrator  
* Incident Manager

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from the user:  
   * title: Problem title (concise, descriptive summary of the underlying issue)  
   * description: Detailed description (summary of observed behavior, patterns, or error signatures)  
   * category: Problem category  
3. Check for the following optional fields. Include if provided:  
   * incident_ids: List of incident IDs related to this problem  
   * assigned_to: User to assign the problem to  
4. If incident IDs were provided in Step 3, validate each incident exists using discover_incident_tracking.  
5. Create the Problem Ticket record using manage_problem_tickets.  
6. If incident IDs were provided in Step 3, for each incident ID:  
   * Use manage_incidents to update each incident  
   * Set problem_id to the problem ticket ID from Step 8  
7. Record "Incident(s) linked to Problem Ticket \[Problem ID\]" in Work Notes using manage_work_notes.  
8. Send notifications to Technical Support and the Incident Manager confirming that the Problem Ticket was created using manage_communications with the content “New problem ticket created with ID \[Problem ID\]”.  
9. Log the problem ticket creation action using log_audit_records.

**Halt, and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**

* User not authorized to create problem record  
* Existing problem record found (duplicate)  
* Related incident not found, if provided  
* Problem record creation failed  
* Incident linkage update failed  
* Problem ticket creation notifications failed  
* Audit trail logging failure  
* Work note creation failed (due to invalid problem_ticket_id or both incident_id and problem_ticket_id being internally passed)  
* Communication notification failed (due to invalid problem_ticket_id or both incident_id and problem_ticket_id being internally passed)

---

### 4.10 Updating Problem Tickets

**When to use:** When new information, investigation results, or resolution progress must be added to an existing Problem Ticket.

**Who can perform:**

* Technical Support Specialist  
* System Administrator  
* Incident Manager

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from the user:  
   * problem_id: Problem ticket to update. Acquire by following SOP 8.1  
3. Check for the following optional fields to update. Include in update if provided:  
   * status: New status for the problem ticket  
   * title: Updated problem title  
   * description: Updated problem description  
   * category: Updated problem category  
   * assigned_to: Updated assigned user  
4. Apply the status change and any optional fields with current timestamp using manage_problem_tickets.  
5. Record "Problem ticket updated with new investigation details" in Work Notes using manage_work_notes.  
6. If status changed to resolved or closed in Step 4, send notifications to the Incident Manager and Technical Support using manage_communications.  
7. Log the problem ticket update action using log_audit_records.

**Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* User not authorized to update problem record  
* Problem record not found  
* Problem record unavailable for update (closed status)  
* Add: Work note creation failed (due to invalid problem_ticket_id or both incident_id and problem_ticket_id being internally passed)  
* Add: Problem ticket update notifications failed (due to invalid problem_ticket_id or both incident_id and problem_ticket_id being internally passed)  
* Invalid status value  
* Invalid status transition  
* Cannot close problem with open incidents remaining  
* Problem record update failed  
* Problem ticket update notifications failed  
* Audit trail logging failure

---

### 4.11 Linking Incidents to Problem Tickets

**When to use:** When an existing incident is identified as related to an existing Problem Ticket.

**Who can perform:**

* Technical Support Specialist  
* System Administrator  
* Incident Manager

**Steps:**

1. Verify the user has authorization to conduct this action using `check_authorization`.  
2. Obtain the following required information from the user:  
   * **incident_id**: Incident to link to the problem ticket. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **problem_id**: Problem ticket to link the incident to. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
3. Update the incident record using `manage_incidents`:  
   * Set `problem_id` to the problem ticket ID from Step 2  
4. Record "Incident linked to Problem Ticket \[Problem Number\]" in Work Notes for the incident using `manage_work_notes`.  
5. Record "Incident \[Incident Number\] linked to this problem ticket" in Work Notes for the problem ticket using `manage_work_notes`.  
6. Send notification to the Incident Manager using `manage_communications`.

7. Log the incident linkage action using `log_audit_records`.

**Halt, and use `transfer_to_human` if you receive the following problems; otherwise complete the SOP:**

* User not authorized to link incident to problem  
* Incident not found  
* Problem ticket not found  
* Incident is already linked to this problem ticket  
* Incident already linked to different problem ticket  
* Cannot link incidents to closed problem tickets  
* Incident update failed  
* Work note creation failed  
* Notification delivery failure  
* Audit trail logging failure

### 4.12 Managing Problem Configuration Items

**When to use:** When linking configuration items to problem tickets to track affected infrastructure.

**Who can perform:**

* Technical Support Specialist  
* System Administrator  
* Incident Manager

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information:  
   * problem_id: Problem ticket to link CI to. Acquire by following SOP 8.1  
   * ci_id: Configuration item to link. Acquire by following SOP 8.1  
3. Validate problem ticket exists and is not closed using discover_incident_tracking.  
4. Validate CI exists using discover_assets.  
5. Check for existing relationship to prevent duplicates using discover_incident_tracking.  
6. Create problem-CI relationship using manage_incidents_problems_configuration_items.  
7. Log the relationship creation using log_audit_records.

**Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* Missing or invalid required inputs  
* Problem ticket not found or closed  
* CI not found  
* Duplicate relationship exists  
* Relationship creation failed

### 4.13 Managing Incident Configuration Items

**When to use:** When linking configuration items to incidents to track affected infrastructure.

**Who can perform:**

* Incident Managers  
* Technical Support  
* System Administrators

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information:  
   * incident_id: Incident to link CI to. Acquire by following SOP 8.1  
   * ci_id: Configuration item to link. Acquire by following SOP 8.1  
3. Check for existing relationship to prevent duplicates using discover_incident_tracking.  
4. Create incident-CI relationship using manage_incidents_problems_configuration_items.  
5. Log the relationship creation using log_audit_records.

**Halt, and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* Missing or invalid required inputs  
* Incident not found or closed  
* CI not found  
* Duplicate relationship exists  
* Relationship creation failed

## **5. Communication Management**

### 5.1 Conducting Communications

**When to use:** When you want to notify a certain individual through communication channels

**Who can perform:**

* Incident Managers  
* Technical Support

**Steps:**

1. Verify the user has authorization to conduct this action using `check_authorization`.  
2. Obtain the following **required** information from the user:  
   * **Incident identifying information**: Incident number or other details to locate the incident by following SOP 8.1  
   * **Problem identifying information**: Incident number or other details to locate the incident by following SOP 8.1  
   * **Communication type**: Type of communication (status_update, resolution_notice, escalation_notice, bridge_invitation, other)  
   * **Recipient type**: Type of recipient (client, internal, executive)  
   * **Recipient information (optional)**: Specific user details if targeting an individual   
   * **Message content**: Communication content  
   * **Delivery method (optional)**: Method of delivery (email, portal, sms, phone)   
3. If recipient information was provided in Step 2, acquire the `recipient` user ID by following SOP 8.1 (Acquiring Entity Records and IDs)  
4. Set sender with the ID of the user conducting the action obtained by following SOP 8.1  
5. Create a communication record using `manage_communications`.  
6. Log the communication creation action using `log_audit_records`.

**Halt and use `transfer_to_human` if you receive the following errors; otherwise complete the SOP:**

* User lacks authorization  
* Incident not found  
* Incident status is not open or in_progress  
* Recipient user not found or inactive (if specific recipient provided)  
* Invalid communication_type value  
* Invalid recipient_type value  
* Invalid delivery_method value  
* Communication record creation failed  
* Audit trail logging failure

## **6. Change Management Operations**

### 6.1 Creating Change Requests

**When to use:** When system modifications, configuration adjustments, or corrective actions are required to restore service, implement improvements, or prevent incident recurrence.

**Who can perform:**

* Technical Support Specialist  
* System Administrators  
* Executive  
* Incident Manager  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from the user:  
   * title: Concise summary of the modification or task  
   * description: Purpose and expected outcome of the change  
   * change_type: Type of change (standard, normal, emergency)  
   * risk_level: Risk assessment (low, medium, high, critical)  
3. Check for the following optional fields. Include if provided:  
   * incident_id: If this change is incident-related, acquire by following SOP 8.1  
   * problem_ticket_id: If this change is problem-related, acquire by following SOP 8.1  
   * implementation_date: Planned implementation date  
4. Create a new change request record using manage_change_control.  
5. Determine approval requirements based on change_type and risk_level from Step 2:  
   * If change_type is standard and risk_level is low, no approval required; skip to Step 11.  
   * If change_type is standard and risk_level is medium or high, approval required from Incident Manager.  
   * If change_type is normal, approval required from Incident Manager.  
   * If change_type is emergency, approval required from Executive.  
6. If approval is required from Step 9, create an approval request by following SOP 4.7.  
7. Log the change request creation action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**  
* User lacks authorization  
* Invalid change_type value  
* Invalid risk_level value  
* Incident not found (if incident information provided)  
* Problem ticket not found (if problem ticket information provided)  
* Change request creation failed  
* Approval request creation failed (if required)  
* Audit trail logging failure


  ---

  ### 6.2 Managing Rollback Requests

  **When to use:** When a change request has been implemented but causes a new incident, performance degradation, or stability issue, and the system must be returned to its pre-change state.  
  **Who can perform:**  
* Technical Support Specialist  
* Systems Administrator  
* Incident Manager  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from the user:  
   * **change_id**: Implemented change request to be rolled back. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **title**: Title for the rollback request  
   * **rollback_reason**: Reason for requesting the rollback  
3. Check for the following optional fields. Include if provided:  
   * **incident_id**: If a new incident was caused by the change, acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
4. Create the rollback request using manage_change_control.  
5. Log the rollback request creation action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**  
* User lacks authorization  
* Change request not found  
* Incident not found (if incident information provided)  
* Rollback request creation failed  
* Audit trail logging failure

  ---

  ### 6.3 Creating Work Notes

  **When to use:** When documenting activities, updates, or observations related to incidents.

  **Who can perform:**

* Incident Managers  
* Technical Support  
* System Administrators  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from the user:  
   * **incident_id**: Incident to document. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs) \[If the note is related to an incident\]  
   * **problem_ticket_id**: Problem to document. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs) \[If the note is related to a problem\]  
   * **note text**: The work note content  
   * **note_type**: Type of work note (progress_update, troubleshooting, resolution)

3. Exactly one of incident_id or problem_ticket_id has to be provided.  
4. Create the work note record using manage_work_notes.  
5. Log the work note creation action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**  
* User lacks authorization  
* Incident not found  
* Work note creation failed  
* Audit trail logging failure

  ---

  ### 6.4 Updating Work Notes

  **When to use:** When modifying existing work note content.

  **Who can perform:**

* Incident Managers  
* Technical Support  
* System Administrators (original author or authorized users only)  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from the user:  
   * **note_id**: Work note to update. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **Updated note text**: The updated work note content  
   * **note_type (optional):** Type of work note (progress_update, troubleshooting, resolution)

     

3. Update the work note record using manage_work_notes.  
4. Log the work note update action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**  
* User lacks authorization  
* Work note not found  
* User not authorized to update this work note (not original author or system administrator)  
* Work note update failed  
* Audit trail logging failure

  ---

  ### 6.5 Creating Attachment Records

  **When to use:** When uploading files or documents related to incidents, changes, RCAs, reports, PIRs, communications, work orders, or problems.

  **Who can perform:**

* Incident Managers  
* Technical Support  
* System Administrators  
* Client Contacts (for their own incidents)  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information from the user:  
   * **Reference type**: Type of record the attachment relates to (incident, change, rca, report, pir, communication, work_order, problem)  
   * **reference_id**: Record to attach file to. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs) using entity type based on reference type  
   * **File name**: Name of the file being attached  
   * **File URL**: URL where the file is stored  
   * **File type (optional)**: MIME type or file extension  
   * **File size bytes (optional)**: Size of the file in bytes  
3. Validate reference_type from Step 2 is one of: incident, change, rca, report, pir, communication, work_order, problem.  
4. Create the attachment record using manage_attachments.  
5. Log the attachment creation action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**  
* User lacks authorization  
* Related record not found  
* Invalid reference_type value  
* Attachment creation failed  
* Audit trail logging failure

  ---

  ### 6.6 Updating Escalation Status

  **When to use:** When escalation status changes are required during the escalation lifecycle.

  **Who can perform:**

* Incident Managers  
* Executives  
* Technical Support (if assigned to the escalation)  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information:  
   * **escalation_id**: Escalation to update. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **status**: New status for the escalation  
3. Check for the following optional fields to update. Include in update if provided:  
   * **escalated_to**: acquire user by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **responded_at**: Timestamp when escalation was responded to  
4. Validate new status is one of: pending, approved, denied, cancelled.  
5. Validate status transition is valid based on current status and escalation workflow.  
6. Apply the status change and any optional fields using manage_escalations.  
7. Add a work note to the related incident documenting the status change using manage_work_notes.  
8. Log the escalation status update action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**  
* User lacks authorization  
* Escalation record not found  
* Invalid status value  
* Invalid status transition  
* Target user not found or inactive (if reassigning)  
* Escalation record update failed  
* Work note creation failed  
* Audit trail logging failure

  ---

  ### 6.7 Updating Communication Status

  **When to use:** When communication delivery status changes or updates are required.

  **Who can perform:**

* Incident Managers  
* Technical Support  
* System Administrators  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information:  
   * **communication_id**: Communication to update. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **delivery_status**: New delivery status  
3. Check for the following optional fields to update. Include in update if provided:  
   * **sent_at**: Timestamp when communication was sent  
4. Validate new delivery_status is one of: pending, sent, delivered, failed.  
5. Apply the status change and any optional fields using manage_communications.  
6. If delivery_status is failed, add a work note to the related incident documenting the issue stating: “Delivery failed for communication \[**communication_id**\]” using manage_work_notes.  
7. Log the communication status update action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**  
* User lacks authorization  
* Communication record not found  
* Invalid delivery_status value  
* Invalid status transition  
* Communication record update failed  
* Work note creation failed (if delivery failed)  
* Audit trail logging failure

  ---

  ### 6.8 Conduct Root Cause Analysis

  **When to use:** After a P1 or P2 incident has been resolved, to create a formal record for investigating the underlying cause and preventing recurrence.

  **Who can perform:**

* Incident Manager  
* Technical Support Specialist (with RCA permissions)  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following root cause analysis information:  
   * incident_id: Acquire by following SOP 8.1 (Acquiring Entity Records and IDs) \[If the root cause analysis to be conducted is related to an incident\]  
   * problem_ticket_id: Acquire by following SOP 8.1 (Acquiring Entity Records and IDs) \[If the root cause analysis to be conducted is related to a problem\]  
   * rca_title  
   * assigned_to  
   * due_date  
   * analysis_method (5_whys, fishbone, timeline, fault_tree, kepner_tregoe) (optional)  
   * root_cause_summary (optional)  
   * status (assigned, in_progress, completed, approved) (optional)  
3. Validate that incident exists and has status of resolved or closed using discover_incident_tracking in case it is provided.  
4. Validate that problem ticket exists and has status of resolved or closed using discover_incident_tracking in case it is provided.  
5. Validate that incident meets RCA eligibility criteria:  
   * Incident severity is P1 or P2  
6. Set reported_by to the current authenticated user's ID.  
7. Create the root cause analysis record using manage_improvements.  
8. Log the RCA initiation action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**  
* User lacks authorization  
* Incident not found or invalid status  
* Incident does not meet RCA eligibility criteria  
* Assigned user not found or has invalid role  
* Invalid analysis_method value  
* RCA creation failed  
* Audit trail logging failure


  ---

  ### 6.9 Updating Root Cause Analysis Records

  **When to use:** When updating root cause analysis findings or status during the analysis process.  
  **Who can perform:**  
* Incident Managers  
* Technical Support  
* System Administrators (original analyst or authorized users)  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the rca record to modify by following SOP 8.1  
3. Apply all changes to the root cause analysis record using manage_improvements.  
4. Log the root cause analysis update action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**  
* User lacks authorization  
* Root cause analysis record not found  
* User not authorized to update this analysis  
* Assigned user not found or inactive  
* Approved by user not found or inactive  
* Invalid analysis_method value  
* Invalid status value  
* Root cause analysis update failed  
* Audit trail logging failure


  ---

  ### 6.10 Updating Post-Incident Review Records

  **When to use:** When updating post-incident review findings, status, or action items during the review process.  
  **Who can perform:**  
* Incident Managers  
* Executives  
  **Steps:**  
1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following information:  
   * review_id  
   * scheduled_date (optional)  
   * facilitator (optional)  
   * status (scheduled, completed, cancelled) (optional)  
   * review_notes (optional)  
   * lessons_learned (optional)  
   * action_items (optional)  
3. Apply all changes to the post-incident review record with current timestamp and user identification using manage_improvements.  
4. Log the post-incident review update action using log_audit_records.  
   **Halt and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**  
* User lacks authorization  
* Post-incident review record not found  
* Facilitator user not found or inactive  
* Invalid status value  
* Post-incident review update failed  
* Audit trail logging failure

---

## **7. Reporting Operations**

### 7.1 Generating Incident Reports

**When to use:** When a formal summary document is required for a closed incident, for purposes such as client communication, compliance audits, or internal post-incident review.

**Who can perform:**

* Incident Manager  
* Executive

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information:  
   * **incident_id**: Incident for which to generate a report. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **report_title**: Title of the incident report  
   * **report_type**: Type of report (post_incident_review, client_impact, compliance)  
   * **report_content**: Content of the report  
   * **report_status**: Status of report (draft, completed, approved, archived)  
3. Validate that incident exists and has status of resolved or closed using discover_incident_tracking.  
4. Generate the report using manage_incident_reports.  
5. Log the report generation action using log_audit_records.

**Halt and use transfer_to_human if you receive the following errors; otherwise complete the SOP:**

* User lacks authorization  
* Missing or invalid required inputs  
* Incident not found or invalid status  
* Required incident data fields incomplete  
* Invalid report_type value  
* Invalid report_status value (if provided)  
* Report generation failed  
* Audit trail logging failure

---

### 7.2 Creating Post-Incident Reviews

**When to use:** When formal review is required to analyze response effectiveness and identify improvements.

**Who can perform:**

* Incident Managers  
* Executives

**Steps:**

1. Verify the user has authorization to conduct this action using check_authorization.  
2. Obtain the following required information:  
   * **incident_id**: Incident to review. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **scheduled_date**: Date for the post-incident review  
   * **facilitator**: User who will facilitate the review. Acquire by following SOP 8.1 (Acquiring Entity Records and IDs)  
   * **review_notes**: Initial notes for the review  
   * **lessons_learned**: Preliminary lessons learned  
   * **action_items**: Action items identified  
   * **status**: Review status  
3. Validate that incident exists and has status of closed using discover_incident_tracking.  
4. Create post-incident review record using manage_improvements.  
5. Log the post-incident review creation action using log_audit_records.

**Halt and use transfer_to_human if you receive the following problems; otherwise complete the SOP:**

* User lacks authorization  
* Missing or invalid required inputs  
* Incident not found or not closed  
* Facilitator user not found or inactive  
* Invalid status value (if provided)  
* Post-incident review creation failed  
* Audit trail logging failure

  ---

## **8. Entity Identification Operations**

### **8.1 Acquiring Entity Records and IDs**

**When to use:** 

* When entity information (name, email, number, etc.) is provided but the specific ID is needed for any operation (incident creation, assignment, linking, reporting, etc.)  
* When you need to retrieve full entity records that match specific search criteria for validation, display, or further processing  
* When you need to verify entity existence, status, or attributes before proceeding with an operation

**Who can perform:**

* All roles

**Steps:**

1. Identify the entity type needed and the appropriate discovery tool:  
   * **Parties** (use `discover_parties`): clients, vendors, users  
   * **Assets** (use `discover_assets`): products, configuration_items  
   * **Contracts** (use `discover_contracts`): subscriptions, sla_agreements  
   * **Incident Tracking** (use `discover_incident_tracking`): incidents, problem_tickets, work_notes, attachments, incident_reports, work_orders  
   * **Coordination** (use `discover_coordination`): escalations, bridges, bridge_participants  
   * **Change Control** (use `discover_change_control`): change_requests, rollback_requests  
   * **Workflows** (use `discover_workflows`): communications, approval_requests  
   * **Improvement** (use `discover_improvement`): root_cause_analyses, post_incident_reviews  
   * **Audit** (use `discover_audit`): audit_trails  
2. Obtain search criteria from the user based on entity type:   
   * **For Clients:**  
     1. `client_name`: Legal or business name  
     2. `registration_number`: Client registration number  
     3. `company_type`: enterprise, mid_market, smb, startup  
     4. primary_address: Primary address  
     5. support_coverage: 24x7, business_hours, on_call  
     6. preferred_communication: email, portal, phone, slack  
     7. `status`: active, inactive  
   * **For Users:**  
     1. `email`: User's email address (unique identifier)  
     2. `first_name`: User's first name  
     3. `last_name`: User's last name  
     4. `role`: incident_manager, technical_support, account_manager, executive, system_administrator,client_contact  
     5. `status`: active, inactive  
     6. `client_id`: Associated client (for client_contact role)  
     7. timezone: User’s timezone  
   * **For Configuration Items:**  
     1. ci_name: Name of the configuration item  
     2. ci_type: server, application, database, network, storage, service  
     3. environment: production, staging, development, testing  
     4. operational_status: operational, degraded, down  
     5. responsible_owner: User responsible for the CI  
   * **For SLA Agreements:**  
     1. client_id: Associated client identifier  
     2. tier: premium, standard, basic  
     3. support_coverage: 24x7, business_hours, on_call  
     4. effective_date: SLA effective start date  
     5. expiration_date: SLA expiration date  
     6. created_by: User who created the SLA  
     7. status: active, inactive, expired  
   * **For CI Client Assignments:**  
     1. ci_id: Configuration item identifier  
     2. client_id: Client identifier  
     3. created_at: Assignment timestamp  
   * **For Incidents:**  
     1. incident_number: Unique incident number (e.g., INC0012345)  
     2. title: Incident title  
     3. severity: P1, P2, P3, P4  
     4. status: open, in_progress, monitoring, resolved, closed  
     5. reported_by: User who reported  
     6. assigned_to: Currently assigned user  
     7. category: inquiry/help, software, hardware, network, database  
     8. problem_id: Linked problem ticket (if applicable)  
     9. impact: critical, high, medium, low  
     10. urgency: critical, high, medium, low  
   * **For Problem Tickets:**  
     1. problem_number: Unique problem number (e.g., PRB0001234)  
     2. title: Problem title  
     3. description  
   * **For Escalations:**  
     1. `incident_id`: Related incident identifier  
     2. `status`: pending, approved, denied, cancelled  
     3. `escalated_from`: User who requested escalation  
     4. `escalated_to`: User receiving escalation  
     5. approver: User who approved/denied the escalation   
   * **For Bridges:**  
     1. `bridge_number`: Unique bridge number (e.g., BRG0001234)  
     2. `incident_id`: Related incident identifier  
     3. `bridge_type`: major_incident, coordination, technical  
     4. `bridge_host`: Incident manager hosting bridge  
     5. `status`: active, closed  
   * **For Bridge Participants:**  
     1. `bridge_id`: Associated bridge identifier  
     2. `user_id`: Participant user identifier  
     3. `role_in_bridge`: host, technical_support, account_manager, executive  
   * **For Change Requests:**  
     1. `change_number`: Unique change number (e.g., CHG0001234)  
     2. `incident_id`: Linked incident (if applicable)  
     3. `title`: Change request title  
     4. `change_type`: standard, normal, emergency  
     5. `risk_level`: low, medium, high, critical  
     6. `status`: requested, approved, denied, scheduled, implemented, cancelled  
     7. `requested_by`: User who requested change  
   * **For Rollback Requests:**  
     1. `rollback_number`: Unique rollback number (e.g., RBK0001234)  
     2. `change_id`: Original change request identifier  
     3. `incident_id`: Incident caused by the change  
     4. `status`: requested, approved, executed, failed  
     5. `requested_by`: User who requested rollback  
   * **For Work Orders:**  
     1. `work_order_number`: Unique work order number (e.g., WO0001234)  
     2. `change_id`: Linked change request (if applicable)  
     3. `incident_id`: Linked incident (if applicable)  
     4. `title`: Work order title  
     5. `assigned_to`: User assigned to work order  
     6. `status`: pending, in_progress, completed, cancelled  
   * **For Approval Requests:**  
     1. `reference_id`: Generic reference to record needing approval  
     2. `reference_type`: escalation, bridge, change, rollback, incident_closure, rca  
     3. `requested_by`: User who requested approval  
     4. `approver`: User who must approve  
     5. `status`: pending, approved, denied  
   * **For Communications:**  
     1. `incident_id`: Related incident identifier  
     2. `problem_ticket_id: Related problem_id`  
     3. `communication_type`: status_update, resolution_notice, escalation_notice, bridge_invitation  
     4. `recipient_type`: client, internal, executive  
     5. `sender`: User sending communication  
     6. `recipient`: Specific user recipient (if applicable)  
     7. `delivery_status`: pending, sent, delivered, failed  
   * **For Incident Reports:**  
     1. `report_number`: Unique report number (e.g., RPT0001234)  
     2. `incident_id`: Related incident identifier  
     3. `report_type`: post_incident_review, client_impact, compliance  
     4. `report_status`: draft, completed, approved, archived  
     5. `generated_by`: User who generated report  
   * **For Root Cause Analyses:**  
     1. `rca_number`: Unique RCA number (e.g., RCA0001234)  
     2. `incident_id`: Related incident identifier  
     3.   
     4. `assigned_to`: User conducting analysis  
     5. `analysis_method`: 5_whys, fishbone, timeline, fault_tree, kepner_tregoe  
     6. `status`: assigned, in_progress, completed, approved  
   * **For Post-Incident Reviews:**  
     1. `incident_id`: Related incident identifier  
     2. `facilitator`: User facilitating the review  
     3. `status`: scheduled, completed, cancelled  
     4. `scheduled_date`: Date for the review  
   * **For Attachments:**  
     1. `reference_id`: ID of related record  
     2. `reference_type`: incident, change, rca, report, pir, communication, work_order, problem  
     3. `file_name`: Name of the file  
     4. `uploaded_by`: User who uploaded  
   * **For Work Notes:**  
     1. `incident_id`: Related incident identifier  
     2. `problem_ticket_id: Related problem ticket ID`  
     3. `created_by`: User who created note  
     4. `note_text`: Content of the note  
3. Search for the entity using the appropriate discovery tool from any of the above with the provided criteria and try to provide as many criteria as possible to the tool.  
4. You will retrieve the records that match the criteria along with the ID field for each record.

