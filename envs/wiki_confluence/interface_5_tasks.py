from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="1",
        user_id="5",
        instruction=(
            "You are Robert Johnson, a Global Administrator at robert.johnson@techcorp.com. "
            "You need to set up a training and onboarding space. "
            "Create a space called 'TRAINING', enable page templates and analytics, "
            "add Janet Williams (user_id: 21) as admin, and generate audit trail."
        ),
        actions=[
            Action(name="get_user", kwargs={
                "user_id": "5"
            }),
            Action(name="process_space", kwargs={
                "action": "create",
                "space_data": {
                    "space_key": "TRAINING",
                    "space_name": "TRAINING - Employee Training and Onboarding",
                    "space_purpose": "Training materials, onboarding guides, and learning resources",
                    "created_by_user_id": "5"
                }
            }),
            Action(name="process_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "page_templates"
            }),
            Action(name="process_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "analytics"
            }),
            Action(name="process_space_memberships", kwargs={
                "action": "add",
                "membership_data": {
                    "space_id": "1",
                    "user_id": "21",
                    "role": "admin"
                }
            }),
            Action(name="generate_new_audit_trail", kwargs={
                "user_id": "5",
                "action_type": "space_created",
                "resource_type": "space",
                "resource_id": "1",
                "details": {"space_key": "TRAINING", "purpose": "employee training and onboarding"}
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="21",
        instruction=(
            "You are Janet Williams, a Space Administrator at janet.williams@outlook.com. "
            "You need to create onboarding documentation in space_id: 1. "
            "Create an onboarding page, add comprehensive content, publish it, "
            "and set up watchers for Jeremy Roberts (user_id: 22) and Christopher Hall (user_id: 23)."
        ),
        actions=[
            Action(name="get_space", kwargs={
                "space_id": "1"
            }),
            Action(name="process_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "1",
                    "title": "New Employee Onboarding Guide",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "21"
                }
            }),
            Action(name="process_page_version", kwargs={
                "page_id": "1",
                "content": "# New Employee Onboarding Guide\\n\\n## Welcome!\\nWelcome to our team! This guide will help you get started.\\n\\n## First Week\\n\\n### Day 1\\n- Meet your manager and team\\n- Complete HR paperwork\\n- Set up workstation and accounts\\n- Review company policies\\n\\n### Day 2-3\\n- Shadow team members\\n- Review project documentation\\n- Attend orientation sessions\\n- Set up development environment\\n\\n### Day 4-5\\n- Begin first assignments\\n- Schedule 1-on-1 meetings\\n- Join team standups\\n\\n## First Month\\n- Complete required training modules\\n- Contribute to team projects\\n- Build relationships with colleagues\\n- Regular check-ins with manager\\n\\n## Resources\\n- [Employee Handbook](/handbook)\\n- [IT Support](/it-support)\\n- [Team Directory](/directory)\\n- [Benefits Guide](/benefits)\\n\\n## Questions?\\nReach out to HR or your manager anytime!",
                "change_comment": "Comprehensive onboarding guide with first week schedule, first month goals, and resources",
                "created_by_user_id": "21"
            }),
            Action(name="process_page", kwargs={
                "action": "update",
                "page_id": "1",
                "page_data": {
                    "state": "published",
                    "updated_by_user_id": "21"
                }
            }),
            Action(name="process_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "22",
                    "page_id": "1"
                }
            }),
            Action(name="process_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "23",
                    "page_id": "1"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="3",
        user_id="39",
        instruction=(
            "You are Robin Ellis, a Space Member at robin.ellis@siemens.com. "
            "You need to update coding standards on page_id: 3. "
            "Get the page, create a new version with updated standards, "
            "watch it, and request approval from user_id: 22."
        ),
        actions=[
            Action(name="get_page", kwargs={
                "page_id": "3"
            }),
            Action(name="get_page_versions", kwargs={
                "page_id": "3"
            }),
            Action(name="process_page_version", kwargs={
                "page_id": "3",
                "content": "# Coding Standards\\n\\n## General Principles\\n- Write clean, readable code\\n- Follow DRY (Don't Repeat Yourself)\\n- Keep functions small and focused\\n- Write meaningful variable names\\n\\n## Python Standards\\n- Follow PEP 8 style guide\\n- Use type hints\\n- Maximum line length: 100 characters\\n- Use docstrings for functions and classes\\n\\n```python\\ndef calculate_total(items: List[Item]) -> float:\\n    \"\"\"Calculate total price of items.\\n    \\n    Args:\\n        items: List of items to calculate\\n        \\n    Returns:\\n        Total price as float\\n    \"\"\"\\n    return sum(item.price for item in items)\\n```\\n\\n## JavaScript Standards\\n- Use ES6+ features\\n- Prefer const over let\\n- Use async/await for promises\\n- Follow Airbnb style guide\\n\\n```javascript\\nconst calculateTotal = (items) => {\\n  return items.reduce((total, item) => total + item.price, 0);\\n};\\n```\\n\\n## Code Review\\n- All code must be reviewed\\n- Address all comments before merging\\n- Run tests locally first\\n- Keep PRs focused and small\\n\\n## Testing\\n- Write unit tests for new features\\n- Maintain >80% code coverage\\n- Include integration tests\\n- Test edge cases",
                "change_comment": "Updated coding standards with Python and JavaScript examples, code review guidelines, and testing requirements",
                "created_by_user_id": "39"
            }),
            Action(name="process_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "39",
                    "page_id": "3"
                }
            }),
            Action(name="process_approval_request", kwargs={
                "page_id": "3",
                "requester_user_id": "39",
                "approver_user_id": "22"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="4",
        user_id="22",
        instruction=(
            "You are Jeremy Roberts, a Space Administrator at jeremy.roberts@gmail.com. "
            "Review and approve coding standards updates. "
            "Check pending approvals, review versions, approve, and notify the contributor."
        ),
        actions=[
            Action(name="get_approval_requests", kwargs={
                "filter": "pending",
                "approver_user_id": "22"
            }),
            Action(name="get_page_versions", kwargs={
                "page_id": "3"
            }),
            Action(name="process_approval_decision", kwargs={
                "request_id": "1",
                "decision_type": "approve",
                "decision_comment": "Coding standards are comprehensive and include excellent examples. Approved for publication."
            }),
            Action(name="process_notification", kwargs={
                "user_id": "39",
                "notification_type": "approval",
                "message": "Your coding standards update has been approved. The code examples are particularly helpful!",
                "related_page_id": "3"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="5",
        user_id="185",
        instruction=(
            "You are Aaron Frost, a Content Contributor at aaron.frost@gmail.com. "
            "Export space_id: 2 documentation in PDF format. "
            "Create export, check status, review notifications, and generate audit trail."
        ),
        actions=[
            Action(name="process_exports", kwargs={
                "action": "create",
                "export_data": {
                    "space_id": "2",
                    "export_format": "pdf",
                    "requested_by_user_id": "185"
                }
            }),
            Action(name="get_exports", kwargs={
                "filter": "user",
                "user_id": "185"
            }),
            Action(name="get_notifications", kwargs={
                "user_id": "185",
                "filter": "unread"
            }),
            Action(name="generate_new_audit_trail", kwargs={
                "user_id": "185",
                "action_type": "export_requested",
                "resource_type": "space",
                "resource_id": "2",
                "details": {"format": "pdf", "space_key": "ENG"}
            })
        ],
        outputs=[]
    )
]
