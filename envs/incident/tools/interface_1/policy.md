# Incident Management Policy

## Introduction
This document defines the operational guide for an incident management automation agent.  
It is designed for single-turn execution: each procedure must be self-contained and completed in one interaction.

## SOPs
These Standard Operating Procedures provide structured workflows for managing incidents.  
Each procedure defines clear steps, role-based permissions, and validation requirements to ensure consistent incident handling and resolution.

---

## Client Management Operations

### Creating Client Records
When to use: When registering new enterprise, mid-market, small business, or startup clients requiring incident management services.  
Who can perform: Account managers, system administrators  
Pre-checks:
- Verify client registration number is unique by checking existing client records
- Check that contact email is not already used by another client

Steps:
- Collect complete client information including name, registration number, contact details, and client type
- Check for existing records with same registration number or email
- Set initial status as active unless user specifies otherwise
- Create client record with the timestamp "2025-10-01T00:00:00"
- Returned client identifier and successful creation flag if client was created 

### Updating Client Information
When to use: When client details change or status modifications are required.  
Who can perform: Account managers assigned to the client and system administrators  
Pre-checks:
- Verify client record exists
- Check user has permission to modify this client's information based on their role and client association
- Confirm new registration number or email is unique if being changed

Steps:
- Retrieve current client record
- Collect specific fields requiring updates
- Apply changes with the timestamp "2025-10-01T00:00:00"
- Returned successful creation flag if client information was updated

## User Management Operations

### Creating User Accounts
When to use: When adding personnel to the incident management system.  
Who can perform: System administrators and incident managers  
Pre-checks: 
- Check that email address is unique
- Verify all required fields are provided by user
- Confirm client or vendor exists if association is specified

Steps:
- Acquire complete user information including name, email, role, and department
- Check for existing records with same email address, users should have unique email
- Associate user with specified client or vendor if provided
- Set status as active 
- Create user record with the timestamp "2025-10-01T00:00:00" and return user identifier

### Managing User Permissions
When to use: When modifying user access levels or role assignments.  
Who can perform: System administrators and incident managers  
Pre-checks:
- Verify user record exists
- Check requesting user has authority based on role (system administrators, incident managers only)
- Confirm new role value exists in allowed enumeration

Steps:
- Retrieve current user record
- Collect specific role or status changes needed
- Check that new role assignment is valid 
- Apply updates with modifier identification
- Return updated user record and confirm changes saved

## Vendor Management Operations

### Registering Vendor Information
When to use: When adding external service providers to the incident management ecosystem.  
Who can perform: System administrators, incident managers, and executives.  
Pre-checks:
- Check that vendor name, contact phone and emails are unique
- Verify all required fields are provided
- Confirm vendor type exists in allowed enumeration values

Steps:
- Acquire vendor details including name, type, and contact information
- Check for existing records with same vendor name
- Set status as active unless user specifies otherwise
- Create vendor record with the timestamp "2025-10-01T00:00:00"
- Return vendor identifier and confirm successful creation

## Authority and Access Controls

### Permission Validation
All operations verify user authority based on:
- Role field (incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact)
- Client association through client_id field
- Vendor association through vendor_id field
- Active status in user table
