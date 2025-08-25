# Policy: User, Worker, Time, and Reimbursement Management

**Effective Date: July 1, 2025**

---

### Overview

This policy is responsible for managing day-to-day organizational workflows involving users, workers, time tracking, reimbursements, and virtual cards. Every operation should happen within the boundaries of a known and authenticated organization or user context. The system should not allow any action that is unscoped or improperly linked.

---

### General Rules

Every worker must be associated with both a valid user account and an organization. The system should not allow actions on workers who are not properly linked. Whenever the system fetches, creates, or updates a record—whether it is a user, time log, or reimbursement—it must ensure the structure strictly follows the defined schema.

For any action involving monetary amounts—such as updating card limits or reimbursing expenses—the system must validate that the values are within expected bounds and formatted in valid currency before proceeding.

---

### Key Behaviors and Conditions

- If a worker does not have any reimbursements submitted or recorded, the system should return an empty list rather than a null value or error.

- The system should allow updates to virtual card limits only when the card status is active. It should not permit such updates if the card is revoked, blocked, or expired. A clear explanation must be returned.

- Time entries should only be allowed for workers who are marked as active. The system should reject any logging attempt made for suspended or terminated workers and return an informative message.

- Once a reimbursement is marked as paid, the system must treat it as immutable. It should not allow any further editing or reprocessing through any method.

- The system should not permit suspended workers to be assigned or reassigned to departments or organizations, regardless of the user's role attempting the action.

---

### Best Practices to Follow

- Error messages should be user-friendly and abstracted. For instance, instead of returning a technical error, the system should say, “This worker is no longer eligible for assignment.”

- The system must check roles before performing sensitive actions. Only users with roles like HR manager or admin should be allowed to deactivate users or assign workers.

- The system should avoid over-fetching data. Summaries, such as those for payroll totals or time aggregates, should return only the most relevant fields.

- All dates should follow ISO 8601 format. If a static date is needed, it should default to `2025-07-01`.

---

### What the System Should Not Allow

- The system should not allow creation of users with duplicate email addresses. If the email already exists, the operation must fail with a clear message indicating the conflict.

- No time entry should exceed 24 hours in duration. The system should either cap or reject any entry above this limit.

- Virtual card spending limits must be positive and must not exceed 100,000 units in their configured currency. Any value outside this range should be rejected.

- The system should not allow a user to be deactivated if they are currently linked to any reimbursements or payroll records that are pending or ongoing.

- Reassigning a worker across organizations or departments should only be allowed for users with elevated roles, such as admins or HR managers. All others must be restricted from doing so.