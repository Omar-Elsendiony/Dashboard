# Incident Management Policy

## Introduction
This document defines the operational guide for an incident management automation agent.  
It is designed for single-turn execution: each procedure must be self-contained and completed in one interaction.

## SOPs
These Standard Operating Procedures provide structured workflows for managing incidents.  
Each procedure defines clear steps, role-based permissions, and validation requirements to ensure consistent incident handling and resolution.

---
## Incident Operations

### Creating Incidents
When to use: When service impacts are detected requiring formal incident management response.  
Who can perform: Incident managers, technical support, and system administrators, 3rd party vendors (vendor_contact), executive  
Pre-checks:
- Check that reporter user exists and has active status
- Verify client exists
- Check that component exists if specified

Steps:
- Collect incident title, category, severity, and impact level
- Set detection timestamp
- Associate with specified client and infrastructure component records
- Create incident record and return incident identifier

#### Severity Classification Process during Incident Creation:  
Evaluate the following conditions and set the corresponding boolean flags (`p1_*`, `p2_*`, `p3_*`) to **True** for every condition that applies based on the available data. Compute severity as **P1** if any P1 condition is `True`; otherwise **P2** if any P2 condition is `True`; otherwise **P3** if any P3 condition is `True`; otherwise **P4**.

**P1 Evaluation:**
- Evaluate whether the incident causes complete outage of business-critical service with no workaround available.
- Evaluate whether the incident impacts the entire enterprise or multiple customers with 5 or more affected parties.
- Evaluate whether the incident has significant regulatory, safety, or financial implications.
- Evaluate whether the incident involves a high-priority customer with contractual P1 requirements or is a recurrent incident.

**P2 Evaluation:**
- Evaluate whether the incident causes major degradation of business-critical services with a workaround available.
- Evaluate whether the incident impacts multiple departments, sites, or critical business functions.
- Evaluate whether the incident risks breaching a high-priority SLA with significant impact.

**P3 Evaluation:**
- Evaluate whether the incident impacts a single department, localized users, or a non-critical function.
- Evaluate whether the incident causes moderate degradation with operations continuing using a minimal workaround.

If none of the P1/P2/P3 conditions apply, set severity as **P4**.

- Set detection timestamp and initial status as open  
- Associate with specified client and reporter.  
- Create incident record with determined severity level and return incident identifier


## Change Management Operations

### Creating Change Requests
When to use: When system modifications are required to resolve incidents or prevent recurrence.  
Who can perform: Technical support, system administrators, executive, and incident manager  
Pre-checks:
- Check requesting user exists
- Verify incident exists if change is incident-related
- Confirm change type exists in allowed enumeration

Steps:
- Collect change details including title, type, and risk level
- Set requested timestamp to "2025-10-01T00:00:00"
- Record requesting user from current session
- Create change request record with incident linkage if applicable
- Set initial status as requested and return change identifier

### Managing Rollback Requests
When to use: When unsuccessful changes require reversion to previous system state.  
Who can perform: Technical support, incident managers, and executive  
Pre-checks:
- Verify change request exists
- Check requesting user exists
- Confirm incident exists if rollback is incident-related

Steps:
- Collect rollback justification and scope details
- Link rollback to original change request record
- Set requested timestamp to "2025-10-01T00:00:00"
- Create rollback request record with proper associations
- Set initial status as requested and return rollback identifier

## Workaround and Resolution Management

### Implementing Workarounds
When to use: When temporary solutions can reduce incident impact while permanent resolution is developed.  
Who can perform: Technical support, incident managers, systems administrator  
Pre-checks:
- Verify incident exists
- Check implementing user exists
- Confirm effectiveness level exists in allowed enumeration

Steps:
- Collect workaround description and effectiveness assessment
- Set implementation timestamp to "2025-10-01T00:00:00"
- Record implementing user from current session
- Create workaround record linked to incident
- Set status as active and return workaround identifier

### Conducting Root Cause Analysis
When to use: When systematic investigation is required to determine incident causation.  
Who can perform: Technical support, incident managers, systems administrator  
Pre-checks:
- Verify incident exists
- Check conducting user exists and has appropriate role
- Confirm analysis method exists in allowed enumeration

Steps:
- Collect analysis method selection and timeline
- Set analysis initiation timestamp to "2025-10-01T00:00:00"
- Create root cause analysis record linked to incident
- Set status as in progress
- Return analysis identifier for tracking progress

## Communication Management

### Recording Communications
When to use: When documenting stakeholder communications during incident response.  
Who can perform: Incident managers, technical support  
Pre-checks:
- Verify incident exists
- Check sender user
- Confirm recipient user exists if specified, or recipient type is valid enum value

Steps:
- Collect communication details including type, recipient, and delivery method
- Check that sender and recipient (if specified) exist
- Set sent timestamp to "2025-10-01T00:00:00"
- Create communication record linked to incident
- Set initial delivery status and return communication identifier

## Authority and Access Controls

### Permission Validation
All operations verify user authority based on:
- Role field (incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact)
- Client association through client_id field
- Vendor association through vendor_id field
- Active status in user table
