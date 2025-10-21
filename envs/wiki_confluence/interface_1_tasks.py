from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="1",
        user_id="1",
        instruction=(
            "You are Danielle Johnson, a Global Administrator at danielle.johnson@outlook.com. "
            "You need to set up a new wiki space for the engineering team. "
            "First, check your user profile, create a new space called 'DEVOPS', "
            "enable page templates and comments features, and add Joshua Walker (user_id: 2) as a space admin."
        ),
        actions=[
            Action(name="get_user", kwargs={
                "user_id": "1"
            }),
            Action(name="manage_space", kwargs={
                "action": "create",
                "space_data": {
                    "space_key": "DEVOPS",
                    "space_name": "DEVOPS - DevOps Documentation",
                    "space_purpose": "DevOps processes and infrastructure documentation",
                    "created_by_user_id": "1"
                }
            }),
            Action(name="manage_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "page_templates"
            }),
            Action(name="manage_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "comments"
            }),
            Action(name="manage_space_memberships", kwargs={
                "action": "add",
                "membership_data": {
                    "space_id": "1",
                    "user_id": "2",
                    "role": "admin"
                }
            }),
            Action(name="record_audit_log", kwargs={
                "user_id": "1",
                "action_type": "space_created",
                "resource_type": "space",
                "resource_id": "1",
                "details": {"space_key": "DEVOPS", "space_name": "DEVOPS - DevOps Documentation"}
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="6",
        instruction=(
            "You are Jeffery Wagner, a Space Administrator at jeffery.wagner@techcorp.com. "
            "You need to manage content in the PROD space (space_id: 1). "
            "Create a new page about 'Monitoring and Alerts', add content to it through a page version, "
            "set it as published, and grant edit permissions to Veronica Bowman (user_id: 31)."
        ),
        actions=[
            Action(name="get_space", kwargs={
                "space_id": "1"
            }),
            Action(name="manage_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "1",
                    "title": "Monitoring Best Practices",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "6"
                }
            }),
            Action(name="create_page_version", kwargs={
                "page_id": "1",
                "content": "# Monitoring Best Practices\\n\\n## Overview\\nThis guide covers monitoring and alerting best practices for our production systems.\\n\\n## Key Metrics\\n- CPU utilization\\n- Memory usage\\n- Disk I/O\\n- Network throughput",
                "change_comment": "Initial monitoring documentation",
                "created_by_user_id": "6"
            }),
            Action(name="manage_page", kwargs={
                "action": "update",
                "page_id": "1",
                "page_data": {
                    "state": "published",
                    "updated_by_user_id": "6"
                }
            }),
            Action(name="manage_permissions", kwargs={
                "action": "grant",
                "permission_data": {
                    "target_type": "page",
                    "target_id": "1",
                    "user_id": "31",
                    "permission_type": "edit"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="3",
        user_id="31",
        instruction=(
            "You are Veronica Bowman, a Space Member at veronica.bowman@siemens.com. "
            "You've been asked to update the 'Architecture Overview' page (page_id: 3). "
            "First, check the page details, update it with new content, create a new version, "
            "add yourself as a watcher, and request approval from Anthony Gonzalez (user_id: 7)."
        ),
        actions=[
            Action(name="get_page", kwargs={
                "page_id": "3"
            }),
            Action(name="get_page_versions", kwargs={
                "page_id": "3"
            }),
            Action(name="create_page_version", kwargs={
                "page_id": "3",
                "content": "# Architecture Overview\\n\\n## System Architecture\\nOur system follows a microservices architecture with the following components:\\n\\n### Frontend\\n- React-based web application\\n- Mobile app (iOS and Android)\\n\\n### Backend Services\\n- Authentication Service\\n- API Gateway\\n- Data Processing Pipeline\\n- Analytics Engine\\n\\n### Infrastructure\\n- Kubernetes clusters\\n- PostgreSQL database\\n- Redis cache\\n- S3 storage",
                "change_comment": "Added detailed architecture breakdown with frontend, backend, and infrastructure sections",
                "created_by_user_id": "31"
            }),
            Action(name="manage_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "31",
                    "page_id": "3"
                }
            }),
            Action(name="create_approval_request", kwargs={
                "page_id": "3",
                "requester_user_id": "31",
                "approver_user_id": "7"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="4",
        user_id="7",
        instruction=(
            "You are Anthony Gonzalez, a Space Administrator at anthony.gonzalez@techcorp.com. "
            "You have a pending approval request for a page update. "
            "Check your pending approval requests, review the page version history, "
            "approve the request with a positive comment, and notify the requester."
        ),
        actions=[
            Action(name="get_approval_requests", kwargs={
                "filter": "pending",
                "approver_user_id": "7"
            }),
            Action(name="get_page_versions", kwargs={
                "page_id": "3"
            }),
            Action(name="decide_approval", kwargs={
                "request_id": "1",
                "decision_type": "approve",
                "decision_comment": "Excellent work on the architecture documentation. The breakdown is clear and comprehensive. Approved!"
            }),
            Action(name="send_notification", kwargs={
                "user_id": "31",
                "notification_type": "approval",
                "message": "Your updates to 'Architecture Overview' have been approved. Great job on the detailed documentation!",
                "related_page_id": "3"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="5",
        user_id="181",
        instruction=(
            "You are Jessica Edwards, a Content Contributor at jessica.edwards@techcorp.com. "
            "You need to export the PROD space (space_id: 1) documentation for offline review. "
            "Create an export job in PDF format, check the status of your recent exports, "
            "and review your notification history to see recent updates."
        ),
        actions=[
            Action(name="manage_exports", kwargs={
                "action": "create",
                "export_data": {
                    "space_id": "1",
                    "export_format": "pdf",
                    "requested_by_user_id": "181"
                }
            }),
            Action(name="get_exports", kwargs={
                "filter": "user",
                "user_id": "181"
            }),
            Action(name="get_notifications", kwargs={
                "user_id": "181",
                "filter": "unread"
            }),
            Action(name="record_audit_log", kwargs={
                "user_id": "181",
                "action_type": "export_requested",
                "resource_type": "space",
                "resource_id": "1",
                "details": {"format": "pdf", "space_name": "PROD"}
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="6",
        user_id="8",
        instruction=(
            "You are Debra Gardner, a Space Administrator at debra.gardner@gmail.com. "
            "You need to investigate recent activities in the API space (space_id: 5). "
            "First, get the space details, check the audit logs for recent changes, "
            "review the space configuration history, and identify who has been active."
        ),
        actions=[
            Action(name="get_space", kwargs={
                "space_id": "5"
            }),
            Action(name="get_audit_logs", kwargs={
                "filter": "space",
                "resource_id": "5",
                "resource_type": "space",
                "limit": 20
            }),
            Action(name="get_space_config_history", kwargs={
                "space_id": "5"
            }),
            Action(name="get_space_memberships", kwargs={
                "space_id": "5"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="7",
        user_id="12",
        instruction=(
            "You are Matthew Moore, a Space Administrator at matthew.moore@company.com. "
            "You need to reorganize pages in the PROJ space (space_id: 3). "
            "Get all pages in the space, create a parent page called 'Project Documentation Index', "
            "then create three child pages: 'Requirements', 'Design', and 'Testing'. "
            "Finally, grant view permissions to the entire space to Angela Cohen (user_id: 32)."
        ),
        actions=[
            Action(name="get_pages", kwargs={
                "space_id": "3"
            }),
            Action(name="manage_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "3",
                    "title": "Project Documentation Index",
                    "content_format": "markdown",
                    "state": "published",
                    "created_by_user_id": "12"
                }
            }),
            Action(name="manage_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "3",
                    "parent_page_id": "1",
                    "title": "Requirements",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "12"
                }
            }),
            Action(name="manage_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "3",
                    "parent_page_id": "1",
                    "title": "Design",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "12"
                }
            }),
            Action(name="manage_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "3",
                    "parent_page_id": "1",
                    "title": "Testing",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "12"
                }
            }),
            Action(name="manage_permissions", kwargs={
                "action": "grant",
                "permission_data": {
                    "target_type": "space",
                    "target_id": "3",
                    "user_id": "32",
                    "permission_type": "view"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="8",
        user_id="14",
        instruction=(
            "You are Christopher Davis, a Space Administrator at christopher.davis@techcorp.com. "
            "You need to manage user groups and permissions for the ENG space (space_id: 2). "
            "Create a user group called 'Engineering Team', add three members to it "
            "(Leslie Adams user_id: 35, Jason Hahn user_id: 36, Nancy Edwards user_id: 37), "
            "and grant the group edit permissions on the space."
        ),
        actions=[
            Action(name="manage_groups", kwargs={
                "action": "create",
                "group_data": {
                    "group_name": "Engineering Team",
                    "description": "Core engineering team members with edit access"
                }
            }),
            Action(name="manage_user_groups", kwargs={
                "action": "add",
                "user_group_data": {
                    "user_id": "35",
                    "group_id": "1"
                }
            }),
            Action(name="manage_user_groups", kwargs={
                "action": "add",
                "user_group_data": {
                    "user_id": "36",
                    "group_id": "1"
                }
            }),
            Action(name="manage_user_groups", kwargs={
                "action": "add",
                "user_group_data": {
                    "user_id": "37",
                    "group_id": "1"
                }
            }),
            Action(name="manage_permissions", kwargs={
                "action": "grant",
                "permission_data": {
                    "target_type": "space",
                    "target_id": "2",
                    "group_id": "1",
                    "permission_type": "edit"
                }
            })
        ],
        outputs=[]
    )
]
