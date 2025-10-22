# Wiki Confluence Environment Documentation

## Overview

The Wiki Confluence environment is a comprehensive mock implementation of a Confluence-like wiki platform. It provides a full-featured collaboration space with user management, content creation, permissions, approval workflows, and audit logging.

## Core Concepts

### Users and Authentication

Users are identified by:

- **user_id**: Unique identifier for each user
- **email**: User's email address (unique)
- **account_id**: Account identifier in format "ACC" + 6 digits (e.g., "ACC000001")
- **full_name**: User's display name
- **global_role**: User's system-wide role determining base permissions

### User Roles

The system supports five global roles with hierarchical permissions:

1. **global_admin**: Full system access, can manage all spaces, users, and settings
2. **space_admin**: Can create and manage spaces they own or are assigned to
3. **space_member**: Can contribute content to spaces they belong to
4. **content_contributor**: Can create and edit content but not manage spaces
5. **content_viewer**: Read-only access to content

### Spaces

Spaces are top-level containers for organizing content:

- **space_id**: Unique identifier
- **space_key**: Short uppercase identifier (e.g., "PROD", "ENG", "PROJ")
- **space_name**: Human-readable space name
- **space_purpose**: Description of space's intended use
- **is_deleted**: Soft delete flag

Common space purposes:

- Sales playbooks and training materials
- Marketing campaigns and strategies
- Customer support knowledge base
- Research findings and analysis
- HR policies and employee handbook
- Technical documentation
- Product documentation

### Pages

Pages are the primary content units within spaces:

- **page_id**: Unique identifier
- **space_id**: Parent space containing the page
- **parent_page_id**: Optional parent page for hierarchical organization
- **title**: Page title
- **content_format**: Format of content (markdown, html, plain_text)
- **current_version**: Current version number
- **state**: Content state (draft, published, archived)
- **is_trashed**: Soft delete flag for trash functionality
- **is_published**: Publication status

### Page Hierarchy

Pages can be organized hierarchically:

- Top-level pages have `parent_page_id = null`
- Child pages reference their parent via `parent_page_id`
- Multiple levels of nesting are supported
- Permissions and watchers can be inherited

### Content States

Pages progress through different states:

- **draft**: Work in progress, not visible to all users
- **published**: Officially published and visible
- **archived**: Older content kept for reference

### Page Versions

All page modifications are tracked through versions:

- **version_number**: Incremental version identifier
- **content**: Actual page content at this version
- **change_comment**: Description of changes made
- **created_by_user_id**: User who made the change
- **created_at**: Timestamp of version creation

## Permissions System

### Permission Types

The system supports granular permissions:

- **view**: Ability to view content
- **edit**: Ability to modify content
- **delete**: Ability to delete content
- **admin**: Administrative access to space/page settings
- **export**: Ability to export content
- **comment**: Ability to add comments
- **restrict**: Ability to restrict access

### Permission Levels

Permissions can be assigned at two levels:

1. **Space-level**: Apply to entire space and can cascade to pages
2. **Page-level**: Specific to individual pages

### Permission Targets

Permissions can be granted to:

- Individual users (via user_id)
- User groups (via group_id)

### Permission Inheritance

- Page permissions can inherit from space permissions
- Child pages can inherit from parent pages
- Explicit permissions override inherited ones

## User Groups

User groups enable collective permission management:

- **group_id**: Unique group identifier
- **group_name**: Display name for the group
- **description**: Purpose of the group
- Users join groups through user_groups membership table
- Permissions granted to groups apply to all members

## Watchers and Notifications

### Watchers

Users can watch spaces or pages to receive updates:

- **watcher_id**: Unique watcher record
- **user_id**: User watching the content
- **space_id** or **page_id**: Content being watched
- **created_at**: When watching started

### Notifications

Notifications inform users of events:

- **notification_type**: Type of event (mention, comment, page_update, approval, export, space_change)
- **is_read**: Whether user has seen the notification
- **related_page_id** / **related_space_id**: Context for the notification

Common notification triggers:

- Page updates on watched content
- Mentions in content or comments
- Approval workflow changes
- Export job completion
- Space configuration changes

## Approval Workflows

### Approval Requests

Content can require approval before publishing:

- **request_id**: Unique approval request
- **page_id**: Page requiring approval
- **requester_user_id**: User requesting approval
- **approver_user_id**: User responsible for approval
- **approval_status**: Current status (pending, approved, rejected, cancelled)

### Approval Decisions

Approvers make decisions on requests:

- **decision_type**: Type of decision (approve, reject, request_changes)
- **decision_comment**: Explanation for the decision
- **decided_at**: Timestamp of decision

## Space Features

Spaces can have various features enabled:

- **page_templates**: Pre-defined page layouts
- **attachments**: File upload capability
- **comments**: Comment functionality
- **analytics**: Usage analytics
- **api_access**: API integration
- **automation**: Automated workflows
- **custom_theme**: Custom visual themes

Features are tracked in the space_features table with:

- **space_id**: Space the feature belongs to
- **feature_type**: Type of feature enabled
- **enabled**: Whether feature is active

## Space Memberships

Space memberships track user participation:

- **space_id**: The space
- **user_id**: The member
- **role**: Role within space (admin, contributor, viewer)
- **joined_at**: Membership start date

## Audit Logging

All significant actions are logged for compliance:

