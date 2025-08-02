from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="agent_maria_101",
        instruction=(
            "You are Agent Maria (‘maria@gmail.com’) working on incident inc_9001 and completed all of the assigned tasks, "
            "and need to register that as you want everyone to know that this critical incident has been resolved. "
            "You have completed the testing as well, but the task for it was not created. You need to record this high-priority "
            "task and mark it as done with an immediate due date of 12 PM, 11th July. If there are no other tasks remaining for "
            "that incident, then update the incident and set the status to resolved, and add a comment 'All tasks completed'. "
            "What helped you to complete the tasks and resolve the issues is a knowledge base article that has the same categorization "
            "as the incident and you want to associate the incident with this article so that future users know how to solve similar kind of incident."
        ),
        actions=[
            Action(name="filter_users", kwargs={
                "email": "maria@gmail.com",
                "role": "agent"
            }),
            Action(name="get_incident_tasks", kwargs={
                "incident_id": "inc_9001"
            }),
            Action(name="update_task", kwargs={
                "task_id": "task_1001",
                "status": "done"
            }),
            Action(name="update_task", kwargs={
                "task_id": "task_1002",
                "status": "done"
            }),
            Action(name="create_incident_task", kwargs={
                "incident_id": "inc_9001",
                "description": "Testing Changes",
                "assigned_to": "agent_maria_101",
                "priority": "high",
                "due_date": "2025-07-11T12:00:00Z"
            }),
            Action(name="update_task", kwargs={
                "task_id": "task_1004",
                "status": "done"
            }),
            Action(name="get_incident_tasks", kwargs={
                "incident_id": "inc_9001"
            }),
            Action(name="update_incident", kwargs={
                "incident_id": "inc_9001",
                "status": "resolved"
            }),
            Action(name="add_incident_comment", kwargs={
                "incident_id": "inc_9001",
                "user_id": "agent_maria_101",
                "comment_text": "All tasks completed",
                "is_public": True
            }),
            Action(name="filter_incidents", kwargs={
                "incident_id": "inc_9001"
            }),
            Action(name="filter_kb_articles", kwargs={
                "category_id": "cat_001",
                "subcategory_id": "sub_cat_001"
            }),
            Action(name="link_incident_to_kb", kwargs={
                "incident_id": "inc_9001",
                "kb_id": "kb_101"
            }),
            Action(name="log_incident_change", kwargs={
                "incident_id": "inc_9001",
                "changed_by": "agent_maria_101"
            })
        ],
        outputs=[]
    )
]
