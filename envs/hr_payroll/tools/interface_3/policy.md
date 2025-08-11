# Policy: Contracts, Invoices, Reimbursements, and Payroll Access

**Effective Date: July 1, 2025**

---

### Overview

This policy governs operations related to invoices, contracts, reimbursements, payroll summaries, and virtual card assignment. It handles both data management and query access at an operational level. All actions must respect record status, organizational policy, and system-defined relationships to ensure consistency and compliance across financial workflows.

---

### General Rules

- Every operation must validate that it references existing, valid records—such as workers, contracts, invoices, or payments—before execution. The system should not allow actions on missing or invalid entities.

- The system should not allow new invoices or reimbursements to be created for workers who are marked as terminated or suspended.

- Virtual cards should only be issued to workers who are currently active. Each card must be associated with a valid financial provider and linked user account.

- Any update that involves currency—such as invoicing, reimbursements, or payments—must verify that the currencies are compatible and align with organizational financial policies.

---

### Key Behaviors and Conditions
- Invoices must be associated with a valid worker, a linked contract, and a positive due amount. Issued invoices may be allowed but require confirmation before marking as paid.

- Invoices may only be marked as paid if their current status is 'issued' or ‘unpaid’. Payment confirmation should include timestamp and method.

- Invoice status queries by organization should filter based on org ID and time range where applicable.

- Reimbursements must only be processed if linked to a valid worker and fall within allowable expense categories defined by the organization or default policy.

- Payroll breakdown views should be restricted to confirmed or completed runs, not draft or partial computations.

- Virtual card issuance requires a currently active worker and a valid financial provider. Issuance should be blocked for suspended or terminated users.

- Contract termination should only occur if the worker is not already terminated, and the system must capture a clear reason or source for the action.

- Updates to worker bank information must include a valid account number, IFSC code, and verified user identity. Previous bank details should be archived.

- Team assignment lookups should only return active users and explicitly exclude any suspended or inactive memberships.

- User working details should reflect only users currently linked to active organizations or contracts, and may exclude historical records unless explicitly requested.


- A worker should be considered active only if their employment status is active and they have at least one ongoing contract with a status of active or signed. The system should enforce both conditions.

- Contracts that have been marked as ended or terminated must not be available for invoice generation or editing. The system should block any such attempts.

- The system should only allow a reimbursement to be processed if the worker is active and correctly linked to both a user and an organization.

- When marking an invoice as paid, the system must ensure the referenced payment record exists and correctly links to that invoice. If the linkage is invalid, the operation should be blocked.

- When fetching team assignments, the system should always return a list—even if the worker has no associated team—to ensure consistent API responses.

---

### Best Practices to Follow

- When creating new records such as invoices, virtual cards, or reimbursements, the system should return a fully populated response, including all relevant details and generated IDs.

- If a request is rejected due to a mismatch in state—like trying to pay a cancelled invoice—the system should return a clear, readable message explaining the reason.

- Summaries for payroll or contracts should be categorized for readability and ease of analysis.

- All dates should follow ISO 8601 format. If a static date is needed, it should default to `2025-07-01`.

---

### What the System Should Not Allow

- Workers who do not have any active contracts must not appear in the list of active workers.

- If a virtual card is already active for a user, the system should not allow another card to be issued for the same user.

- Invoices that are marked as paid should not be modified again. The system must block any further edits or attempts to re-pay these invoices.

- Contracts that are ended or terminated should not be reactivated or extended under any condition.

- When updating bank account information, the system must not overwrite the currency unless explicitly directed to do so by policy or the user.