#!/usr/bin/env python3
"""
Interface 5 Task Examples
"""

from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="5",
        user_id="3",
        instruction=(
            "You are an Incident Management Specialist. A critical production incident has been reported. "
            "You need to investigate the incident, coordinate with relevant teams, and ensure proper resolution."
        ),
        actions=[
            Action(name="check_approval", kwargs={
                "action": "incident_management",
                "requester_email": "specialist@corp.org"
            }),
            Action(name="generate_code", kwargs={
                "incident_id": "INC-00123"
            }),
            Action(name="generate_id", kwargs={
                "incident_id": "INC-00123"
            }),
            Action(name="get_info", kwargs={
                "incident_id": "INC-00123"
            }),
            Action(name="invoke", kwargs={
                "incident_id": "INC-00123"
            }),
            Action(name="main", kwargs={
                "incident_id": "INC-00123"
            }),
            Action(name="add_audit_records", kwargs={
                "entity_type": "incident",
                "entity_id": "INC-00123",
                "operation_type": "RESOLVE",
                "changed_by_id": "3"
            })
        ],
        outputs=[]
    )
]

if __name__ == "__main__":
    print("Interface 5 Task Examples")
    print(f"Total test tasks: {len(INTERFACE_5_TEST)}")
    for task in INTERFACE_5_TEST:
        print("Available actions:")
        for action in task.actions:
            print(f"  - {action.name}")
