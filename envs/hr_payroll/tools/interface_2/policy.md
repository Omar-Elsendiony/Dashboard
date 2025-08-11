# Policy: Contracts, Payroll, Reimbursements, and Card Security

**Effective Date: July 1, 2025**

---

### Overview

This policy governs contract management, payroll execution, reimbursement approvals, time entry evaluations, and the control of payment flows and virtual card security. Each action should be validated for accuracy, legitimacy, and alignment with defined processes. The system should enforce these workflows to maintain financial integrity and secure processing.

---

### General Rules

- Any action involving payments or reimbursements must be connected to valid, verifiable records. The system should not allow execution on orphaned references or unverified data.

- A contract should only be extended if it belongs to a legitimate worker–organization relationship. Before allowing updates, the system must confirm that valid start and end dates are present and pass validation.

- Blocking a suspicious payment or virtual card should only happen if the system has sufficient evidence to justify the action. Once blocked, the system must also flag the status to prevent the same issue from recurring.

- Payroll run details should only be accessible once a run has reached the “confirmed” state. The system must not expose full details for draft or failed runs.

---

### Key Behaviors and Conditions

- Reimbursements are only eligible for approval if they are marked as ‘submitted’. The system should exclude reimbursements in any other status—such as ‘approved’, ‘paid’, or ‘rejected’—from approval workflows.

- If a payroll run contains no line items, the system should still return a structured response object with an empty list. It must not return an error or null result.

- A document that is linked to any active or pending contract must not be allowed to transition into a ‘deleted’ state. The system should enforce referential integrity at all times.

- Only time entries in the ‘submitted’ or ‘draft’ status should be considered eligible for overtime approval. The system must reject any override attempts made on other statuses.

- Contracts must be uniquely scoped to each worker and time period. If the system detects an overlap or duplicate range, the new contract creation should be blocked.

- Suspicious payments are only blocked if a payment has not already been settled and matches a fraud condition, such as duplicate payment attempts or irregular transaction routing.

- Virtual cards can only be blocked if they are marked 'active' and not already flagged. If blocked, the action must reflect in system audit trails.

- A contract can only be extended if the new end date is later than the existing one and remains within organizational bounds or defined limits.

- New contracts require a verified user ID, a valid link to an organization, and acceptable payment terms. Optional fields like probation may be included but should follow configured defaults.

- Detailed payroll run access is limited to runs in ‘confirmed’ status. Draft or failed runs must avoid exposing full transaction-level details to ensure data consistency.

- Time summaries are grouped by date and only include workers who were part of the requested team during the corresponding logged periods.

- Documents uploaded must include the type and owner identity. Systems may optionally flag or block duplicate uploads based on metadata or hash match.

--

### Best Practices to Follow

- When a payment or card is blocked, do not perform any operations on it.

- Team-level time summaries should include per-day aggregates and should support summarization across multiple workers in the same response.

- All dates should follow ISO 8601 format. If a static date is needed, it should default to `2025-07-01`.

---

### What the System Should Not Allow

- The system must not allow payments marked as failed to be retried, reversed, or toggled. These records should be treated as final once flagged.

- Contract date validation must be enforced: the end date must always come after the start date, and both dates must be explicitly provided at the time of contract creation.

- If a card has already been revoked, expired, or blocked, the system should not allow another block operation. This is redundant and may confuse users.

- Only documents that are in a live and available state should be eligible for modification. Archived or deleted documents must not allow updates or status changes of any kind.

- The ability to view full payroll run details should be limited strictly to runs marked as “confirmed”. For all other statuses, access should be limited to summaries or deferred until confirmation.
