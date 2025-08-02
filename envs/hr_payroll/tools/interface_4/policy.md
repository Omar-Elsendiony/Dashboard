# Policy: User, Contract, Payroll, and Organization Onboarding

**Effective Date: July 1, 2025**

---

### Overview

This policy governs the processes of onboarding and managing users, organizations, contracts, payroll components, reimbursements, and virtual card adjustments. It ensures that every onboarding step, contract update, or payroll change is carried out in line with policy, validated relationships, and system integrity. Actions performed must always operate on complete and verified records.

---

### General Rules

- The system must ensure that all referenced entities—such as users, contracts, organizations, and reimbursements—exist and are valid before allowing any action.

- A user should only be onboarded and linked to a worker if both the user and the organization are marked as active. The system must enforce this validation.

- Payroll items must always be tied to a valid contract. If bonuses or deductions are added, the system should require a reason to be recorded.

- Any changes to currency or rate type on a contract must align with the financial policies and structures defined by the organization. The system must prevent unauthorized or incompatible updates.

- When an organization is created, the timezone and region fields must be correctly formatted and validated. Invalid values should block the creation.

---

### Key Behaviors and Conditions
- New user accounts require a unique email and assigned role. Duplicate emails should be rejected.

- User accounts should only be disabled if they are currently marked as active.

- Time entry fetches by project should include filters for date range and exclude rejected entries by default.

- Financial provider details can only be accessed if the provider exists and supports the user's organization.

- User locale and timezone lookups must return defaults if none are explicitly set.

- Worker onboarding requires a verified user and organization match, and may pre-fill contract templates.

- Listing virtual cards by organization must exclude blocked or expired cards unless explicitly requested.

- Workers listed under an organization should be filtered by active contracts unless overridden.

- New organizations must include validated timezone, region, and at least one admin contact.

- Reimbursement rejections must include a reason and can only be performed on non-paid requests.

- Payroll adjustments require a contract reference and a justification field for the change.

- Contract pay term updates must preserve currency compatibility and not reduce rates below minimum wage.

- If a reimbursement is already marked as paid, the system must not allow it to be rejected afterward. Any attempt to do so should be blocked and accompanied by a clear reason message.

- Only contracts that are confirmed should be eligible for new payroll entries. The system should reject adjustments made to contracts that are still in draft or unconfirmed status.

- A user who is already linked to a worker should not be re-onboarded unless that worker’s status is either terminated or inactive. The system must enforce this linkage rule.

- When contracts are updated, the system must ensure that previously paid payroll records remain untouched. No contract change should affect historical payroll data.

---

### Best Practices

- The system should validate all ID references against existing database relationships. No orphaned or mismatched references should be allowed.

- All dates should follow ISO 8601 format. If a static date is needed, it should default to `2025-07-01`.

- When registering a new organization, address information must be stored using the standardized JSON format—even if only partially completed.

- Upon creation or update of any user, contract, reimbursement, or organization, the system should return a fully detailed record in the response, including all relevant fields and identifiers.

---

### What the System Should Not Allow

- Contracts that have been marked as terminated or ended must not be modified or updated further.

- Workers who are in a suspended or pending state should not be allowed to proceed through the onboarding workflow.

- The system must prevent the creation of organizations that have duplicate names or conflicting region entries.

- Reimbursements that are already marked as approved or paid should not be rejected or reprocessed.

- A user must not be disabled if they are the sole admin of an organization. The system should block such actions to preserve administrative access.
