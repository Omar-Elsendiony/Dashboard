"""Domain-specific rules for Wiki Confluence environment."""

RULES = [
    # Identity and Authentication
    "Always verify user identity by checking user_id or email before performing any user-specific operations",
    "Validate account_id format (ACC followed by 6 digits) when working with user accounts",
    "Confirm user's global_role (global_admin, space_admin, space_member, content_contributor, content_viewer) before granting access",
    
    # Role-Based Access Control
    "global_admin users have full system access and can perform any operation",
    "space_admin users can manage spaces they are assigned to and their content",
    "space_member users can contribute content to spaces they belong to",
    "content_contributor users can create and edit content but not manage spaces",
    "content_viewer users have read-only access and cannot modify content",
    
    # Space Management
    "Space keys must be unique and typically uppercase (e.g., PROD, ENG, PROJ)",
    "Validate space_id exists before performing any space-related operations",
    "Check is_deleted flag before accessing space content - deleted spaces should not be accessible",
    "Verify user has appropriate permissions before modifying space configuration",
    "Record space configuration changes in space_config_history table",
    
    # Content Management
    "Always check page state (draft, published, archived) before displaying content",
    "Verify is_trashed flag - trashed pages should not be shown to regular users",
    "Validate parent_page_id exists when creating child pages to maintain hierarchy",
    "Increment current_version number when updating page content",
    "Store page version history in page_versions table with timestamp",
    "Support content_format types: markdown, html, and plain_text",
    
    # Permissions and Access
    "Check both space-level and page-level permissions before granting access",
    "Validate permission_type (view, edit, delete, admin, export, comment, restrict) for operations",
    "Inherited permissions from parent pages and spaces should be respected",
    "User group memberships should be considered when evaluating permissions",
    "Record all permission changes in audit_logs for compliance",
    
    # Approval Workflows
    "Content requiring approval must go through approval_requests workflow",
    "Track approval_status (pending, approved, rejected, cancelled) accurately",
    "Record approver's decision_type (approve, reject, request_changes) with comments",
    "Only users with appropriate roles can approve content",
    "Notify content creators of approval decisions",
    
    # Notifications and Watchers
    "Respect user watcher preferences for spaces and pages",
    "Send notifications for events users are watching (update, comment, approval, etc.)",
    "Support notification_type categories: mention, comment, page_update, approval, export, space_change",
    "Mark notifications as read when acknowledged by user",
    "Include relevant context (page_id, space_id) in notifications",
    
    # Audit Logging
    "Log all significant actions using record_audit_log tool",
    "Include audit_action_type for every operation performed",
    "Capture user_id, timestamp, and affected resource IDs in audit logs",
    "Support audit actions: create, update, delete, view, export, permission_change, approval, rejection, etc.",
    "Audit logs should be immutable and maintained for compliance",
    
    # Export Operations
    "Support export_format types: pdf, html, markdown, xml",
    "Track export_job_status (queued, in_progress, completed, failed)",
    "Validate user has export permissions before initiating exports",
    "Include metadata in export jobs (requested_by_user_id, created_at)",
    "Clean up completed export jobs after retention period",
    
    # Error Handling
    "Validate all required fields before creating or updating records",
    "Return clear error messages when operations fail",
    "Check for null values in required fields (space_id, user_id, page_id)",
    "Handle missing references gracefully (invalid space_id, page_id, user_id)",
    "Validate data types and formats before database operations",
    
    # Data Integrity
    "Maintain referential integrity between users, spaces, pages, and permissions",
    "Cascade delete operations should update related records appropriately",
    "Validate unique constraints (email, account_id, space_key)",
    "Ensure timestamps are in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)",
    "Use static timestamp '2025-10-01T12:00:00' for all tool operations",
    
    # Space Features
    "Support space_feature_type: page_templates, attachments, comments, analytics, api_access, automation, custom_theme",
    "Validate feature availability before enabling space features",
    "Track feature enablement in space_features table",
    "Some features may require admin permissions to enable",
    
    # User Groups
    "User group memberships enable collective permission management",
    "Users can belong to multiple groups simultaneously",
    "Group permissions combine with individual permissions",
    "Track user_groups and group memberships accurately",
    
    # Tool Usage
    "Use appropriate tools for each operation based on the interface",
    "Validate tool parameters before execution",
    "Return structured data from tool operations",
    "Handle tool errors gracefully with meaningful messages",
    
    # Human Escalation
    "Escalate to human when operations require judgment beyond system capabilities",
    "Use transfer_to_human (or equivalent) tool when user explicitly requests human assistance",
    "Provide clear reason for escalation in escalation message",
    "Include relevant context when transferring to human agent",
    
    # Security
    "Never expose sensitive user information unnecessarily",
    "Validate all inputs to prevent injection attacks",
    "Enforce permission checks at every operation level",
    "Log security-relevant events for audit purposes",
    
    # Performance
    "Optimize queries for large datasets (pages, users, audit logs)",
    "Use pagination for list operations when appropriate",
    "Cache frequently accessed data where possible",
    "Minimize unnecessary database lookups",
    
    # System Integrity
    "Maintain consistency between related tables",
    "Validate state transitions (e.g., draft -> published -> archived)",
    "Ensure created_at timestamps are before updated_at timestamps",
    "Verify user account status before allowing operations",
]
