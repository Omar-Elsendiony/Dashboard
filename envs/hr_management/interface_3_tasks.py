from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="user_0003",
        instruction=(
            "Your user ID is user_0003. You want to submit a reimbursement for June payroll. "
            "Please first check your time entries and whether the reimbursement amount is within policy. "
            "If allowed, proceed with submission. Then compute gross and net pay based on your hours worked."
        ),
        actions=[
            Action(name="get_time_entries", kwargs={
                "worker_id": "worker_0003",
                "start_date": "2025-06-01",
                "end_date": "2025-06-30"
            }),
            Action(name="validate_reimbursement_limits", kwargs={
                "amount": 300.0
            }),
            Action(name="submit_reimbursement", kwargs={
                "worker_id": "worker_0003",
                "organization_id": "org_3001",
                "amount": 300.0,
                "currency": "EUR",
                "submit_date": "2025-06-30"
            }),
            Action(name="calculate_gross_payroll", kwargs={
                "worker_id": "worker_0003",
                "contract_id": "contract_003",
                "total_hours": 160
            }),
            Action(name="calculate_tax_and_benefits", kwargs={
                "worker_id": "worker_0003",
                "gross_amount": 6400
            })
        ],
        outputs=[]
    )
]
