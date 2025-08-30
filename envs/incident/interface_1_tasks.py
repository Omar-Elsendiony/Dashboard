from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="user_steve_admin_9999",
        instruction=(
            "You are Steve Mar with the email \"steve@target.com\", admin of the security department of Target. "
            "There has been an incident (inc_8001) logged reporting a data leak and passwords for all the agents "
            "of your department have been compromised. You need to handle this incident which is considered a high priority. "
            "You will have to reset the password for all the affected agents, but you have to first log this as a task "
            "having the description 'Resetting passwords for affected users' because the process mandates this. "
            "Then, you will be able to reset the passwords. For other users to know what you did, you want to add a comment "
            "stating 'Passwords Reset for affected users, and an email will be sent for changing the passwords to their inboxes'. "
            "To avoid this situation happening again, you want to coordinate with external security vendors for additional support, "
            "however, you will assign this task to Sara Josh who has the email \"sar.josh@Target.com\" as she has experience "
            "with external affairs, ensuring to add the description \"Coordinating with external security vendors for additional support\". "
            "All the tasks mentioned should be done before 6 PM, 24th July."
        ),
        actions=[
            Action(name="search_users", kwargs={
                "filters": {
                    "name": "steve@target.com"
                }
            }),
            Action(name="get_company_by_name", kwargs={
                "name": "Target"
            }),
            Action(name="search_departments", kwargs={
                "filters": {
                    "company_id": "org_target_002",
                    "name": "Security"
                }
            }),
            Action(name="create_incident_task", kwargs={
                "incident_id": "inc_8001",
                "description": "Resetting passwords for affected users",
                "assigned_to": "user_steve_admin_9999",
                "priority": "high",
                "due_date": "2025-07-24T18:00:00Z"
            }),
            Action(name="search_users", kwargs={
                "first_name": None,
                "last_name": None,
                "role": "agent",
                "company_id": "org_target_002",
                "department_id": "dept_sec_002"
            }),
            Action(name="search_users", kwargs={
                "email": "sar.josh@Target.com"
            }),
            Action(name="create_incident_task", kwargs={
                "incident_id": "inc_8001",
                "description": "Coordinating with external security vendors for additional support",
                "assigned_to": "sarauserid",
                "priority": "high",
                "due_date": "2025-07-24T18:00:00Z"
            }),
            Action(name="add_incident_comment", kwargs={
                "incident_id": "inc_8001",
                "user_id": "user_steve_admin_9999",
                "comment_text": "Passwords Reset for affected users, and an email will be sent for changing the passwords to their inboxes.",
                "is_public": True
            }),
            Action(name="update_task", kwargs={
                "task_id": "task_6001",
                "status": "done"
            }),
            Action(name="update_incident", kwargs={
                "incident_id": "inc_8001",
                "status": "resolved"
            })
        ],
        outputs=[]
    )
]