- **audit_log_id**: Unique log entry
- **user_id**: User who performed the action
- **action_type**: Type of action performed
- **resource_id**: ID of affected resource
- **resource_type**: Type of resource (space, page, user, etc.)
- **details**: Additional context as JSON
- **timestamp**: When action occurred

### Audit Action Types

Comprehensive action tracking includes:

- create, update, delete operations
- view, export operations
- permission_change, space_config_change
- user_login, user_logout
- approval, rejection
- comment_added, attachment_added
- page_published, page_archived, page_restored
- watcher_added, watcher_removed
- And more...

## Export Operations

Users can export content in various formats:

- **export_job_id**: Unique job identifier
- **export_format**: Output format (pdf, html, markdown, xml)
- **page_id** or **space_id**: Content to export
- **export_job_status**: Job state (queued, in_progress, completed, failed)
- **requested_by_user_id**: User who requested export
- **export_url**: Download link when completed

## Space Configuration History

Changes to space configuration are tracked:

- **config_id**: Unique configuration record
- **space_id**: Space being configured
- **changed_by_user_id**: User making the change
- **config_key**: Setting being changed
- **old_value** / **new_value**: Before and after values
- **changed_at**: Timestamp of change

## Data Structures

### Database Tables

The environment maintains the following data tables:

1. **users.json**: User accounts and profiles
2. **groups.json**: User groups
3. **user_groups.json**: User-group memberships
4. **spaces.json**: Space definitions
5. **pages.json**: Page metadata
6. **page_versions.json**: Version history
7. **permissions.json**: Access control rules
8. **watchers.json**: Watch subscriptions
9. **space_features.json**: Enabled features
10. **space_config_history.json**: Configuration change log
11. **space_memberships.json**: Space membership records
12. **notifications.json**: User notifications
13. **approval_requests.json**: Approval workflows
14. **approval_decisions.json**: Approval outcomes
15. **audit_logs.json**: Audit trail
16. **export_jobs.json**: Export operations

### Timestamp Format

All timestamps use ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

- Example: "2025-10-01T12:00:00"
- Tools use static timestamp for consistency

## Tool Interfaces

The environment provides 5 different tool interfaces for benchmarking. Each interface provides the same functionality with different naming conventions:

### Interface 1: manage*\* / get*\*

- manage_user, manage_space, manage_page, etc.
- get_user, get_space, get_page, etc.
- record_audit_log
- transfer_to_human

### Interface 2: set*\* / fetch*\*

- set_user, set_space, set_page, etc.
- fetch_user, fetch_space, fetch_page, etc.
- create_new_audit_trail
- switch_to_human

### Interface 3: manipulate*\* / retrieve*\*

- manipulate_user, manipulate_space, manipulate_page, etc.
- retrieve_user, retrieve_space, retrieve_page, etc.
- register_new_audit_trail
- escalate_to_human

### Interface 4: address*\* / lookup*\*

- address_user, address_space, address_page, etc.
- lookup_user, lookup_space, lookup_page, etc.
- record_new_audit_trail
- handover_to_human

### Interface 5: process*\* / get*\*

- process_user, process_space, process_page, etc.
- get_user, get_space, get_page, etc.
- generate_new_audit_trail
- route_to_human

## Common Operations

### Creating a New Space

1. Choose unique space_key
2. Set space_name and space_purpose
3. Assign created_by_user_id
4. Set created_at timestamp
5. Initialize is_deleted = false

### Creating a Page

1. Select parent space_id
2. Optionally set parent_page_id for hierarchy
3. Set title and content_format
4. Initialize current_version = 1
5. Set state (typically 'draft')
6. Set created_by_user_id and created_at

### Updating a Page

1. Increment current_version
2. Create new page_version record
3. Update updated_by_user_id and updated_at
4. Optionally change state
5. Log audit_action

### Granting Permissions

1. Validate user/group exists
2. Validate space/page exists
3. Set permission_type
4. Optionally set grant_type (direct/inherited)
5. Record in permissions table

### Managing Approvals

1. Create approval_request
2. Set requester and approver
3. Set approval_status = 'pending'
4. Approver creates approval_decision
5. Update request status based on decision
6. Notify requester of outcome

## Best Practices

### Security

- Always validate user permissions before operations
- Check user roles and specific permissions
- Log security-relevant actions
- Never expose sensitive data unnecessarily

### Data Integrity

- Validate all foreign key relationships
- Check for deleted/trashed content
- Maintain version history
- Use transactions for multi-step operations

### User Experience

- Provide clear error messages
- Send appropriate notifications
- Respect user watch preferences
- Support content discovery through hierarchy

### Performance

- Use pagination for large result sets
- Cache frequently accessed data
- Optimize permission checks
- Index key lookup fields

### Compliance

- Log all significant actions
- Maintain audit trail
- Support export for data portability
- Respect privacy settings

## Error Handling

Common error scenarios:

- **Invalid user_id**: User does not exist
- **Invalid space_id**: Space not found or deleted
- **Invalid page_id**: Page not found or trashed
- **Permission denied**: User lacks required permissions
- **Invalid state transition**: Cannot change to requested state
- **Missing required field**: Required parameter not provided
- **Duplicate key**: Unique constraint violation
- **Invalid reference**: Foreign key constraint violation

## Escalation to Human

Use human escalation tools when:

- User explicitly requests human assistance
- Operation requires judgment beyond system capabilities
- Complex permission conflicts arise
- Ambiguous user intent needs clarification
- Policy exceptions require approval
- Technical issues prevent operation completion
