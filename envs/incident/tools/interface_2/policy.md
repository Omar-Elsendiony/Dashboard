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

### Updating Incident Status
When to use: When incident conditions change requiring status modifications or progress updates.  
Who can perform: Incident managers, technical support, executive  
Pre-checks:
- Verify incident exists and is accessible to user
- Check user's role allows incident modifications

Steps:
- Retrieve current incident record
- Collect specific status changes or field updates needed
- Check that new status value matches allowed enum values (if there is any)
- Create incident update record(s) documenting the change(s) along with logging the user who conducted the change
- Apply changes to incident with the user identifier
- Return updated incident information

#### subscription tier values and metrics
**Premium Tier**
Target clients: Enterprise customers with mission-critical operations
Response times by severity:
- P1 (Critical): 15-30 minutes initial response
- P2 (High): 1-2 hours initial response
- P3 (Medium): 4-8 hours initial response
- P4 (Low): 24-48 hours initial response

Resolution times:
- P1: 2-4 hours resolution target
- P2: 8-24 hours resolution target
- P3: 48-72 hours resolution target
- P4: 128 hours resolution target
Availability guarantee: 99.9% uptime
Support coverage: 24/7/365

**Standard Tier**
Target clients: Mid-market businesses with important but less critical operations
Response times by severity:
- P1: 1-2 hours initial response
- P2: 4-8 hours initial response
- P3: 24 hours initial response
- P4: 48-72 hours initial response

Resolution times:
- P1: 8-24 hours resolution target
- P2: 24-48 hours resolution target
- P3: 72-120 hours resolution target
- P4: 168 hours resolution target
Availability guarantee: 99.5% uptime
Support coverage: Business hours with on-call for critical issues

**Basic Tier**

Target clients: Small businesses and startups with standard operational needs
Response times by severity:
- P1: 4-8 hours initial response
- P2: 24 hours initial response
- P3: 48-72 hours initial response
- P4: 5-7 business days initial response

Resolution times:
- P1: 24-48 hours resolution target
- P2: 72-120 hours resolution target
- P3: 5-10 business days resolution target
- P4: 2 weeks

Availability guarantee: 99.0% uptime
Support coverage: Business hours only


## Product and Infrastructure Operations

### Creating Product Records
When to use: When adding new systems or applications requiring incident management coverage.  
Who can perform: Technical support, system administrators  
Pre-checks:
- Check that product name is unique
- Verify all required fields are provided
- Confirm vendor exists if vendor support is specified

Steps:
- Acquire product information including name, type, and version
- Check for existing products with same name
- Link to vendor record if external support required
- Create product record and return product identifier

### Managing Infrastructure Components
When to use: When documenting system components that support products and services.  
Who can perform: Technical support, system administrators.  
Pre-checks:
- Verify product exists if component is associated with a product
- Check that component name is unique within the specified product

Steps:
- Acquire component details including name, type, environment, and staus
- Check for existing components with same name under same product
- Set operational status based on user input
- Record port numbers if provided
- Create component record linked to product

## Subscription and Service Level Management

### Creating Client Subscriptions
When to use: When establishing service agreements and coverage levels for clients.  
Who can perform: Account managers, incident manager, executive  
Pre-checks:
- Verify client record exists
- Check product record exists 

Steps:
- Collect subscription details including type, service level tier, and dates
- Set recovery time objectives based on user input
- Define start and end dates as specified
- Link subscription to specified client and product records
- Create subscription record with active status

### Creating SLA agreement
Who can perform: Account managers, system administrators, executives
Pre-checks:
- Verify subscription exists and is active
- Check user has authority to create SLA agreements for this client
- Validate response/resolution times align with subscription tier

Use case: When defining specific SLA metrics for client subscriptions



### Managing Service Level Agreements
When to use: When defining response and resolution requirements for different incident severities.  
Who can perform: Account managers, incident managers, and executives.  
Pre-checks:
- Verify subscription record exists
- Check that severity level exists in allowed enumeration

Steps:
- Collect service level parameters for specified severity level
- Set response time requirements in minutes as specified
- Define resolution time objectives in hours as specified
- Set availability percentage targets if provided
- Create SLA record linked to subscription
  

## Authority and Access Controls
#### Permission Validation
All operations verify user authority based on:  
- Role field (incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact)  
- Client association through client_id field  
- Vendor association through vendor_id field  
- Active status in user table
