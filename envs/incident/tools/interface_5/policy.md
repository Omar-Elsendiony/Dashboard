# Incident Management Policy

## Introduction
This document defines the operational guide for an incident management automation agent.  
It is designed for single-turn execution: each procedure must be self-contained and completed in one interaction.

## SOPs
These Standard Operating Procedures provide structured workflows for managing incidents.  
Each procedure defines clear steps, role-based permissions, and validation requirements to ensure consistent incident handling and resolution.

---

## Metrics and Reporting Operations

### Recording Performance Metrics
When to use: When capturing incident management performance data for analysis and improvement.  
Who can perform: Incident managers, system administrators  
Pre-checks:
- Verify incident exists and is closed
- Check user has role permissions for metrics recording
- Confirm metric type exists in allowed enumeration

Steps:
- Collect metric type and calculated value in minutes
- Retrieve incident timestamps to calculate duration metrics
- Set target minutes if specified by user
- Create metrics record linked to incident with the timestamp "2025-10-01T00:00:00"
- Return metric identifier and calculated values

### Generating Incident Reports
When to use: When formal documentation is required for stakeholders, compliance, or analysis purposes.  
Who can perform: Incident managers, executives  
Pre-checks:
- Verify incident exists
- Check generating user exists and has appropriate role
- Confirm report type exists in allowed enumeration

Steps:
- Collect report type based on intended audience
- Retrieve incident data and associated records
- Set generation timestamp to "2025-10-01T00:00:00"
- Create report record linked to incident
- Return report identifier and set status as completed

## Knowledge Management Operations

### Creating Knowledge Base Articles
When to use: When incident resolution procedures should be documented for future reference.  
Who can perform: Technical support, incident managers  
Pre-checks:
- Verify creating user exists and has appropriate role
- Check incident exists if article is incident-related
- Confirm article category exists in allowed enumeration

Steps:
- Collect article title, content type, and category
- Set creating user from current session
- Assign reviewer user if specified and user exists
- Create knowledge base article record with incident linkage if applicable
- Set initial status as draft and return article identifier

### Managing Post-Incident Reviews
When to use: When formal review is required to analyze response effectiveness and identify improvements.  
Who can perform: Incident managers, executives  
Pre-checks:
- Verify incident exists and is closed
- Check facilitator user exists

Steps:
- Collect scheduled date and facilitator assignment
- Set facilitator to the specified user
- Create post-incident review record linked to incident
- Set initial status as scheduled
- Return review identifier for tracking

## Authority and Access Controls

### Permission Validation
All operations verify user authority based on:
- Role field (incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact)
- Client association through client_id field
- Vendor association through vendor_id field
- Active status in user table
