from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="user_0002",
        instruction=(
            "Your user ID is user_0002. You are onboarding a contractor for your organization. "
            "Start by creating their contract. Then confirm if the contract is active and the worker has valid compliance. "
            "Only proceed to verify their tax form if compliance is valid."
        ),
        actions=[
            Action(name="create_contract", kwargs={
                "worker_id": "worker_0002",
                "organization_id": "org_2001",
                "contract_type": "contractor",
                "start_date": "2025-07-01",
                "currency": "USD",
                "rate": 80,
                "rate_type": "hourly"
            }),
            Action(name="get_worker_active_contract", kwargs={
                "worker_id": "worker_0002"
            }),
            Action(name="get_compliance_status", kwargs={
                "worker_id": "worker_0002"
            }),
            Action(name="validate_documents", kwargs={
                "worker_id": "worker_0002",
                "document_type": "tax_form"
            })
        ],
        outputs=[]
    )
]
