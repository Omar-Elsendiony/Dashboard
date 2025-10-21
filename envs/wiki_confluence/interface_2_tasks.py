from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Joshua Walker, a Global Administrator at joshua.walker@siemens.com. "
            "You need to configure a new marketing space. "
            "Create a space called 'MKTG', enable analytics and automation features, "
            "add Jill Rhodes (user_id: 3) as a contributor, and create an audit trail."
        ),
        actions=[
            Action(name="fetch_user", kwargs={
                "user_id": "2"
            }),
            Action(name="set_space", kwargs={
                "action": "create",
                "space_data": {
                    "space_key": "MKTG",
                    "space_name": "MKTG - Marketing Operations",
                    "space_purpose": "Marketing campaigns, strategies, and analytics",
                    "created_by_user_id": "2"
                }
            }),
            Action(name="set_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "analytics"
            }),
            Action(name="set_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "automation"
            }),
            Action(name="set_space_memberships", kwargs={
                "action": "add",
                "membership_data": {
                    "space_id": "1",
                    "user_id": "3",
                    "role": "contributor"
                }
            }),
            Action(name="create_new_audit_trail", kwargs={
                "user_id": "2",
                "action_type": "space_created",
                "resource_type": "space",
                "resource_id": "1",
                "details": {"space_key": "MKTG", "purpose": "marketing operations"}
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="9",
        instruction=(
            "You are Jeffrey Lawrence, a Space Administrator at jeffrey.lawrence@gmail.com. "
            "You need to create a troubleshooting guide page in space_id: 1. "
            "Create the page, add detailed content via a version, publish it, "
            "and set up watchers for Lisa Smith (user_id: 10) and Linda Wolfe (user_id: 11)."
        ),
        actions=[
            Action(name="fetch_space", kwargs={
                "space_id": "1"
            }),
            Action(name="set_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "1",
                    "title": "Troubleshooting Common Issues",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "9"
                }
            }),
            Action(name="set_page_version", kwargs={
                "page_id": "1",
                "content": "# Troubleshooting Guide\\n\\n## Connection Issues\\n1. Check network connectivity\\n2. Verify credentials\\n3. Review firewall settings\\n\\n## Performance Problems\\n1. Monitor resource usage\\n2. Check database queries\\n3. Review application logs\\n\\n## Common Errors\\n### Error 500\\n- Check server logs\\n- Verify configuration\\n- Restart services if needed",
                "change_comment": "Initial troubleshooting documentation",
                "created_by_user_id": "9"
            }),
            Action(name="set_page", kwargs={
                "action": "update",
                "page_id": "1",
                "page_data": {
                    "state": "published",
                    "updated_by_user_id": "9"
                }
            }),
            Action(name="set_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "10",
                    "page_id": "1"
                }
            }),
            Action(name="set_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "11",
                    "page_id": "1"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="3",
        user_id="32",
        instruction=(
            "You are Angela Cohen, a Space Member at angela.cohen@company.com. "
            "You've been asked to update page_id: 3 with new architecture changes. "
            "Fetch the current page, create a new version with updated content, "
            "add yourself as a watcher, and submit an approval request to user_id: 13."
        ),
        actions=[
            Action(name="fetch_page", kwargs={
                "page_id": "3"
            }),
            Action(name="fetch_page_versions", kwargs={
                "page_id": "3"
            }),
            Action(name="set_page_version", kwargs={
                "page_id": "3",
                "content": "# Architecture Overview - Updated\\n\\n## New Microservices Architecture\\n\\n### Service Mesh\\n- Istio for service-to-service communication\\n- mTLS encryption\\n- Traffic management\\n\\n### API Gateway\\n- Kong Gateway\\n- Rate limiting\\n- Authentication\\n\\n### Data Layer\\n- PostgreSQL (primary database)\\n- MongoDB (document store)\\n- Redis (caching and session management)\\n\\n### Observability\\n- Prometheus for metrics\\n- Grafana for dashboards\\n- Jaeger for distributed tracing\\n- ELK stack for logging",
                "change_comment": "Major update: Added service mesh, updated data layer, added observability section",
                "created_by_user_id": "32"
            }),
            Action(name="set_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "32",
                    "page_id": "3"
                }
            }),
            Action(name="set_approval_request", kwargs={
                "page_id": "3",
                "requester_user_id": "32",
                "approver_user_id": "13"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="4",
        user_id="13",
        instruction=(
            "You are Susan Rogers, a Space Administrator at susan.rogers@siemens.com. "
            "You have pending approval requests to review. "
            "Check your approvals, review the page history, approve with feedback, "
            "and notify the requester of the approval."
        ),
        actions=[
            Action(name="fetch_approval_requests", kwargs={
                "filter": "pending",
                "approver_user_id": "13"
            }),
            Action(name="fetch_page_versions", kwargs={
                "page_id": "3"
            }),
            Action(name="set_approval_decision", kwargs={
                "request_id": "1",
                "decision_type": "approve",
                "decision_comment": "Great improvements to the architecture documentation. The new observability section is particularly valuable."
            }),
            Action(name="set_notification", kwargs={
                "user_id": "32",
                "notification_type": "approval",
                "message": "Your architecture updates have been approved. Excellent work on the service mesh documentation!",
                "related_page_id": "3"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="5",
        user_id="182",
        instruction=(
            "You are Catherine Dixon, a Content Contributor at catherine.dixon@company.com. "
            "You need to export pages from space_id: 2 in HTML format for review. "
            "Create the export, check your notifications, and log the activity."
        ),
        actions=[
            Action(name="set_exports", kwargs={
                "action": "create",
                "export_data": {
                    "space_id": "2",
                    "export_format": "html",
                    "requested_by_user_id": "182"
                }
            }),
            Action(name="fetch_exports", kwargs={
                "filter": "user",
                "user_id": "182"
            }),
            Action(name="fetch_notifications", kwargs={
                "user_id": "182",
                "filter": "unread"
            }),
            Action(name="create_new_audit_trail", kwargs={
                "user_id": "182",
                "action_type": "export_requested",
                "resource_type": "space",
                "resource_id": "2",
                "details": {"format": "html", "space_key": "ENG"}
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="6",
        user_id="15",
        instruction=(
            "You are Melanie Munoz, a Space Administrator at melanie.munoz@gmail.com. "
            "You need to set up permissions for a new project team. "
            "Create a group called 'Project Alpha Team', add members (user_ids: 33, 34, 35), "
            "and grant them comment and view permissions on space_id: 3."
        ),
        actions=[
            Action(name="set_groups", kwargs={
                "action": "create",
                "group_data": {
                    "group_name": "Project Alpha Team",
                    "description": "Team members working on Project Alpha"
                }
            }),
            Action(name="set_user_groups", kwargs={
                "action": "add",
                "user_group_data": {
                    "user_id": "33",
                    "group_id": "1"
                }
            }),
            Action(name="set_user_groups", kwargs={
                "action": "add",
                "user_group_data": {
                    "user_id": "34",
                    "group_id": "1"
                }
            }),
            Action(name="set_user_groups", kwargs={
                "action": "add",
                "user_group_data": {
                    "user_id": "35",
                    "group_id": "1"
                }
            }),
            Action(name="set_permissions", kwargs={
                "action": "grant",
                "permission_data": {
                    "target_type": "space",
                    "target_id": "3",
                    "group_id": "1",
                    "permission_type": "comment"
                }
            }),
            Action(name="set_permissions", kwargs={
                "action": "grant",
                "permission_data": {
                    "target_type": "space",
                    "target_id": "3",
                    "group_id": "1",
                    "permission_type": "view"
                }
            })
        ],
        outputs=[]
    )
]
