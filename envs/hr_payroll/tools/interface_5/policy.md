# Policy: Invoices, Reimbursements, Roles, and Worker Access Control

**Effective Date: July 1, 2025**

---

### Scope and Responsibilities

This policy is responsible for managing key operational activities such as invoice handling, reimbursement tracking, role assignments, time entry processing, and access control for workers. It also covers workflows around team assignments, logging bonuses, issuing or modifying virtual cards, and secure offboarding processes. All actions must respect organizational boundaries and user permissions.

---

### General Operational Rules

- Before performing any operation, the system must verify the existence and validity of referenced entities—this includes workers, users, teams, cards, invoices, and reimbursements.

- Contracts, payroll items, and reimbursements must only be created or modified if there is an active and valid relationship linking the involved user, worker, and organization.

- All financial transactions must remain within their appropriate contract scopes and valid timeframes. The system should enforce these boundaries to prevent misuse or misallocation.

---

### Conditional Logic and Behavior
- Workers may only be added to teams within the same organization. Cross-org assignments must be blocked.

- User role assignments must validate role eligibility and ensure the user is part of the relevant organization.

- Invoice details may only be changed before the invoice is marked as paid or approved.

- Contracts created for workers must validate that the worker belongs to the specified organization and is not terminated.

- Virtual cards may only be enabled if the worker is active and the linked contract supports virtual payments.

- Fetching time entries by period must respect date limits and may exclude unapproved entries unless explicitly included.

- Freezing worker access should disable both card use and contract activity while maintaining audit trail.

- Reimbursement total queries must include only those reimbursements with status 'paid' or 'approved'.

- Bonuses logged must cite a contract, a justification, and must not exceed configured caps without override approval.

- Submitting invoice payments must confirm invoice approval status and must attach a payment method.

- Contract updates must not change the associated organization and should preserve historical rate tracking.

- Reimbursement status can only move forward in flow (e.g., submitted → approved → paid) unless explicitly overridden.

- Virtual card status changes must log the actor and justification if disabling or reactivating a card.

- User document lists must be scoped to the requesting user or include admin override credentials.

- Only workers with at least one active virtual card should appear in this listing unless status filters are used.

- Working detail views for users with cards must include only currently linked and active user–card associations.

- Invoice summaries must group by status and may optionally filter by due date or amount thresholds.

- If a user tries to assign a worker to a team that belongs to a different organization, the system must block the operation and inform the user that cross-organization assignments are not permitted.

- When marking an invoice as paid, the system must verify that both the invoice and the payment record exist, and that the payment correctly references the intended invoice. If any part of this linkage fails, the action must be rejected.

- Reimbursements that are already in a 'paid' status must not be altered in any way. The system should treat them as final and immutable from this interface.

- A worker must not be removed from the system if they are associated with active contracts or ongoing payroll entries. Any such removal attempt should be blocked until those links are resolved.

- Virtual cards that are marked as revoked or expired must not be reactivated unless their status explicitly supports re-enablement. The system should not allow any changes otherwise.

- If a worker's access is frozen, their user account must be transitioned to a 'suspended' status. Additionally, all virtual cards still marked as active for that worker must be blocked immediately to secure payment systems.

---

### Best Practices and Recommendations

- Validation messages should be clear and specific, helping users understand exactly why an action was denied. For example: “Worker not found,” “Card already revoked,” or “Cannot remove worker with active payroll.”

- Virtual card status transitions must be tightly controlled. The system should allow reactivation only for cards in 'blocked' or 'expired' status. Cards marked as 'revoked' should be treated as permanently deactivated.

- When logging bonuses or creating contracts, the system must always link them to the worker’s current, active contract and associated organization. Duplication or orphaned records should be avoided.

- Responses to document and reimbursement queries should be filtered to highlight active records and sorted by relevant dates to ensure users can quickly access recent and relevant information.

- Submitted dates—such as contract starts—and financial values—like bonuses—must be validated for realism and policy compliance. The system should enforce that all monetary amounts are positive and within expected limits.

- All dates should follow ISO 8601 format. If a static date is needed, it should default to `2025-07-01`.

---

### Security and Limitations

- Only users with authorized roles—such as HR or admin—should be allowed to assign roles, create contracts, or adjust financial elements like payroll bonuses or invoice payments.

- Time entry queries over a date range must include a valid start and end date. The system should restrict such queries to no more than one full calendar year to reduce excessive data loads.

- Contracts should not be created for workers who do not exist or who have been offboarded. The system must block any such creation attempts.

- Users whose status is marked as 'suspended' or 'inactive' must not be allowed to undergo role changes.

- Invoices and reimbursements must only be linked to valid, existing workers and organizations. If the target records do not exist, the system must reject the operation gracefully and return a clear explanation.
