from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="4",
        user_id="3",
        instruction=(
            "You are Samantha Phillips, an Incident Manager. You need to onboard a new enterprise client, locate the relevant product, "
            "create a trial subscription, and record the entire process for auditing."
        ),
        actions=[
            Action(name="create_client", kwargs={
                "client_info": {
                    "client_name": "Blue Horizon Capital",
                    "client_type": "enterprise",
                    "country": "Portugal"
                }
            }),
            Action(name="add_product_reference", kwargs={
                "filters": {
                    "product_id": "1"
                }
            }),
            Action(name="register_subscription", kwargs={
                "subscription_details": {
                    "client_id": "121",
                    "product_id": "1",
                    "subscription_type": "trial",
                    "start_date": "2025-09-17",
                    "sla_tier": "basic",
                    "rto_hours": 24
                }
            }),
            Action(name="record_audit_entry", kwargs={
                "entity_type": "subscription",
                "entity_id": "234",
                "operation_type": "CREATE",
                "changed_by_id": "3"
            }),
            Action(name="generate_onboarding_report", kwargs={
                "client_id": "121",
                "include_details": True
            })
        ],
        outputs=[]
    )
]
