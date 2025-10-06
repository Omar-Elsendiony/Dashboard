from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="3",
        user_id="3",
        instruction=(
            "You are Samantha Phillips, an Incident Manager. You need to onboard a new enterprise client, locate the relevant product, create a trial subscription, and log the activity for auditing."
        ),
        actions=[
            Action(name="find_clients", kwargs={
                "entity_type": "clients",
                "filters": {
                    "client_name": "Blue Horizon Capital"
                }
            }),
            Action(name="manipulate_clients", kwargs={
                "action": "create",
                "client_data": {
                    "client_name": "Blue Horizon Capital",
                    "client_type": "enterprise",
                    "country": "Portugal"
                }
            }),
            Action(name="find_products", kwargs={
                "entity_type": "products",
                "filters": {
                    "product_id": "1"
                }
            }),
            Action(name="manipulate_client_subscriptions", kwargs={
                "action": "create",
                "subscription_data": {
                    "client_id": "121",
                    "product_id": "1",
                    "subscription_type": "trial",
                    "start_date": "2025-09-17",
                    "sla_tier": "basic",
                    "rto_hours": 24

                }
            }),
            Action(name="manipulate_audit_records", kwargs={
                "entity_type": "subscription",
                "entity_id": "234",
                "operation_type": "INSERT",
                "changed_by_id": "3"
            })
        ],
        outputs=[]
    )
]