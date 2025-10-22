from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="1",
        user_id="4",
        instruction=(
            "You are Patricia Miller, a Global Administrator at patricia.miller@gmail.com. "
            "You need to set up a support knowledge base space. "
            "Create a space called 'SUPPORT', enable attachments and comments, "
            "add Nicholas Arnold (user_id: 18) as contributor, and record audit trail."
        ),
        actions=[
            Action(name="lookup_user", kwargs={
                "user_id": "4"
            }),
            Action(name="address_space", kwargs={
                "action": "create",
                "space_data": {
                    "space_key": "SUPPORT",
                    "space_name": "SUPPORT - Customer Support Knowledge Base",
                    "space_purpose": "Support articles, FAQs, and troubleshooting guides",
                    "created_by_user_id": "4"
                }
            }),
            Action(name="address_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "attachments"
            }),
            Action(name="address_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "comments"
            }),
            Action(name="address_space_memberships", kwargs={
                "action": "add",
                "membership_data": {
                    "space_id": "1",
                    "user_id": "18",
                    "role": "contributor"
                }
            }),
            Action(name="record_new_audit_trail", kwargs={
                "user_id": "4",
                "action_type": "space_created",
                "resource_type": "space",
                "resource_id": "1",
                "details": {"space_key": "SUPPORT", "purpose": "customer support knowledge base"}
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="18",
        instruction=(
            "You are Nicholas Arnold, a Space Administrator at nicholas.arnold@gmail.com. "
            "You need to create FAQ documentation in space_id: 1. "
            "Create a FAQ page, add detailed Q&A content, publish it, "
            "and set up watchers for Maria Montgomery (user_id: 19) and Michelle Ray (user_id: 20)."
        ),
        actions=[
            Action(name="lookup_space", kwargs={
                "space_id": "1"
            }),
            Action(name="address_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "1",
                    "title": "Frequently Asked Questions",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "18"
                }
            }),
            Action(name="address_page_version", kwargs={
                "page_id": "1",
                "content": "# Frequently Asked Questions\\n\\n## Account & Login\\n\\n### How do I reset my password?\\nClick 'Forgot Password' on the login page and follow the email instructions.\\n\\n### How do I update my email address?\\nGo to Profile Settings > Contact Information > Update Email.\\n\\n## Features\\n\\n### How do I create a new space?\\nNavigate to Spaces > Create Space, then fill in the required details.\\n\\n### How do I share a page?\\nOpen the page, click Share, and enter user emails or select from the list.\\n\\n## Permissions\\n\\n### Who can edit my pages?\\nUsers with edit permissions on the page or space can make changes.\\n\\n### How do I restrict access?\\nUse the Permissions menu to set view, edit, or admin access levels.\\n\\n## Technical Issues\\n\\n### The page won't load. What should I do?\\nTry refreshing, clearing cache, or contacting support if the issue persists.",
                "change_comment": "Comprehensive FAQ covering account, features, permissions, and technical issues",
                "created_by_user_id": "18"
            }),
            Action(name="address_page", kwargs={
                "action": "update",
                "page_id": "1",
                "page_data": {
                    "state": "published",
                    "updated_by_user_id": "18"
                }
            }),
            Action(name="address_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "19",
                    "page_id": "1"
                }
            }),
            Action(name="address_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "20",
                    "page_id": "1"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="3",
        user_id="38",
        instruction=(
            "You are Diana Foster, a Space Member at diana.foster@techcorp.com. "
            "You need to update deployment procedures on page_id: 2. "
            "Look up the page, create a new version with deployment steps, "
            "watch it, and request approval from user_id: 19."
        ),
        actions=[
            Action(name="lookup_page", kwargs={
                "page_id": "2"
            }),
            Action(name="lookup_page_versions", kwargs={
                "page_id": "2"
            }),
            Action(name="address_page_version", kwargs={
                "page_id": "2",
                "content": "# Deployment Procedures\\n\\n## Pre-Deployment Checklist\\n- [ ] Code review completed\\n- [ ] All tests passing\\n- [ ] Staging environment validated\\n- [ ] Rollback plan prepared\\n- [ ] Stakeholders notified\\n\\n## Deployment Steps\\n\\n### 1. Prepare Release\\n```bash\\ngit checkout main\\ngit pull origin main\\ngit tag -a v1.2.3 -m 'Release v1.2.3'\\ngit push origin v1.2.3\\n```\\n\\n### 2. Build and Test\\n```bash\\nnpm run build\\nnpm run test:prod\\n```\\n\\n### 3. Deploy to Staging\\n```bash\\n./scripts/deploy.sh staging\\n```\\n\\n### 4. Smoke Tests\\nRun automated smoke tests on staging environment.\\n\\n### 5. Deploy to Production\\n```bash\\n./scripts/deploy.sh production\\n```\\n\\n### 6. Post-Deployment Validation\\n- Verify critical paths\\n- Monitor error rates\\n- Check performance metrics\\n\\n## Rollback Procedure\\nIf issues are detected:\\n```bash\\n./scripts/rollback.sh v1.2.2\\n```",
                "change_comment": "Added comprehensive deployment procedures with pre-deployment checklist, step-by-step deployment, and rollback procedures",
                "created_by_user_id": "38"
            }),
            Action(name="address_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "38",
                    "page_id": "2"
                }
            }),
            Action(name="address_approval_request", kwargs={
                "page_id": "2",
                "requester_user_id": "38",
                "approver_user_id": "19"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="4",
        user_id="19",
        instruction=(
            "You are Maria Montgomery, a Space Administrator at maria.montgomery@techcorp.com. "
            "Review and approve deployment procedure updates. "
            "Check pending approvals, review versions, approve, and notify the contributor."
        ),
        actions=[
            Action(name="lookup_approval_requests", kwargs={
                "filter": "pending",
                "approver_user_id": "19"
            }),
            Action(name="lookup_page_versions", kwargs={
                "page_id": "2"
            }),
            Action(name="address_approval_decision", kwargs={
                "request_id": "1",
                "decision_type": "approve",
                "decision_comment": "Deployment procedures are detailed and include proper rollback steps. Approved."
            }),
            Action(name="address_notification", kwargs={
                "user_id": "38",
                "notification_type": "approval",
                "message": "Your deployment procedures update has been approved. Great work on including the rollback procedures!",
                "related_page_id": "2"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="5",
        user_id="184",
        instruction=(
            "You are Jonathan Fletcher, a Content Contributor at jonathan.fletcher@siemens.com. "
            "Export space_id: 5 documentation in XML format. "
            "Create export, check status, review notifications, and record audit."
        ),
        actions=[
            Action(name="address_exports", kwargs={
                "action": "create",
                "export_data": {
                    "space_id": "5",
                    "export_format": "xml",
                    "requested_by_user_id": "184"
                }
            }),
            Action(name="lookup_exports", kwargs={
                "filter": "user",
                "user_id": "184"
            }),
            Action(name="lookup_notifications", kwargs={
                "user_id": "184",
                "filter": "unread"
            }),
            Action(name="record_new_audit_trail", kwargs={
                "user_id": "184",
                "action_type": "export_requested",
                "resource_type": "space",
                "resource_id": "5",
                "details": {"format": "xml", "space_key": "API"}
            })
        ],
        outputs=[]
    )
]
