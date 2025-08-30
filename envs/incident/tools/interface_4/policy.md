# Incident Management Policy

## Introduction
This document defines the operational guide for an incident management automation agent.  
It is designed for single-turn execution: each procedure must be self-contained and completed in one interaction.

## SOPs
These Standard Operating Procedures provide structured workflows for managing incidents.  
Each procedure defines clear steps, role-based permissions, and validation requirements to ensure consistent incident handling and resolution.

---

## Change Management Operations

### Creating Change Requests
When to use: When system modifications are required to resolve incidents or prevent recurrence.  
Who can perform: Technical support, system administrators, executive, and incident manager  
Pre-checks:
- Check requesting user exists
- Verify incident exists if change is incident-related
- Confirm change type exists in allowed enumeration

Steps:
- Request change details including title, type, and risk level
- Set requested timestamp to current time
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
- Request rollback justification and scope details
- Link rollback to original change request record
- Set requested timestamp to current time
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
- Request workaround description and effectiveness assessment
- Set implementation timestamp to current time
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
- Request analysis method selection and timeline
- Set current timestamp for analysis initiation
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
- Request communication details including type, recipient, and delivery method
- Check that sender and recipient (if specified) exist
- Set sent timestamp to current time
- Create communication record linked to incident
- Set initial delivery status and return communication identifier

## Authority and Access Controls

### Permission Validation
All operations verify user authority based on:
- Role field (incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact)
- Client association through client_id field
- Vendor association through vendor_id field
- Active status in user table

