from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="1",
        user_id="3",
        instruction=(
            "You are Jill Rhodes, a Global Administrator at jill.rhodes@company.com. "
            "You need to set up a research space. "
            "Create a space called 'RESEARCH', enable API access and custom theme features, "
            "add Patricia Miller (user_id: 4) as admin, and register the audit trail."
        ),
        actions=[
            Action(name="retrieve_user", kwargs={
                "user_id": "3"
            }),
            Action(name="manipulate_space", kwargs={
                "action": "create",
                "space_data": {
                    "space_key": "RESEARCH",
                    "space_name": "RESEARCH - Research and Development",
                    "space_purpose": "Research findings, experiments, and analysis",
                    "created_by_user_id": "3"
                }
            }),
            Action(name="manipulate_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "api_access"
            }),
            Action(name="manipulate_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "custom_theme"
            }),
            Action(name="manipulate_space_memberships", kwargs={
                "action": "add",
                "membership_data": {
                    "space_id": "1",
                    "user_id": "4",
                    "role": "admin"
                }
            }),
            Action(name="register_new_audit_trail", kwargs={
                "user_id": "3",
                "action_type": "space_created",
                "resource_type": "space",
                "resource_id": "1",
                "details": {"space_key": "RESEARCH", "features": ["api_access", "custom_theme"]}
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="16",
        instruction=(
            "You are Lindsay Blair, a Space Administrator at lindsay.blair@siemens.com. "
            "You need to document API endpoints in space_id: 5. "
            "Create a page about REST API documentation, add comprehensive content, "
            "publish it, and set up watchers for Robert Johnson (user_id: 5) and Jeffery Wagner (user_id: 6)."
        ),
        actions=[
            Action(name="retrieve_space", kwargs={
                "space_id": "5"
            }),
            Action(name="manipulate_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "5",
                    "title": "REST API Documentation",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "16"
                }
            }),
            Action(name="manipulate_page_version", kwargs={
                "page_id": "1",
                "content": "# REST API Documentation\\n\\n## Authentication\\nAll API requests require Bearer token authentication.\\n\\n## Endpoints\\n\\n### Users\\n- GET /api/v1/users - List all users\\n- GET /api/v1/users/{id} - Get user details\\n- POST /api/v1/users - Create new user\\n- PUT /api/v1/users/{id} - Update user\\n- DELETE /api/v1/users/{id} - Delete user\\n\\n### Spaces\\n- GET /api/v1/spaces - List all spaces\\n- GET /api/v1/spaces/{id} - Get space details\\n- POST /api/v1/spaces - Create new space\\n\\n### Pages\\n- GET /api/v1/pages - List pages\\n- GET /api/v1/pages/{id} - Get page content\\n- POST /api/v1/pages - Create page\\n- PUT /api/v1/pages/{id} - Update page",
                "change_comment": "Initial API documentation with authentication and CRUD endpoints",
                "created_by_user_id": "16"
            }),
            Action(name="manipulate_page", kwargs={
                "action": "update",
                "page_id": "1",
                "page_data": {
                    "state": "published",
                    "updated_by_user_id": "16"
                }
            }),
            Action(name="manipulate_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "5",
                    "page_id": "1"
                }
            }),
            Action(name="manipulate_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "6",
                    "page_id": "1"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="3",
        user_id="37",
        instruction=(
            "You are Nancy Edwards, a Space Member at nancy.edwards@gmail.com. "
            "You need to update security guidelines on page_id: 4. "
            "Retrieve the page, create a new version with enhanced security content, "
            "watch the page, and request approval from user_id: 17."
        ),
        actions=[
            Action(name="retrieve_page", kwargs={
                "page_id": "4"
            }),
            Action(name="retrieve_page_versions", kwargs={
                "page_id": "4"
            }),
            Action(name="manipulate_page_version", kwargs={
                "page_id": "4",
                "content": "# Security Guidelines\\n\\n## Access Control\\n- Implement role-based access control (RBAC)\\n- Use principle of least privilege\\n- Regular access reviews\\n\\n## Authentication\\n- Multi-factor authentication (MFA) required\\n- Strong password policies\\n- Session timeout after 30 minutes\\n\\n## Data Protection\\n- Encrypt data at rest and in transit\\n- Regular backups\\n- Data retention policies\\n\\n## Incident Response\\n- Security incident reporting process\\n- Escalation procedures\\n- Post-incident reviews\\n\\n## Compliance\\n- GDPR compliance requirements\\n- SOC 2 Type II certification\\n- Annual security audits",
                "change_comment": "Enhanced security guidelines with access control, authentication, data protection, incident response, and compliance sections",
                "created_by_user_id": "37"
            }),
            Action(name="manipulate_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "37",
                    "page_id": "4"
                }
            }),
            Action(name="manipulate_approval_request", kwargs={
                "page_id": "4",
                "requester_user_id": "37",
                "approver_user_id": "17"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="4",
        user_id="17",
        instruction=(
            "You are Amanda Dudley, a Space Administrator at amanda.dudley@outlook.com. "
            "Review and approve pending security guideline updates. "
            "Check pending approvals, review versions, approve, and notify the contributor."
        ),
        actions=[
            Action(name="retrieve_approval_requests", kwargs={
                "filter": "pending",
                "approver_user_id": "17"
            }),
            Action(name="retrieve_page_versions", kwargs={
                "page_id": "4"
            }),
            Action(name="manipulate_approval_decision", kwargs={
                "request_id": "1",
                "decision_type": "approve",
                "decision_comment": "Security guidelines are comprehensive and well-structured. Approved for publication."
            }),
            Action(name="manipulate_notification", kwargs={
                "user_id": "37",
                "notification_type": "approval",
                "message": "Your security guidelines update has been approved. Thank you for the thorough documentation!",
                "related_page_id": "4"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="5",
        user_id="183",
        instruction=(
            "You are Paul Ray, a Content Contributor at paul.ray@outlook.com. "
            "Export documentation from space_id: 3 in markdown format. "
            "Create export, check status, review notifications, and register audit trail."
        ),
        actions=[
            Action(name="manipulate_exports", kwargs={
                "action": "create",
                "export_data": {
                    "space_id": "3",
                    "export_format": "markdown",
                    "requested_by_user_id": "183"
                }
            }),
            Action(name="retrieve_exports", kwargs={
                "filter": "user",
                "user_id": "183"
            }),
            Action(name="retrieve_notifications", kwargs={
                "user_id": "183",
                "filter": "unread"
            }),
            Action(name="register_new_audit_trail", kwargs={
                "user_id": "183",
                "action_type": "export_requested",
                "resource_type": "space",
                "resource_id": "3",
                "details": {"format": "markdown", "space_key": "PROJ"}
            })
        ],
        outputs=[]
    )
]
